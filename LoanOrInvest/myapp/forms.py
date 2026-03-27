from django import forms


class PayOrInvestForm(forms.Form):
    time_period_years = forms.IntegerField(min_value = 0, max_value = 60)
    #loan_amount = forms.DecimalField(decimal_places=2, min_value=0.0)
    #loan_payment = forms.DecimalField(decimal_places=2, min_value=0.0)
    #loan_interest_annual = forms.DecimalField(decimal_places=2, min_value=0.0)
    invest_return = forms.DecimalField(decimal_places=2, min_value=0.0)
    flex_amount = forms.DecimalField(decimal_places=2, min_value=0.0)

class LoanInfoForm(forms.Form):
    loan_amount = forms.DecimalField(decimal_places=2, min_value=0.0, required= True)
    loan_payment = forms.DecimalField(decimal_places=2, min_value=0.0)
    loan_interest_annual = forms.DecimalField(decimal_places=2, min_value=0.0)