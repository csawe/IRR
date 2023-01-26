from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import fields, widgets


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
class taxoptionsForm(forms.ModelForm):
    class Meta:
        model =  TaxOptions
        fields = ['taxationcapacity','method','taxrate','annualtaxableincome','rate', 'maximumtaxrate','income_rate']   
class managementexpensesForm(forms.ModelForm):
    class Meta:
        model =  ManagementExpenses
        fields = ['vacancyrate','managementfee','managementfeeperyear']               
class RentalIncomeForm(forms.ModelForm):
    class Meta:
        model =  RentalIncome
        fields = ['rentalincreasetype','increasepercentage','averagerentalincomepermonth','amount']        
class comparisonForm(forms.ModelForm):
    class Meta:
        model =  Comparison
        fields = ['description','rate']        
