from django.db import models
from datetime import date, timedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField

# from scipy.optimize import root
import numpy_financial as npf
from django.contrib.postgres.fields import ArrayField


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = "email"  # make the user log in with the email
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    prof_pic = CloudinaryField(
        "images",
        default="http://res.cloudinary.com/dim8pysls/image/upload/v1639001486"
        "/x3mgnqmbi73lten4ewzv.png",
    )
    bio = models.TextField(blank=True, max_length=255, default="please update your bio")
    f_name = models.CharField(blank=True, max_length=255)
    l_name = models.CharField(blank=True, max_length=50)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.f_name


class PropertyType(models.Model):
    name = models.CharField(max_length=252, null=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=252, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=252, null=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=252, null=True)
    property_type = models.ForeignKey(PropertyType, null=True, on_delete=models.CASCADE)
    City = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    purchase_price = models.FloatField(null=True)
    deposit = models.FloatField(null=True)
    market_value = models.FloatField(null=True)
    bond_value = models.IntegerField(null=True)
    purchase_date = models.DateField(auto_now_add=True, null=True)
    notes = models.TextField(max_length=1260, null=True)
    InflationRates = ArrayField(models.IntegerField(), null=True, default=list)
    CapitalGrowthRates = ArrayField(models.IntegerField(), null=True, default=list)
    MonthlyExpenses = ArrayField(models.JSONField(), null=True, default=list)
    OwnRenovations = ArrayField(models.JSONField(), null=True, default=list)
    LoanRenovations = ArrayField(models.JSONField(), null=True, default=list)
    RepairsAndMaintainance = ArrayField(models.IntegerField(), null=True, default=list)
    Specialexpenses = ArrayField(models.IntegerField(), null=True, default=list)
    AdditionalLoanPayments = ArrayField(models.IntegerField(), null=True, default=list)
    Capitalincome = ArrayField(models.IntegerField(), null=True, default=list)
    # Begin of array fields
    property_value_list = ArrayField(models.IntegerField(), default=list)

    def assign_property_value(self):
        purchase_price = self.purchase_price
        rate = self.CapitalGrowthRates if self.CapitalGrowthRates else [1] * 30
        for i in range(30):
            property_value = purchase_price * (1 + rate[i] / 100) ** i
            self.property_value_list.append(property_value)
        self.save()

    loan_amount_list = ArrayField(models.IntegerField(), default=list)

    def assign_outstanding_loan(self):
        interest_rate = sum(
            InterestRates.objects.get(property=Property.objects.get(id=self.id)).rates
        ) / len(
            InterestRates.objects.get(property=Property.objects.get(id=self.id)).rates
        )
        for year in range(30):
            outstanding_loan = int(
                self.bond_value * (1 - interest_rate / 100) ** (year + 1)
            )
            self.loan_amount_list.append(outstanding_loan)
        self.save()

    equity_list = ArrayField(models.IntegerField(), default=list)

    def assign_equity(self):
        for i in range(30):
            equity = self.property_value_list[i] - self.loan_amount_list[i]
            self.equity_list.append(equity)
        self.save()

    gross_rental_income_list = ArrayField(models.IntegerField(), default=list)

    def assign_gross_rental_income(self):
        management_expenses = ManagementExpenses.objects.get(
            property=Property.objects.get(id=self.id)
        )
        rent = RentalIncome(
            increasepercentage=2,
            averagerentalincomepermonth=1800,
            property=Property.objects.get(id=self.id),
        )
        for _ in range(30):
            income = (
                rent.averagerentalincomepermonth * 12
            ) - management_expenses.managementfeeperyear
            self.gross_rental_income_list.append(income)
            self.save()
        rent.save()

    loan_interest_list = ArrayField(models.IntegerField(), default=list)

    def assign_loan_interest(self):
        interest_rate = sum(
            InterestRates.objects.get(property=Property.objects.get(id=self.id)).rates
        ) / len(
            InterestRates.objects.get(property=Property.objects.get(id=self.id)).rates
        )
        for i in range(30):
            interest = self.loan_amount_list[i] * interest_rate / 100
            self.loan_interest_list.append(interest)
        self.save()

    loan_principle_list = ArrayField(models.IntegerField(), default=list)

    def assign_loan_principal(self):
        for i in range(30):
            principal = self.loan_amount_list[i] - self.loan_interest_list[i]
            self.loan_principle_list.append(principal)
        self.save()

    total_loan_payment_list = ArrayField(models.IntegerField(), default=list)

    def assign_total_loan_payment(
        self, interest_change_year=None, new_interest_rate=None
    ):
        bond_price = self.bond_value
        interest_rate = sum(
            InterestRates.objects.get(property=Property.objects.get(id=self.id)).rates
        ) / len(
            InterestRates.objects.get(property=Property.objects.get(id=self.id)).rates
        )
        term = InterestRates.objects.get(property=Property.objects.get(id=self.id)).term
        for i in range(30):
            if interest_change_year is None or new_interest_rate is None:
                total_loan_payment = (
                    bond_price * interest_rate / (1 - (1 + interest_rate) ** term)
                )
            else:
                if interest_change_year > term:
                    raise ValueError(
                        "Interest change year cannot be greater than loan term."
                    )
                new_interest_rate = new_interest_rate / 100
                total_loan_payment = bond_price * interest_rate / (
                    1 - (1 + interest_rate) ** interest_change_year
                ) + bond_price * (1 + interest_rate) ** (
                    -interest_change_year
                ) * new_interest_rate / (
                    1 - (1 + new_interest_rate) ** (term - interest_change_year)
                )
            self.total_loan_payment_list.append(total_loan_payment)
        self.save()

    additional_loan_payment_list = ArrayField(models.IntegerField(), default=list)

    def assign_additional_loan_payments(self):
        pass

    renovations_own_list = ArrayField(models.JSONField(), default=list)

    def assign_renovations_own(self):
        pass

    renovations_loan_list = ArrayField(models.JSONField(), default=list)

    def assign_renovations_loan(self):
        pass

    repairs_and_maintenance_list = ArrayField(models.IntegerField(), default=list)

    def assign_repairs_and_maintenance(self):
        for i in range(30):
            self.repairs_and_maintenance_list.append(0)
        self.save()

    special_expenses_list = ArrayField(models.IntegerField(), default=list)

    def assign_special_expenses(self):
        for i in range(30):
            self.special_expenses_list.append(0)
        self.save()

    property_expenses_list = ArrayField(models.IntegerField(), default=list)

    def assign_property_expenses(self):
        monthly_expense = 2000  # monthly_expense = self.MonthlyExpense.value
        for i in range(30):
            expenses = monthly_expense * 12
            self.property_expenses_list.append(expenses)
        self.save()

    total_property_expenses_list = ArrayField(models.IntegerField(), default=list)

    def assign_total_property_expenses(self):
        for i in range(30):
            property_expenses_per_year = self.property_expenses_list[i]
            special_expenses = self.special_expenses_list[i]
            # ownrenovations = self.OwnRenovations.amount
            # LoanRenovations = self.LoanRenovations.amount
            repairs_maintenance = self.repairs_and_maintenance_list[i]
            total = property_expenses_per_year + special_expenses + repairs_maintenance
            self.total_property_expenses_list.append(total)
        self.save()

    capital_received_list = ArrayField(models.IntegerField(), default=list)

    def assign_capital_list(self):
        for _ in range(30):
            self.capital_received_list.append(0)
        self.save()

    pre_tax_cashflow_list = ArrayField(models.IntegerField(), default=list)

    def assign_pre_tax_cashflow(self):
        for i in range(30):
            cash_flow = (
                self.gross_rental_income_list[i] + self.capital_received_list[i]
            ) - (self.total_property_expenses_list[i] + self.total_loan_payment_list[i])
            self.pre_tax_cashflow_list.append(cash_flow)
        self.save()

    initial_capital_outflow_list = ArrayField(models.IntegerField(), default=list)

    def assign_initial_capital_outflow(self):
        deposit = self.deposit
        other_costs = 0  # Assign other costs
        for _ in range(30):
            outflow = deposit + other_costs
            self.initial_capital_outflow_list.append(outflow)
        self.save()

    pre_tax_cashoncash_list = ArrayField(models.IntegerField(), default=list)

    def assign_pre_tax_cashoncash(self):
        for i in range(30):
            cash_on_cash = (
                self.pre_tax_cashflow_list[i]
                / self.initial_capital_outflow_list[i]
                * 100
            )
            self.pre_tax_cashoncash_list.append(cash_on_cash)
        self.save()

    total_taxable_deductions_list = ArrayField(models.IntegerField(), default=list)

    def assign_taxable_deductions(self):
        for i in range(30):
            deductions = (
                self.loan_interest_list[i] + self.total_property_expenses_list[i]
            )
            self.total_taxable_deductions_list.append(deductions)
        self.save()

    depreciation_list = ArrayField(models.IntegerField(), default=list)

    def assign_depreciation_list(self, depreciation_type="straight"):
        if depreciation_type == "straight":
            rate = (
                Depreciation.objects.get(property=Property.objects.get(id=self.id)).rate
            ) / 100
            years = Depreciation.objects.get(
                property=Property.objects.get(id=self.id)
            ).years
            purchase_date = self.purchase_date
            purchase_price = self.purchase_price
            annual_depreciation = purchase_price * rate
            total_depreciation = annual_depreciation * years
            remaining_value = purchase_price - total_depreciation
            for i in range(30):
                # current_date = purchase_date + timedelta(days=365*(year+1))
                current_depreciation = annual_depreciation * (i + 1)
                self.depreciation_list.append(current_depreciation)  # Fix formula
            self.save()
        elif depreciation_type == "Diminishing":
            rate = (
                Depreciation.objects.get(property=Property.objects.get(id=self.id)).rate
            ) / 100
            years = Depreciation.objects.get(
                property=Property.objects.get(id=self.id)
            ).years
            purchase_date = self.purchase_date
            purchase_price = self.purchase_price
            for i in range(30):
                annual_depreciation = purchase_price * (rate * (years - i)) / years
                self.depreciation_list.append(annual_depreciation)
            self.save()

    taxable_amaount_list = ArrayField(models.IntegerField(), default=list)

    def assign_taxable_amount(self):
        for i in range(30):
            amount = self.gross_rental_income_list[i] - (
                self.total_taxable_deductions_list[i] + self.depreciation_list[i]
            )
            self.taxable_amaount_list.append(amount)
        self.save()

    tax_credit_list = ArrayField(models.IntegerField(), default=list)

    def assign_tax_credits(self):
        for i in range(30):
            credit = self.total_taxable_deductions_list[i] * 0.3
            self.tax_credit_list.append(credit)
        self.save()

    after_tax_cashflow_list = ArrayField(models.IntegerField(), default=list)

    def assign_after_tax_cashflow(self):
        for i in range(30):
            cashflow = self.pre_tax_cashflow_list[i] + self.tax_credit_list[i]
            self.after_tax_cashflow_list.append(cashflow)
        self.save()

    after_tax_cashoncash_list = ArrayField(models.IntegerField(), default=list)

    def assign_after_tax_cashoncash(self):
        for i in range(30):
            cash_on_cash = (
                self.after_tax_cashflow_list[i] / self.initial_capital_outflow_list[i]
            ) * 100
            self.after_tax_cashoncash_list.append(cash_on_cash)
        self.save()

    income_per_month_list = ArrayField(models.IntegerField(), default=list)

    def assign_income(self):
        for i in range(30):
            income = self.after_tax_cashflow_list[i] / 12
            self.income_per_month_list.append(income)
        self.save()

    irr_list = ArrayField(models.IntegerField(), default=list)

    def assign_irr(self):
        pass

    # def assign_inflation_rates(self):
    #     pass

    # Assign interest Rates
    def assign_monthlyexpenses(self):
        description = ["Water", "Insurance", "Maintenance", "Bank charges", "Other"]
        for i in description:
            key = {"Description": i, "Value": 0}
            self.MonthlyExpenses.append(key)
        self.save()

    def assign_ownrenovations(self):
        for i in range(30):
            key = {"Amount": 0, "Income per year": 0}
            self.OwnRenovations.append(key)
        self.save()

    def assign_loanrenovations(self):
        for i in range(30):
            key = {"Amount": 0, "Income per year": 0}
            self.LoanRenovations.append(key)
        self.save()

    def assign_tax_options(self):
        income_rate = []
        for _ in range(2):
            income_rate.append({"income": 1000, "rate": 100})
        taxoptions = TaxOptions(
            taxationcapacity="Personal",
            method="0%",
            taxrate=0,
            maximumtaxrate=0,
            income_rate=income_rate,
            property=Property.objects.get(id=self.id),
        )
        taxoptions.save()
        pass

    def assign_interest_rates(self):
        rates = [9] * 30
        interest_rate = InterestRates(
            interest_type="Interest & capital",
            term=20,
            rates=rates,
            property=Property.objects.get(id=self.id),
        )
        interest_rate.save()

    def assign_inflationrates(self):
        for _ in range(30):
            self.InflationRates.append(0)
        self.save()

    def assign_capitalgrowthrates(self):
        for _ in range(30):
            self.CapitalGrowthRates.append(0)
        self.save()

    def assign_repairsandmaintenance(self):
        for _ in range(30):
            self.RepairsAndMaintainance.append(0)
        self.save()

    def assign_specialexpenses(self):
        for _ in range(30):
            self.Specialexpenses.append(0)
        self.save()

    def assign_additionalloanpayments(self):
        for _ in range(30):
            self.AdditionalLoanPayments.append(0)
        self.save()

    def assign_capitalincome(self):
        for _ in range(30):
            self.Capitalincome.append(0)
        self.save()

    # Assign management expenses
    def assign_management_expenses(self):
        management_expenses = ManagementExpenses(
            vacancyrate=8,
            managementfee=8,
            managementfeeperyear=1728,
            property=Property.objects.get(id=self.id),
        )
        management_expenses.save()

    # depreciation
    def assign_depreciation(self):
        depreciation = Depreciation(
            depreciation_type="Straight",
            value=2,
            rate=2,
            years=30,
            property=Property.objects.get(id=self.id),
        )
        depreciation.save()

    def assign_comparison(self):
        comparison = Comparison(property=Property.objects.get(id=self.id))
        comparison.save()

    def __str__(self):
        return self.name


