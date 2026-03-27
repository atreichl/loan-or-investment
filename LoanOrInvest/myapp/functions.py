from decimal import *

#finds the total amount paid for a loan based of a repayment amount
#also returns the time in months it takes to repay and any extra from tth last payment.
#return [total_paid, length_month, last_payment_extra]
def total_loan_payment(payment, loan_interest_annual, loan_amount):
    length_month = 0;
    total_paid = Decimal(0.00)
    monthly_interest = Decimal((loan_interest_annual / 12))
    output = []

    #print(f'payment: {payment:.2f}')
    #print(f'monthly interest: {monthly_interest}')
    #print(f'loan amount: {loan_amount}')

    while loan_amount > 0 and length_month < 100*12:
        loan_amount += loan_amount * monthly_interest
        loan_amount -= payment
        length_month += 1
        total_paid += payment
        #print(f'left: {loan_amount}')
        #print(f'paid: {total_paid}')
        #print(f'month: {length_month}')
        #print("\n")

    #print(f'loan amount: {loan_amount:.2f}')
    #print(f'total paid: {total_paid:.2f}')

    if loan_amount < 0:
        total_paid += loan_amount
        loan_amount = loan_amount * -1
        #print(f'paid amount: {total_paid}')

    #print(f'loan amount: {loan_amount:.2f}')
    #print(f'total paid: {total_paid:.2f}')

    output.append(total_paid)
    output.append(length_month)
    output.append(loan_amount)

    return output

#finds invest amount for a monthly payment and a number of months.
#intrest is compounded monthly.
#returns [interest, total, paid]
def investment_return(payment, invest_return_annual, num_months, investment):
    paid = 0
    num_months = int(num_months)
    #print(f'months: {num_months}')
    investment_return_monthly = Decimal((invest_return_annual / 12) / 100)
    output = []
    #print(f'payment: {payment:.2f}')

    for i in range(num_months):
        #print(f'month: {i}')
        investment += investment * investment_return_monthly
        #print(f'investment after interest: {investment:.2f}')
        investment += payment
        #print(f'investment after deposit: {investment:.2f}')
        paid += payment
        #print(f'total deposit: {paid:.2f}')
        #print('\n')

    #print(f"total investment: {investment:.2f}")
    interest = investment - paid
    #print(f'investment: {investment}')
    #print(f'paid: {paid}')
    #print(f'interest: {interest}')

    output.append(interest)
    output.append(investment)
    output.append(paid)

    return output