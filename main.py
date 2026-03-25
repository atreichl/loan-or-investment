import matplotlib.pyplot as plt

months = 60
startAmount = 10000
loanInterest = 10
loanPayment = 212.47
monthlyInterest = loanInterest/12
investment_return = 10
investment_return_monthly = (investment_return/12)/100
flex_spending = 100


def total_loan_payment(payment):
    month_count = 0;
    amount = startAmount
    total_payed = 0.0

    while amount > 0.1:
        amount += amount * (monthlyInterest / 100)
        amount -= payment
        month_count += 1
        total_payed += payment
        print(f'left: {amount}')
        print(f'payed: {total_payed}')
        print("\n")

    return total_payed
    print(month_count)

#finds invest amount for a monthly payment and a number of months.
#intres is compounded monthly.
def investment_return(payment, num_months):
    amount = 0
    paid = 0

    for i in range(num_months):
        amount += amount * investment_return_monthly
        amount += payment
        paid += payment

    interest = amount - paid
    print(f'investment: {amount}')
    print(f'paid: {paid}')
    print(f'interest: {interest}')

    return interest

if __name__ == '__main__':
    #total_loan_payment(212.47)
    investment_return(100, 60)
