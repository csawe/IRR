from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import fields, widgets, formset_factory


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['prof_pic', 'f_name', 'l_name', 'phone', 'bio']
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'property_type', 'purchase_price', 'deposit', 'City',
                  'bond_value', 'notes']
        widgets = {
            'name': widgets.Input(attrs={
                'class': 'form-control',
                'placeholder': 'Five bedroom townhouse',
                'id': 'name'
            }),
            'property_type': widgets.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select type',
                'id': 'property_type'
            }),
            'purchase_price': widgets.Input(attrs={
                'class': 'form-control',
                'placeholder': '4000000',
                'id': 'purchase_price'
            }),
            'deposit': widgets.Input(attrs={
                'class': 'form-control',
                'placeholder': '300000',
                'id': 'deposit'
            }),
            'City': widgets.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Location',
                'id': 'City'
            }),
            'bond_value': widgets.Input(attrs={
                'class': 'form-control',
                'placeholder': '-----',
                'id': 'bond_value',
                'readonly': 'readonly'
            }),
            'notes': widgets.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any Other Information',
                'id': 'notes'
            }),
        }
        def save(self, commit=True):
            instance = super().save(commit=False)
            purchase_price = self.cleaned_data['purchase_price']
            deposit = self.cleaned_data['deposit']
            instance.bond_value = purchase_price - deposit
            if commit:
                instance.save()
            return instance
        ##pick up from here on wednesday
class EditpropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'property_type', 'purchase_price', 'deposit', 'City', 'bond_value', 'notes']      
class InterestRateForm(forms.ModelForm):
    class Meta:
        model = InterestRates
        fields = ['property','averageinterestrate', 'interest_type', 'term']
class DepreciationForm(forms.ModelForm):
    class Meta:
        model = Depreciation
        fields = ['property','description','depreciation_type','value','rate','years']    
class TaxOptionsForm(forms.ModelForm):
    class Meta:
        model =  TaxOptions
        fields = ['property','taxationcapacity','method','taxrate','maximumtaxrate']   
class ManagementExpensesForm(forms.ModelForm):
    class Meta:
        model =  ManagementExpenses
        fields = ['vacancyrate','managementfee','managementfeeperyear', 'property']               
class RentalIncomeForm(forms.ModelForm):
    class Meta:
        model =  RentalIncome
        fields = ['rentalincreasetype','increasepercentage','averagerentalincomepermonth','amount']              
class ComparisonForm(forms.ModelForm):
    class Meta:
        model =  Comparison
        fields = ['description','rate']        

class InterestRateFormRate(forms.Form):
    interestrate = forms.IntegerField()
InterestRateFormSet = forms.formset_factory(InterestRateFormRate, extra=0)# Interest Rate Options -- Rate form
class InflationRateFormRate(forms.Form):
    inflationrate = forms.IntegerField()
InflationRatesFormSet = forms.formset_factory(InflationRateFormRate, extra=0)# Inflation Rates -- Rate form
class CapitalGrowthRatesFormRate(forms.Form):
    capitalgrowthrate = forms.IntegerField()
CapitalGrowthRatesFormSet = forms.formset_factory(CapitalGrowthRatesFormRate, extra=0) # Capital Growth Rate
class MonthlyExpensesFormJson(forms.Form):
    monthly_expense_description = forms.CharField()
    value = forms.CharField()
MonthlyExpenseFormSet = forms.formset_factory(MonthlyExpensesFormJson, extra=0) # Monthly Expenses
class OwnRenovationsFormJson(forms.Form):
    own_renovations_amount = forms.IntegerField()
    own_renovations_income = forms.IntegerField()
OwnRenovationsFormSet = forms.formset_factory(OwnRenovationsFormJson, extra=0) # Own renovations
class LoanRenovationsFormJson(forms.Form):
    loan_renovations_amount = forms.IntegerField()
    loan_renovations_income = forms.IntegerField()
LoanRenovationsFormSet = forms.formset_factory(LoanRenovationsFormJson, extra=0) # Loan renovations
class RepairsAndMaintenanceForm(forms.Form):
    repairsandmaintenance = forms.IntegerField()
RepairsAndMaintenanceFormSet = forms.formset_factory(RepairsAndMaintenanceForm, extra=0) # Repairs and Maintenance# Repairs & Maintenance
class SpecialExpensesForm(forms.Form):
    special_expense = forms.IntegerField()
SpecialExpensesFormSet = forms.formset_factory(SpecialExpensesForm, extra=0) # Special Expenses
class TaxOptionsFormJson(forms.Form):
    tax_options_income_rate = forms.IntegerField()
    tax_options_rate = forms.IntegerField()
TaxOptionFormSet = forms.formset_factory(TaxOptionsFormJson, extra=0)
class AdditionalLoanPaymentsForm(forms.Form):
    additonalloanpayment  = forms.IntegerField()
AdditionalLoanPaymentFormSet = forms.formset_factory(AdditionalLoanPaymentsForm, extra=0) # Additional Loan Payments 

class CapitalIncomeForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['Capitalincome']
Model14Formset = formset_factory(CapitalIncomeForm, extra=1) # Capital Income
Model15Formset = formset_factory(RentalIncomeForm, extra=1) # Rental Income
Model16Formset = formset_factory(ComparisonForm, extra=1) # Compariosn