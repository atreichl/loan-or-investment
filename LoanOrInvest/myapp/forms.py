from django import forms

class PayOrInvestForm(forms.Form):
    time_period_years = forms.IntegerField(min_value = 0, max_value = 60)
    loan_amount = forms.FloatField()
    loan_payment = forms.FloatField()
    loan_interest_annual = forms.FloatField()
    invest_return = forms.FloatField()
    flex_amount = forms.FloatField()