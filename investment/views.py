# from django.http  import HttpResponse
from typing import Any
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from .forms import *

# Create your views here.
# Homepage
@login_required(login_url='login')
def welcome(request):
    all_property = Property.objects.all()
    context = {
        'all_property': all_property
    }
    return render(request, 'home.html', context=context)

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

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
                return redirect('home')
            else:
                error = True
    else:
        form = LogInForm()
    return render(request, 'users/login.html', {'form': form, 'error': error})

@login_required(login_url='login')
def log_out(request):
    logout(request)
    return redirect(reverse('login'))

# Add property
@login_required(login_url='login')
def add_property(request):
    property_form = PropertyForm()
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        if property_form.is_valid():
            temp = property_form.save()
            property_id = temp.id
 
            temp.assign_interest_rates()
            temp.assign_management_expenses()
            temp.assign_depreciation()
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
            temp.assign_depreciation()
            temp.assign_taxable_amount()
            temp.assign_tax_credits()
            temp.assign_after_tax_cashflow()
            temp.assign_after_tax_cashoncash()
            temp.assign_income()
            temp.assign_irr()
            
            return redirect(f'../addimages/{property_id}')
    context = {
        'property_form': property_form
    }
    return render(request, 'users/addproperty.html', context=context)

def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = EditpropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('propertyitem',pk=pk)
        # fix the redirect.
    else:
        form = EditpropertyForm(instance=property)
    return render(request, 'users/editproperty.html', {'form': form})

@login_required(login_url='login')
def addimages(request, id):
    property = Property.objects.all()
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        # if data['property'] != 'none':
        #     property = Property.objects.get(id=id)
        property = Property.objects.get(id=id)
        print(images, property)
        for image in images:
            images = Images.objects.create(
                property=property,
                image=image
            )
            return redirect('home')
    context = {'property': property}
    return render(request, 'users/addimages.html', context=context)

@login_required(login_url='login')
def view_one_property(request, id):
    property_obj = Property.objects.get(id=id)
    images = Images.objects.filter(property=property_obj)
    context = {
        'property_obj': property_obj,
        'images': images
    }
    return render(request, 'users/propertypage.html', context=context)

#continue Thursday
def interestview(request):
    if request.method == 'POST':
        form = InterestRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = InterestRateForm()
    return render(request, 'users/interestrates.html', {'form': form})