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

    # photograph
    interestrate_instance = get_object_or_404(InterestRates, property=property_instance)
    interestrates_rates = interestrate_instance.rates
    # # inflationrate_instance = get_object_or_404(Property, pk=pk)
    # inflationrates_rates = property_instance.InflationRates
    # depreciation_instance = get_object_or_404(Depreciation, property=property_instance)
    # # capitalgrowthrates_instance = get_object_or_404(Property, pk=pk)
    # capitalgrowthrates_rates = property_instance.CapitalGrowthRates
    # # monthlyexpense_instance = get_object_or_404(Property, pk=pk)
    # # ownrenovations_instance = get_object_or_4-4(Property, pk=pk)
    # ownrenovations_list = property_instance.OwnRenovations
    # # loanrenovations_instance = get_object_or_4-4(Property, pk=pk)
    # # repairsandmaintenance_instace = get_object_or_404(Property, pk=pk)
    # repairs_list = property_instance.RepairsAndMaintainance
    # # specialexpenses_instance = get_object_or_404(Property, pk=pk)
    # special_list = property_instance.Specialexpenses
    # taxoptions_instance = get_object_or_404(TaxOptions, property=property_instance)
    # managementexpenses_instance = get_object_or_404(ManagementExpenses, property=property_instance)
    # # additionalloanpayments_instance = get_object_or_404(Property, pk=pk)
    # additionpayments_list = property_instance.AdditionalLoanPayments
    # # capitalincome_instance = get_object_or_404(Property, pk=pk)
    # capitalincome_list = property_instance.Capitalincome
    # rentalincome_instance = get_object_or_404(RentalIncome, property=property_instance)
    # rentalincome_list = rentalincome_instance.amount
    # comparison_instance = get_object_or_404(Comparison, property=property_instance)

    if request.method == "POST":
        # model1_formset = Model1Formset(request.POST, prefix='model1')
        model2_formset = InterestRateForm(request.POST)
        interestrate_rateforms = RateFormSet(request.POST)
        # model3_formset = Model3Formset(request.POST, prefix='model3')
        # inflationrates_rateforms = RateFormSet(request.POST)
        # model4_formset = Model4Formset(request.POST, prefix='model4')
        # model5_formset = Model5Formset(request.POST, prefix='model5')
        # capitalgrowthrates_rateforms = RateFormSet(request.POST)
        # model6_formset = Model6Formset(request.POST, prefix='model6')
        # model7_formset = Model7Formset(request.POST, prefix='model7')
        # ownrenovations_jsonforms = JsonFormSet(request.POST)
        # model8_formset = Model8Formset(request.POST, prefix='model8')
        # model9_formset = Model9Formset(request.POST, prefix='model9')
        # repairs_rateforms = RateFormSet(request.POST)
        # model10_formset = Model10Formset(request.POST, prefix='model10')
        # special_rateforms = RateFormSet(request.POST)
        # model11_formset = Model11Formset(request.POST, prefix='model11')
        # model12_formset = Model12Formset(request.POST, prefix='model12')
        # model13_formset = Model13Formset(request.POST, prefix='model13')
        # additionalpayments_rateforms = RateFormSet(request.POST)
        # model14_formset = Model14Formset(request.POST, prefix='model14')
        # capitalincome_rateforms = RateFormSet(request.POST)
        # model15_formset = Model15Formset(request.POST, prefix='model15')
        # rentalincome_rateforms = RateFormSet(request.POST)
        # model16_formset = Model16Formset(request.POST, prefix='model16')

        if model2_formset.is_valid() and interestrate_rateforms.is_valid():
            # and model3_formset.is_valid() and inflationrates_rateforms.is_valid() and model4_formset.is_valid() and \
            #     model5_formset.is_valid() and capitalgrowthrates_rateforms.is_valid() and model6_formset.is_valid() and model7_formset.is_valid() and ownrenovations_jsonforms.is_valid() and \
            #         model8_formset.is_valid() and model9_formset.is_valid() and repairs_rateforms.is_valid() and model10_formset.is_valid() and special_rateforms.is_valid() and \
            #             model11_formset.is_valid() and model12_formset.is_valid() and model13_formset.is_valid() and additionalpayments_rateforms.is_valid() and \
            #                 model14_formset.is_valid() and capitalincome_rateforms.is_valid() and model15_formset.is_valid() and rentalincome_rateforms.is_valid() and model16_formset.is_valid():
            # for form in model2_formset:
            # interest_rates = [form.cleaned_data['rate'] for form in interestrate_rateforms]
            # interestrates_rates.rates = interest_rates
            # interestrates_rates.save()
            model2_formset.save()
            interestrate_rateforms.save()
            # for form in model3_formset:
            #     inlfaition_rates = [form.cleaned_data['rate'] for form in inflationrates_rateforms]
            #     inflationrates_rates.rates = inlfaition_rates
            #     inflationrates_rates.save()
            #     form.save()
            # for form in model4_formset:
            #     form.save()
            # for form in model5_formset:
            #     capitalgrowth_rates = [form.cleaned_data['rate'] for form in capitalgrowthrates_rateforms]
            #     capitalgrowthrates_rates.rates = capitalgrowth_rates
            #     capitalgrowthrates_rates.save()
            #     form.save()
            # for form in model6_formset:
            #     form.save()
            # for form in model7_formset:
            #     renovations_own = [form.cleaned_data['rate'] for form in ownrenovations_jsonforms]
            #     ownrenovations_list.rates = renovations_own
            #     ownrenovations_list.save()
            #     form.save()
            # for form in model8_formset:
            #     form.save()
            # for form in model9_formset:
            #     repairs = [form.cleaned_data['rate'] for form in repairs_rateforms]
            #     repairs_list.rates = repairs
            #     repairs_list.save()
            #     form.save()
            # for form in model10_formset:
            #     special = [form.cleaned_data['rate'] for form in special_rateforms]
            #     special_list.rates = special
            #     special_list.save()
            #     form.save()
            # for form in model11_formset:
            #     form.save()
            # for form in model12_formset:
            #     form.save()
            # for form in model13_formset:
            #     additionalpayment = [form.cleaned_data['rate'] for form in additionalpayments_rateforms]
            #     additionpayments_list.rates = additionalpayment
            #     additionalpayment.save()
            #     form.save()
            # for form in model14_formset:
            #     capitalincome = [form.cleaned_data['rate'] for form in capitalincome_rateforms]
            #     capitalincome_list.rates = capitalincome
            #     capitalincome_list.save()
            #     form.save()
            # for form in model15_formset:
            #     rentalincome = [form.cleaned_data['rate'] for form in rentalincome_rateforms]
            #     rentalincome_list.rates = rentalincome
            #     rentalincome_list.save()
            #     form.save()
            # for form in model16_formset:
            #     form.save()
    else:
        # form = EditpropertyForm(instance=property_instance)
        # model1_formset = Model1Formset(prefix='model1', form_kwargs={'instance': property_instance})
        # model2_formset = InterestRateForm(prefix='model2', form_kwargs={'instance': interestrate_instance})
        model2_formset = InterestRateForm(instance=interestrate_instance)
        interestrate_rateforms = RateFormSet(
            initial=[{"rate": rate} for rate in interestrates_rates]
        )
        # model3_formset = Model3Formset(prefix='model3', form_kwargs={'instance': property_instance})
        # inflationrates_rateforms = RateFormSet(initial=[{'rate': rate} for rate in inflationrates_rates])
        # model4_formset = Model4Formset(prefix='model4', form_kwargs={'instance': depreciation_instance})
        # model5_formset = Model5Formset(prefix='model5', form_kwargs={'instance': property_instance})
        # capitalgrowthrates_rateforms = RateFormSet(initial=[{'rate': rate} for rate in capitalgrowthrates_rates])
        # model6_formset = Model6Formset(prefix='model6', form_kwargs={'instance': property_instance})
        # model7_formset = Model7Formset(prefix='model6', form_kwargs={'instance': property_instance})
        # #ownrenovations_jsonforms = JsonFormSet(initial=[{'amount': amount, 'income': income} for amount,income in ownrenovations_list.items()])
        # ownrenovations_jsonforms = JsonFormSet(form_kwargs={'instance': ownrenovations_list})
        # model8_formset = Model8Formset(prefix='model6', form_kwargs={'instance': property_instance})
        # model8_formset = Model8Formset(prefix='model6', form_kwargs={'instance': property_instance})
        # model9_formset = Model9Formset(prefix='model6', form_kwargs={'instance': property_instance})
        # repairs_rateforms = RateFormSet(initial=[{'rate': rate} for rate in repairs_list])
        # model10_formset = Model10Formset(prefix='model6', form_kwargs={'instance': property_instance})
        # special_rateforms = RateFormSet(initial=[{'rate': rate} for rate in special_list])
        # model11_formset = Model11Formset(prefix='model11', form_kwargs={'instance': taxoptions_instance})
        # model12_formset = Model12Formset(prefix='model12', form_kwargs={'instance': managementexpenses_instance})
        # model13_formset = Model14Formset(prefix='model13', form_kwargs={'instance': property_instance})
        # additionalpayments_rateforms = RateFormSet(initial=[{'rate': rate} for rate in additionpayments_list])
        # model14_formset = Model14Formset(prefix='model14', form_kwargs={'instance': property_instance})
        # capitalincome_rateforms = RateFormSet(initial=[{'rate': rate} for rate in capitalincome_list])
        # model15_formset = Model15Formset(prefix='model15', form_kwargs={'instance': rentalincome_instance})
        # rentalincome_rateforms = RateFormSet(initial=[{'rate': rate} for rate in rentalincome_list])
        # model16_formset = Model15Formset(prefix='model16', form_kwargs={'instance': comparison_instance})

    context = {
        # 'model1_formset': model1_formset,
        "model2_formset": model2_formset,
        "interestrate_rateforms": interestrate_rateforms,
        # 'model3_formset': model3_formset,
        # 'inflationrates_rateforms': inflationrates_rateforms,
        # 'model4_formset': model4_formset,
        # 'model5_formset': model5_formset,
        # 'capitalgrowthrates_rateforms': capitalgrowthrates_rateforms,
        # 'model6_formset': model6_formset,
        # 'model7_formset': model7_formset,
        # 'ownrenovations_jsonforms' : ownrenovations_jsonforms,
        # 'model8_formset': model8_formset,
        # 'model9_formset': model9_formset,
        # 'repairs_rateforms': repairs_rateforms,
        # 'model10_formset': model10_formset,
        # 'special_rateforms': special_rateforms,
        # 'model11_formset': model11_formset,
        # 'model12_formset': model12_formset,
        # 'model13_formset': model13_formset,
        # 'additionalpayments_rateforms': additionalpayments_rateforms,
        # 'model14_formset': model14_formset,
        # 'capitalincome_rateforms': capitalincome_rateforms,
        # 'model15_formset': model15_formset,
        # 'rentalincome_rateforms': rentalincome_rateforms,
        # 'model16_formset': model16_formset,
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
    context = {"property_obj": property_obj, "images": images}
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
