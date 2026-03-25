from django.shortcuts import render

from .forms import PayOrInvestForm

from .functions import total_loan_payment, investment_return
from decimal import *

# Create your views here.
def index(request):
    form = PayOrInvestForm()
    loan_payoff_cost = ""
    invest_loan_cost =0.0
    if request.method == 'POST':
        form = PayOrInvestForm(request.POST)
        if form.is_valid():
            time_period_years = form.cleaned_data['time_period_years']
            loan_time = form.cleaned_data['loan_time']
            loan_amount = form.cleaned_data['loan_amount']
            loan_payment = form.cleaned_data['loan_payment']
            loan_interest_annual = form.cleaned_data['loan_interest_annual']
            invest_return = form.cleaned_data['invest_return']
            flex_amount = form.cleaned_data['flex_amount']

            #print(time_period_years)
            #print(loan_time)
            #print(loan_amount)
            #print(loan_payment)
            #print(loan_interest_annual)
            #print(invest_return)
            #print(flex_amount)

            loan_payoff_info_1 = total_loan_payment(loan_payment + flex_amount, loan_interest_annual, loan_amount)
            invest_info_1 = investment_return(flex_amount,invest_return,loan_payoff_info_1[1])

            for x in loan_payoff_info_1:
                print(x)

            loan_payoff_cost = f"{loan_payoff_info_1[0]:.2f}"
            invest_loan_cost = f"{invest_info_1:.2f}"

    return render(request, 'home.html', context={'form': form,'loan_payoff_cost': loan_payoff_cost, 'invest_loan_cost': invest_loan_cost})