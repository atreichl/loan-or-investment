
months = 60
startAmount = 10000
loanInterest = 10
loanPayment = 212.47
monthlyInterest = loanInterest/12


def totalLoanPayment(payment):
    monthCount = 0;
    amount = startAmount
    totalPayed = 0.0

    while amount > 0.1:
        amount += amount * (monthlyInterest / 100)
        amount -= payment
        monthCount += 1
        totalPayed += payment
        print(f'left: {amount}')
        print(f'payed: {totalPayed}')
        print("\n")

    print(monthCount)


if __name__ == '__main__':
    totalLoanPayment(212.47)
