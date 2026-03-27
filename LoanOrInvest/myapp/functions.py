from decimal import *

#finds the total amount paid for a loan based of a repayment amount
#also returns the time in months it takes to repay and any extra from tth last payment.
#return [total_paid, length_month, last_payment_extra]
def total_loan_payment(payment, loan_interest_annual, loan_amount):
    length_month = 0;
    total_paid = Decimal(0.00)
    monthly_interest = Decimal((loan_interest_annual / 12) / 100)
    output = []

    while loan_amount > 0 and length_month < 100*12:
        loan_amount += loan_amount * monthly_interest
        loan_amount -= payment
        length_month += 1
        total_paid += payment
        #print(f'left: {loan_amount}')
        #print(f'payed: {total_paid}')
        #print("\n")

    if loan_amount < 0:
        total_paid += loan_amount
        loan_amount = loan_amount * -1
        #print(f'paid amount: {total_paid}')

    output.append(total_paid)
    output.append(length_month)
    output.append(loan_amount)

    return output

#finds invest amount for a monthly payment and a number of months.
#intrest is compounded monthly.
#returns [interest, total]
def investment_return(payment, num_months, invest_return_annual, investment):
    paid = 0
    num_months = int(num_months)
    investment_return_monthly = Decimal((invest_return_annual / 12) / 100)
    output = []

    for i in range(num_months):
        investment += investment * investment_return_monthly
        investment += payment
        paid += payment

    interest = investment - paid
    #print(f'investment: {investment}')
    #print(f'paid: {paid}')
    #print(f'interest: {interest}')

    output.append(interest)
    output.append(investment)

    return output