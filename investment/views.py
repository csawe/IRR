# from django.http  import HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

from django.forms import modelform_factory, formset_factory


# Create your views here.
# Homepage
@login_required(login_url="login")
def welcome(request):
    all_property = Property.objects.all()
    context = {"all_property": all_property}
    return render(request, "home.html", context=context)


def index(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


def log_in(request):
    error = False
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                error = True
    else:
        form = LogInForm()
    return render(request, "users/login.html", {"form": form, "error": error})


@login_required(login_url="login")
def log_out(request):
    logout(request)
    return redirect(reverse("login"))


# Add property
@login_required(login_url="login")
def add_property(request):
    property_form = PropertyForm()
    if request.method == "POST":
        property_form = PropertyForm(request.POST)
        if property_form.is_valid():
            temp = property_form.save()
            property_id = temp.id

            temp.assign_interest_rates()
            temp.assign_management_expenses()
            temp.assign_depreciation()
            temp.assign_tax_options()
            temp.assign_comparison()
            temp.assign_monthlyexpenses()
            temp.assign_ownrenovations()
            temp.assign_loanrenovations()

            temp.assign_inflationrates()
            temp.assign_capitalgrowthrates()
            temp.assign_repairsandmaintenance()
            temp.assign_specialexpenses()
            temp.assign_additionalloanpayments()
            temp.assign_capitalincome()

            # Fill table
            temp.assign_property_value()
            temp.assign_outstanding_loan()
            temp.assign_equity()
            temp.assign_gross_rental_income()
            temp.assign_loan_interest()
            temp.assign_loan_principal()
            temp.assign_total_loan_payment()
            temp.assign_additional_loan_payments()
            temp.assign_renovations_own()
            temp.assign_renovations_loan()
            temp.assign_repairs_and_maintenance()
            temp.assign_special_expenses()
            temp.assign_property_expenses()
            temp.assign_total_property_expenses()
            temp.assign_capital_list()
            temp.assign_pre_tax_cashflow()
            temp.assign_initial_capital_outflow()
            temp.assign_pre_tax_cashoncash()
            temp.assign_taxable_deductions()
            temp.assign_depreciation_list()
            temp.assign_taxable_amount()
            temp.assign_tax_credits()
            temp.assign_after_tax_cashflow()
            temp.assign_after_tax_cashoncash()
            temp.assign_income()
            temp.assign_irr()

            return redirect(f"../addimages/{property_id}")
    context = {"property_form": property_form}
    return render(request, "users/addproperty.html", context=context)


def edit_property(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)
    interestrate_instance = InterestRates.objects.get(property=property_instance)
    interestrates_rates = interestrate_instance.rates
    inflationrates_rates = property_instance.InflationRates
    depreciation_instance = Depreciation.objects.get(property=property_instance)
    capitalgrowthrate_rates = property_instance.CapitalGrowthRates
    monthly_expenses = property_instance.MonthlyExpenses
    own_renovations = property_instance.OwnRenovations
    loan_renovations = property_instance.LoanRenovations
    repairs_maintainences = property_instance.RepairsAndMaintainance
    special_expenses = property_instance.special_expenses_list
    taxoptions_instance = TaxOptions.objects.get(property=property_instance)
    taxoptions_rates = taxoptions_instance.income_rate
    managementexpenses_instance = ManagementExpenses.objects.get(
        property=property_instance
    )
    additionalloan_payments = property_instance.AdditionalLoanPayments
    capital_incomes = property_instance.Capitalincome
    rentalincome_instance = RentalIncome.objects.get(property=property_instance)
    rental_incomes = rentalincome_instance.amount
    comparison_instance = Comparison.objects.get(property=property_instance)
    if request.method == "POST":
        interestrate_forms = InterestRateForm(request.POST)
        interestrate_rateforms = InterestRateFormSet(
            request.POST, prefix="intereset_rateforms"
        )
        inflationrate_rateforms = InflationRatesFormSet(
            request.POST, prefix="inflation_rates"
        )
        depreciation_forms = DepreciationForm(request.POST)
        capitalgrowthrate_rateforms = CapitalGrowthRatesFormSet(
            request.POST, prefix="capitalgrowth_rates"
        )
        monthlyexpenses_forms = MonthlyExpenseFormSet(
            request.POST, prefix="monthly_expenses"
        )
        ownrenovations_forms = OwnRenovationsFormSet(
            request.POST, prefix="own_renovations"
        )
        loanrenovations_forms = LoanRenovationsFormSet(
            request.POST, prefix="loan_renovations"
        )
        repairsmaintainences_forms = RepairsAndMaintenanceFormSet(
            request.POST, prefix="repairsandmaintenance"
        )
        specialexpenses_forms = SpecialExpensesFormSet(
            request.POST, prefix="special_expenses"
        )
        taxoptions_forms = TaxOptionsForm(request.POST)
        taxoptions_rateforms = TaxOptionFormSet(request.POST, prefix="taxoptions_rates")
        managementexpense_forms = ManagementExpensesForm(request.POST)
        additioanloanpayment_forms = AdditionalLoanPaymentFormSet(
            request.POST, prefix="additionalloan_payments"
        )
        capitalincome_forms = CapitalIncomeFormSet(
            request.POST, prefix="capital_income"
        )
        rentalincome_forms = RentalIncomeForm(request.POST)
        rentalincomeamounts_form = RentalIncomeFormSet(
            request.POST, prefix="rental_income"
        )
        comparison_form = ComparisonForm(request.POST)
        # Interst rates
        if interestrate_forms.is_valid() and interestrate_rateforms.is_valid():
            interestrate_instance.property = property_instance
            interestrate_instance.type = interestrate_forms.cleaned_data[
                "interest_type"
            ]
            interestrate_instance.term = interestrate_forms.cleaned_data["term"]
            interestrate_instance.averageinterestrate = interestrate_forms.cleaned_data[
                "averageinterestrate"
            ]
            interestrate_instance.rates = [
                formone.cleaned_data["interestrate"]
                for formone in interestrate_rateforms
            ]
            interestrate_instance.save()
        else:
            print("Interest rate form", interestrate_forms.errors)
            print("Interest rate formrate", interestrate_rateforms.errors)
        # Inflation rates
        if inflationrate_rateforms.is_valid():
            property_instance.InflationRates = [
                formtwo.cleaned_data["inflationrate"]
                for formtwo in inflationrate_rateforms
            ]
            property_instance.save()
        else:
            print("Inlfation rate formrate", inflationrate_rateforms.errors)
        # Depreciation
        if depreciation_forms.is_valid():
            depreciation_instance.property = property_instance
            depreciation_instance.description = depreciation_forms.cleaned_data[
                "description"
            ]
            depreciation_instance.type = depreciation_forms.cleaned_data[
                "depreciation_type"
            ]
            depreciation_instance.value = depreciation_forms.cleaned_data["value"]
            depreciation_instance.rate = depreciation_forms.cleaned_data["rate"]
            depreciation_instance.years = depreciation_forms.cleaned_data["years"]
            depreciation_instance.save()
        else:
            print("Depreciation form", depreciation_forms.errors)
        # Capital Griwth Rate
        if capitalgrowthrate_rateforms.is_valid():
            property_instance.CapitalGrowthRates = [
                formthree.cleaned_data["capitalgrowthrate"]
                for formthree in capitalgrowthrate_rateforms
            ]
            property_instance.save()
        else:
            print("Capital growthrate formrate", capitalgrowthrate_rateforms.errors)
        # Monthly Expense
        if monthlyexpenses_forms.is_valid():
            property_instance.MonthlyExpenses = [
                {
                    "Description": formfour.cleaned_data["monthly_expense_description"],
                    "Value": formfour.cleaned_data["value"],
                }
                for formfour in monthlyexpenses_forms
            ]
            property_instance.save()
        else:
            # print("Monthly expenses form", monthlyexpenses_forms.errors)
            pass
        # Own renovations
        if ownrenovations_forms.is_valid():
            property_instance.OwnRenovations = [
                {
                    "Amount": formfive.cleaned_data["own_renovations_amount"],
                    "Income per year": formfive.cleaned_data["own_renovations_income"],
                }
                for formfive in ownrenovations_forms
            ]
            property_instance.save()
        else:
            print("Own renovations form", ownrenovations_forms.errors)
        # Loan renovations
        if loanrenovations_forms.is_valid():
            property_instance.LoanRenovations = [
                {
                    "Amount": formsix.cleaned_data["loan_renovations_amount"],
                    "Income per year": formsix.cleaned_data["loan_renovations_income"],
                }
                for formsix in loanrenovations_forms
            ]
            property_instance.save()
        else:
            print("Loan renovations form--", loanrenovations_forms.errors)
        # Repairs and Maintenance
        if repairsmaintainences_forms.is_valid():
            property_instance.RepairsAndMaintainance = [
                formseven.cleaned_data["repairsandmaintenance"]
                for formseven in repairsmaintainences_forms
            ]
        else:
            print("Repairs and Maintenence", repairsmaintainences_forms.errors)
        # Special Expenses
        if specialexpenses_forms.is_valid():
            property_instance.special_expenses_list = [
                formeight.cleaned_data["special_expense"]
                for formeight in specialexpenses_forms
            ]
        else:
            print("Special expenses form", specialexpenses_forms.errors)
        # Tax Options
        if taxoptions_forms.is_valid() and taxoptions_rateforms.is_valid():
            ["rate", "maximumtaxrate"]
            taxoptions_instance.property = property_instance
            taxoptions_instance.taxationcapacity = taxoptions_forms.cleaned_data[
                "taxationcapacity"
            ]
            taxoptions_instance.method = taxoptions_forms.cleaned_data["method"]
            taxoptions_instance.taxrate = taxoptions_forms.cleaned_data["taxrate"]
            taxoptions_instance.maximumtaxrate = taxoptions_forms.cleaned_data[
                "maximumtaxrate"
            ]
            taxoptions_instance.income_rate = [
                {
                    "income": formnine.cleaned_data["tax_options_income_rate"],
                    "rate": formnine.cleaned_data["tax_options_rate"],
                }
                for formnine in taxoptions_rateforms
            ]
            taxoptions_instance.save()
        else:
            print("Tax options forms", taxoptions_forms.errors)
            print("Tax options rateforms", taxoptions_rateforms.errors)
        # Management Expenses
        if managementexpense_forms.is_valid():
            managementexpenses_instance.vacancyrate = (
                managementexpense_forms.cleaned_data["vacancyrate"]
            )
            managementexpenses_instance.managementfee = (
                managementexpense_forms.cleaned_data["managementfee"]
            )
            managementexpenses_instance.managementfeeperyear = (
                managementexpense_forms.cleaned_data["managementfeeperyear"]
            )
            managementexpenses_instance.property = managementexpense_forms.cleaned_data[
                "property"
            ]
            managementexpenses_instance.save()
        else:
            print("Management Expenses", managementexpense_forms.errors)
        # Additional Loan Payments
        if additioanloanpayment_forms.is_valid():
            property_instance.AdditionalLoanPayments = [
                formten.cleaned_data["additonalloanpayment"]
                for formten in additioanloanpayment_forms
            ]
            property_instance.save()
        else:
            print("Additional LoanPayment form", additioanloanpayment_forms.errors)
        # Capital Income
        if capitalincome_forms.is_valid():
            property_instance.Capitalincome = [
                formeleven.cleaned_data["capital_income"]
                for formeleven in capitalincome_forms
            ]
            property_instance.save()
        else:
            print("Capital income", capitalincome_forms.errors)
        # Rental Income
        if rentalincome_forms.is_valid() and rentalincomeamounts_form.is_valid():
            rentalincome_instance.property = property_instance
            rentalincome_instance.rentalincreasetype = rentalincome_forms.cleaned_data[
                "rentalincreasetype"
            ]
            rentalincome_instance.increasepercentage = rentalincome_forms.cleaned_data[
                "increasepercentage"
            ]
            rentalincome_instance.averagerentalincomepermonth = (
                rentalincome_forms.cleaned_data["averagerentalincomepermonth"]
            )
            rentalincome_instance.amount = [
                formtwelve.cleaned_data["rental_income"]
                for formtwelve in rentalincomeamounts_form
            ]
            rentalincome_instance.save()
        else:
            print("Rental Income", rentalincome_forms.errors)
            print("Rental Income amount", rentalincomeamounts_form.errors)
        # Comparison
        if comparison_form.is_valid():
            comparison_instance.property = property_instance
            comparison_instance.description = comparison_form.cleaned_data[
                "comparison_description"
            ]
            comparison_instance.comparison_rate = comparison_form.cleaned_data[
                "comparison_rate"
            ]
            comparison_instance.save()
        else:
            print("Comparison form", comparison_form.errors)

    else:
        interestrate_forms = InterestRateForm(instance=interestrate_instance)
        interestrate_rateforms = InterestRateFormSet(
            initial=[
                {"interestrate": interestrate} for interestrate in interestrates_rates
            ],
            prefix="intereset_rateforms",
        )
        inflationrate_rateforms = InflationRatesFormSet(
            initial=[
                {"inflationrate": inflationrate}
                for inflationrate in inflationrates_rates
            ],
            prefix="inflation_rates",
        )
        depreciation_forms = DepreciationForm(instance=depreciation_instance)
        capitalgrowthrate_rateforms = CapitalGrowthRatesFormSet(
            initial=[
                {"capitalgrowthrate": capitalgrowthrate}
                for capitalgrowthrate in capitalgrowthrate_rates
            ],
            prefix="capitalgrowth_rates",
        )
        monthly_expenses_data = []
        for obj in monthly_expenses:
            for key, v in obj.items():
                if key == "Description":
                    monthly_expense_description = v
                elif key == "Value":
                    value = v
            monthly_expenses_data.append(
                {
                    "monthly_expense_description": monthly_expense_description,
                    "value": value,
                }
            )
        monthlyexpenses_forms = MonthlyExpenseFormSet(
            initial=monthly_expenses_data, prefix="monthly_expenses"
        )
        own_renovations_data = []
        for obj in own_renovations:
            for key, v in obj.items():
                if key == "Amount":
                    own_renovations_amount = v
                elif key == "Income per year":
                    own_renovations_income = v
            own_renovations_data.append(
                {
                    "own_renovations_amount": own_renovations_amount,
                    "own_renovations_income": own_renovations_income,
                }
            )
        ownrenovations_forms = OwnRenovationsFormSet(
            initial=own_renovations_data, prefix="own_renovations"
        )
        loan_renovations_data = []
        for obj in loan_renovations:
            for key, v in obj.items():
                if key == "Amount":
                    loan_renovations_amount = v
                elif key == "Income per year":
                    loan_renovations_income = v
            loan_renovations_data.append(
                {
                    "loan_renovations_amount": loan_renovations_amount,
                    "loan_renovations_income": loan_renovations_income,
                }
            )
        loanrenovations_forms = LoanRenovationsFormSet(
            initial=loan_renovations_data, prefix="loan_renovations"
        )
        repairsmaintainences_forms = RepairsAndMaintenanceFormSet(
            initial=[
                {"repairsandmaintenance": repairsandmaintenance}
                for repairsandmaintenance in repairs_maintainences
            ],
            prefix="repairsandmaintenance",
        )
        specialexpenses_forms = SpecialExpensesFormSet(
            initial=[
                {"special_expense": special_expense}
                for special_expense in special_expenses
            ],
            prefix="special_expenses",
        )
        taxoptions_forms = TaxOptionsForm(instance=taxoptions_instance)
        taxoptions_data = []
        for obj in taxoptions_rates:
            for key, v in obj.items():
                if key == "income":
                    tax_options_income_rate = v
                elif key == "rate":
                    tax_options_rate = v
            taxoptions_data.append(
                {
                    "tax_options_income_rate": tax_options_income_rate,
                    "tax_options_rate": tax_options_rate,
                }
            )
        taxoptions_rateforms = TaxOptionFormSet(
            initial=taxoptions_data, prefix="taxoptions_rates"
        )
        managementexpense_forms = ManagementExpensesForm(
            instance=managementexpenses_instance
        )
        additioanloanpayment_forms = AdditionalLoanPaymentFormSet(
            initial=[
                {"additonalloanpayment": additonalloanpayment}
                for additonalloanpayment in additionalloan_payments
            ],
            prefix="additionalloan_payments",
        )
        capitalincome_forms = CapitalIncomeFormSet(
            initial=[
                {"capital_income": capital_income} for capital_income in capital_incomes
            ],
            prefix="capital_income",
        )
        rentalincome_forms = RentalIncomeForm(instance=rentalincome_instance)
        rentalincomeamounts_form = RentalIncomeFormSet(
            initial=[
                {"rental_income": rental_income} for rental_income in rental_incomes
            ],
            prefix="rental_income",
        )
        comparison_form = ComparisonForm(instance=comparison_instance)
    context = {
        "interestrate_forms": interestrate_forms,
        "interestrate_rateforms": interestrate_rateforms,
        "inflationrate_rateforms": inflationrate_rateforms,
        "depreciation_forms": depreciation_forms,
        "capitalgrowthrate_rateforms": capitalgrowthrate_rateforms,
        "monthlyexpenses_forms": monthlyexpenses_forms,
        "ownrenovations_forms": ownrenovations_forms,
        "loanrenovations_forms": loanrenovations_forms,
        "repairsmaintainences_forms": repairsmaintainences_forms,
        "specialexpenses_forms": specialexpenses_forms,
        "taxoptions_forms": taxoptions_forms,
        "taxoptions_rateforms": taxoptions_rateforms,
        "managementexpense_forms": managementexpense_forms,
        "additioanloanpayment_forms": additioanloanpayment_forms,
        "capitalincome_forms": capitalincome_forms,
        "rentalincome_forms": rentalincome_forms,
        "rentalincomeamounts_form": rentalincomeamounts_form,
        "comparison_form": comparison_form,
    }
    return render(request, "users/editproperty2.html", context=context)


@login_required(login_url="login")
def addimages(request, id):
    property = Property.objects.all()
    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist("images")
        # if data['property'] != 'none':
        #     property = Property.objects.get(id=id)
        property = Property.objects.get(id=id)
        print(images, property)
        for image in images:
            images = Images.objects.create(property=property, image=image)
            return redirect("home")
    context = {"property": property}
    return render(request, "users/addimages.html", context=context)


@login_required(login_url="login")
def view_one_property(request, id):
    property_obj = Property.objects.get(id=id)
    images = Images.objects.filter(property=property_obj)
    growth_rate_list = property_obj.CapitalGrowthRates
    property_value_list = property_obj.property_value_list
    outstanding_list = property_obj.loan_amount_list
    equity_list = property_obj.equity_list
    zipped_lists = zip(
        growth_rate_list, property_value_list, outstanding_list, equity_list
    )
    data_1 = list(property_value_list)
    data_2 = list(outstanding_list)
    context = {
        "property_obj": property_obj,
        "images": images,
        "zipped_lists": zipped_lists,
        'data_1': data_1,
        'data_2' : data_2, 
    }
    return render(request, "users/propertypage.html", context=context)


# continue Thursday
def interestview(request):
    if request.method == "POST":
        form = InterestRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = InterestRateForm()
    return render(request, "users/interestrates.html", {"form": form})
