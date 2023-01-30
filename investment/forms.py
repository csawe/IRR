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
        fields = ['averageinterestrate', 'type', 'term', 'rates']
class DepreciationForm(forms.ModelForm):
    class Meta:
        model = Depreciation
        fields = ['description','type','value','rate','years']    
class TaxOptionsForm(forms.ModelForm):
    class Meta:
        model =  TaxOptions
        fields = ['taxationcapacity','method','taxrate','annualtaxableincome','rate', 'maximumtaxrate','income_rate']   
class ManagementExpensesForm(forms.ModelForm):
    class Meta:
        model =  ManagementExpenses
        fields = ['vacancyrate','managementfee','managementfeeperyear']               
class RentalIncomeForm(forms.ModelForm):
    class Meta:
        model =  RentalIncome
        fields = ['rentalincreasetype','increasepercentage','averagerentalincomepermonth','amount']        
        
class ComparisonForm(forms.ModelForm):
    class Meta:
        model =  Comparison
        fields = ['description','rate']        

class RateForm(forms.Form):
    rate = forms.IntegerField()
RateFormSet = forms.formset_factory(RateForm, extra=0)

class JsonForm(forms.Form):
    data = forms.JSONField()
JsonFormSet = forms.formset_factory(JsonForm, extra=0)

#Model1Formset = formset_factory(EditpropertyForm, extra=1) # Photograph
Model2Formset = formset_factory(InterestRateForm, extra=1) # Interest Rate Options -- Interest form
class InflationRatesForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['InflationRates']
Model3Formset = formset_factory(InflationRatesForm, extra=1) # Inflation Rates
Model4Formset = formset_factory(DepreciationForm, extra=1) # Depreciation
class CapitalGrowthRatesForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['CapitalGrowthRates']
Model5Formset = formset_factory(CapitalGrowthRatesForm, extra=1) # Capital Growth Rates
class MonthlyExpensesForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['MonthlyExpenses']
Model6Formset = formset_factory(MonthlyExpensesForm, extra=1) # Monthly Expenses
class OwnRenovationsForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['OwnRenovations']
Model7Formset = formset_factory(OwnRenovationsForm, extra=1) # Renovations(Own)
class LoanRenovationsForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['LoanRenovations']
Model8Formset = formset_factory(LoanRenovationsForm, extra=1) # Renovations(Loan)
class RepairsForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['RepairsAndMaintainance']
Model9Formset = formset_factory(RepairsForm, extra=1) # Repairs & Maintenance
class SpecialExpensesForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['Specialexpenses']
Model10Formset = formset_factory(SpecialExpensesForm, extra=1) # Special Expenses
Model11Formset = formset_factory(TaxOptionsForm, extra=1) # Tax Options
Model12Formset = formset_factory(ManagementExpensesForm, extra=1) # Management Expenses
class AdditionalLoanPaymentsForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['AdditionalLoanPayments']
Model13Formset = formset_factory(AdditionalLoanPaymentsForm, extra=1) # Additional Loan Payments 
class CapitalIncomeForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['Capitalincome']
Model14Formset = formset_factory(CapitalIncomeForm, extra=1) # Capital Income
Model15Formset = formset_factory(RentalIncomeForm, extra=1) # Rental Income
Model16Formset = formset_factory(ComparisonForm, extra=1) # Compariosn