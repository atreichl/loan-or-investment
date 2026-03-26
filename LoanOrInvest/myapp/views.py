from django.forms.formsets import formset_factory
from django.shortcuts import render

from .forms import PayOrInvestForm, LoanInfoForm

from .functions import total_loan_payment, investment_return
from decimal import *

# Create your views here.
def index(request):
    form = PayOrInvestForm()
    loan_info_forms = formset_factory(LoanInfoForm, extra=1)
    loan_payoff_cost = ""
    invest_loan_cost = ""
    if request.method == 'POST':
        form = PayOrInvestForm(request.POST)
        formset = loan_info_forms(request.POST)
        if form.is_valid() and formset.is_valid():
            time_period_months = form.cleaned_data['time_period_years'] * 12
            #loan_amount = form.cleaned_data['loan_amount']
            #loan_payment = form.cleaned_data['loan_payment']
            #loan_interest_annual = form.cleaned_data['loan_interest_annual']
            invest_return = form.cleaned_data['invest_return']
            flex_amount = form.cleaned_data['flex_amount']

            for loan_info in formset:
                loan_amount = loan_info.cleaned_data['loan_amount']
                loan_payment = loan_info.cleaned_data['loan_payment']
                loan_interest_annual = loan_info.cleaned_data['loan_interest_annual']

            loan_info_forms = formset

            #print(time_period_years)
            #print(loan_amount)
            #print(loan_payment)
            #print(loan_interest_annual)
            #print(invest_return)
            #print(flex_amount)

            #find info for base laon payment amount
            loan_info_base = total_loan_payment(loan_payment, loan_interest_annual, loan_amount)

            #find the investment return for base loan payment, shift loan payment to investment once loan paid off
            invest_info_base = investment_return(flex_amount,invest_return,loan_info_base[1], 0)
            invest_info_base = investment_return(flex_amount + loan_payment, invest_return, time_period_months - loan_info_base[1], invest_info_base[1])

            #finds info for loan while adding extra payment
            loan_payoff_info_1 = total_loan_payment(loan_payment + flex_amount, loan_interest_annual, loan_amount)
            #find invest for only investing after paying off the loon
            invest_info_1 = investment_return(loan_payment + flex_amount, invest_return, time_period_months - loan_payoff_info_1[1], 0)

            #finds the amount saved by paying off the loan faster
            payoff_loan_first = loan_info_base[0] - loan_payoff_info_1[0]
            #adds the amount made from investing after
            payoff_loan_first += invest_info_1[0]

            loan_payoff_cost = f"{payoff_loan_first:.2f}"
            invest_loan_cost = f"{invest_info_base[0]:.2f}"

    return render(request, 'home.html', context={'form': form,
                                                 'formset': loan_info_forms,
                                                 'loan_payoff_cost': loan_payoff_cost,
                                                 'invest_loan_cost': invest_loan_cost})
