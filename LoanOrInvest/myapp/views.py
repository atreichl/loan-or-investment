from django.forms.formsets import formset_factory
from django.shortcuts import render

from .forms import PayOrInvestForm, LoanInfoForm

from .functions import total_loan_payment, investment_return
from decimal import *

# Create your views here.
def index(request):
    form = PayOrInvestForm()
    loan_info_forms = formset_factory(LoanInfoForm, extra=1)
    loan_payoff_saving = ""
    loan_payoff_investment_earnings = ""
    invest_loan_cost = ""

    if request.method == 'POST':
        form = PayOrInvestForm(request.POST)
        formset = loan_info_forms(request.POST)
        if form.is_valid() and formset.is_valid():
            time_period_months = form.cleaned_data['time_period_years'] * 12
            invest_return = form.cleaned_data['invest_return']
            flex_amount = form.cleaned_data['flex_amount']
            loan_payment_rollover = form.cleaned_data['loan_payment_rollover'] / 100
            #print(loan_payment_rollover)

            total_pay_loan = Decimal(0.00)
            total_loan_value = Decimal(0.00)
            blended_interest = Decimal(0.00)

            for loan_info in formset:
                if loan_info.has_changed():
                    #print(loan_info.cleaned_data)
                    total_loan_value += Decimal(loan_info.cleaned_data['loan_amount'])
                    total_pay_loan += Decimal(loan_info.cleaned_data['loan_payment'])
                    blended_interest += loan_info.cleaned_data['loan_amount'] * (loan_info.cleaned_data['loan_interest_annual'] /100)

            loan_info_forms = formset

            #print(f'total loan value: {total_loan_value:.2f}')
            #print(f'blended interest: {blended_interest:.2f}')
            #print(f'total_pay_loan: {total_pay_loan:.2f}')

            # find blended interest
            if total_loan_value != 0:
                blended_interest = blended_interest / total_loan_value
                #print(blended_interest)
                #print(total_loan_value)
                #print(total_pay_loan)

            #print(f'blended_interest: {blended_interest:.2f}')

            #print(time_period_years)
            #print(loan_amount)
            #print(loan_payment)
            #print(loan_interest_annual)
            #print(invest_return)
            #print(flex_amount)

            #find info for base laon payment amount
            loan_info_base = total_loan_payment(total_pay_loan, blended_interest, total_loan_value)


            #find the investment return for base loan payment, shift loan payment to investment once loan paid off
            invest_info_base = investment_return(flex_amount, invest_return, loan_info_base[1], 0)
            invest_loan_base_cost = invest_info_base[2]
            invest_info_base = investment_return(flex_amount + (total_pay_loan * loan_payment_rollover), invest_return, time_period_months - loan_info_base[1], invest_info_base[1])

            #finds info for loan while adding extra payment
            loan_payoff_info_1 = total_loan_payment(total_pay_loan + flex_amount, blended_interest, total_loan_value)
            #find invest for only investing after paying off the loon
            invest_info_1 = investment_return((total_pay_loan * loan_payment_rollover) + flex_amount, invest_return, time_period_months - loan_payoff_info_1[1], 0)

            #finds the amount saved by paying off the loan faster
            payoff_loan_first = loan_info_base[0] - loan_payoff_info_1[0]
            #print(f'base loan cost: {loan_info_base[0]:.2f}')
            #print(f'fast loan payoff cost: {loan_payoff_info_1[0]:.2f}')
            #adds the amount made from investing after
            #payoff_loan_first += invest_info_1[0]

            # format outputs for web page
            # info from paying off loan first
            loan_payoff_saving = f"${payoff_loan_first:.2f}"
            loan_payoff_investment_earnings = f"${invest_info_1[0]:.2f}"

            #print(invest_info_base[1])
            #print(invest_loan_base_cost)
            #print(invest_info_1[2])

            invest_loan_cost = f"{invest_info_base[1] - invest_loan_base_cost - invest_info_base[2]:.2f}"

    return render(request, 'home.html', context={'form': form,
                                                 'formset': loan_info_forms,
                                                 'loan_payoff_saving': loan_payoff_saving,
                                                 'loan_payoff_investment_earnings': loan_payoff_investment_earnings,
                                                 'invest_loan_cost': invest_loan_cost})
