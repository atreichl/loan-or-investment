from django.shortcuts import render

from .forms import PayOrInvestForm


# Create your views here.
def index(request):
    form = PayOrInvestForm()
    if request.method == 'POST':
        form = PayOrInvestForm(request.POST)
        if form.is_valid():
            time_period_years = form.cleaned_data['time_period_years']
            loan_amount = form.cleaned_data['loan_amount']
            loan_payment = form.cleaned_data['loan_payment']
            loan_interest_annual = form.cleaned_data['loan_interest_annual']
            invest_return = form.cleaned_data['invest_return']
            flex_amount = form.cleaned_data['flex_amount']

            print(time_period_years)
            print(loan_amount)
            print(loan_payment)
            print(loan_interest_annual)
            print(invest_return)
            print(flex_amount)

    return render(request, 'home.html', context={'form': form})