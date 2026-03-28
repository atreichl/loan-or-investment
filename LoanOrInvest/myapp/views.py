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
    total_loan_cost_payoff = ""
    total_investment_earnings_payoff = ""
    total_investment_earnings_invest = ""
    total_loan_cost_invest = ""
    combined_savings_and_earnings = ""

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

            # find blended interest
            if total_loan_value != 0:
                blended_interest = blended_interest / total_loan_value

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

            # format outputs for web page
            # info from paying off loan first
            total_loan_cost_payoff = f'${loan_payoff_info_1[0]:.2f}'
            loan_payoff_saving = f"${payoff_loan_first:.2f}"
            loan_payoff_investment_earnings = f"${invest_info_1[0]:.2f}"
            total_investment_earnings_payoff = f"${invest_info_1[1]:.2f}"
            combined_savings_and_earnings = f"${payoff_loan_first + invest_info_1[0]:.2f}"

            # info for investing during loan.
            invest_loan_cost = f"${invest_info_base[1] - invest_loan_base_cost - invest_info_base[2]:.2f}"
            total_investment_earnings_invest = f"${invest_info_base[1]:.2f}"
            total_loan_cost_invest = f'${loan_info_base[0]:.2f}'

    return render(request, 'home.html', context={'form': form,
                                                 'formset': loan_info_forms,
                                                 'total_loan_cost_payoff': total_loan_cost_payoff,
                                                 'loan_payoff_saving': loan_payoff_saving,
                                                 'loan_payoff_investment_earnings': loan_payoff_investment_earnings,
                                                 'total_investment_earnings_payoff': total_investment_earnings_payoff,
                                                 'total_investment_earnings_invest': total_investment_earnings_invest,
                                                 'total_loan_cost_invest': total_loan_cost_invest,
                                                 'combined_savings_and_earnings': combined_savings_and_earnings,
                                                 'invest_loan_cost': invest_loan_cost})