class OtherCosts(models.Model):
    CHOICES = (
        ("Property Taxes", "Property Taxes"),
        ("Repairs & Utilities", "Repairs & Utilities"),
        ("Mortgage Insurance", "Mortgage Insurance"),
    )
    other_costs = models.CharField(max_length=255, null=True, choices=CHOICES)
    amount = models.IntegerField(null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.other_costs


class Images(models.Model):
    image = CloudinaryField(
        "images",
        default="http://res.cloudinary.com/dim8pysls/image/upload/v1639001486"
        "/x3mgnqmbi73lten4ewzv.png",
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class InterestRates(models.Model):
    averageinterestrate = models.FloatField(
        ("Average Interest Rate (%)"), null=True, default=10
    )
    interest_type = models.CharField(
        null=True,
        max_length=50,
        default="Interest & capital",
        choices=(
            ("Interest & capital", "Interest & capital"),
            ("Interest Only", "Interest Only"),
        ),
    )
    term = models.IntegerField(null=True)
    # years = models.IntegerField(null=True,editable=False)
    rates = ArrayField(models.IntegerField(), default=list)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.term)


class Depreciation(models.Model):
    description = models.CharField(null=True, max_length=255, blank=True)
    depreciation_type = models.CharField(
        null=True,
        max_length=50,
        default="Straight",
        choices=(
            ("Straight", "Straight"),
            ("Diminishing", "Diminishing"),
        ),
    )
    value = models.FloatField(null=True)
    rate = models.IntegerField(("Rate (%)"), null=True, default=8, blank=True)
    years = models.IntegerField(null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.rate)


class TaxOptions(models.Model):
    taxationcapacity = models.CharField(
        null=True,
        max_length=50,
        default="Interest & capital",
        choices=(
            ("Personal", "Personal"),
            ("close corporation", "close corporation"),
            ("private company", "private company"),
            ("trust", "trust"),
        ),
    )
    method = models.CharField(
        null=True,
        max_length=50,
        default="Interest & capital",
        choices=(
            ("0%", "0%"),
            ("Marginal", "Marginal"),
            ("Use Tax Table", "Use Tax Table"),
            ("Custom", "Custom"),
        ),
    )
    taxrate = models.FloatField(("Tax Rate(%)"), null=True)
    # annualtaxableincome = models.FloatField(('Annual Taxableincome(%)'),null=False)
    # rate = models.IntegerField(null=True)
    maximumtaxrate = models.IntegerField(("Maximum Tax Rate (%)"), null=False)
    income_rate = ArrayField(models.JSONField(), null=True, default=list, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    # def __str__(self):
    #     return str(self.rate)


class ManagementExpenses(models.Model):
    vacancyrate = models.IntegerField(("Vacancy Rate (%)"), null=True, default=0)
    managementfee = models.IntegerField(("Management Fee (%)"), null=True, default=0)
    managementfeeperyear = models.IntegerField(("Management Fee per Year "))
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.vacancyrate)


class RentalIncome(models.Model):
    rentalincreasetype = models.CharField(
        ("Type"),
        null=True,
        max_length=50,
        default="capital",
        choices=(
            ("capital", "capital"),
            ("inflation", "inflation"),
            ("percent", "percent"),
        ),
    )
    increasepercentage = models.IntegerField(("Increase Percentage (%)"))
    averagerentalincomepermonth = models.FloatField(
        ("Average Rental Income Per Month"), null=True
    )
    amount = ArrayField(
        models.IntegerField(), default=list
    )  # amount = models.IntegerField(('Amount'),null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.rentalincreasetype


class Comparison(models.Model):
    comparison_description = models.CharField(max_length=255, null=True, blank=True)
    comparison_rate = models.IntegerField(
        ("Rate (%)"), null=True, default=0, blank=True
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.comparison_description)
