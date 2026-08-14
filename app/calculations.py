def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class BankAccount:
    def __init__(self, starting_balance=0):
        """Initialize the bank account with a starting balance."""
        if starting_balance < 0:
            raise ValueError("Starting balance cannot be negative")
        self.balance = starting_balance

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount < 0:
            raise ValueError("Cannot deposit negative amount")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if amount < 0:
            raise ValueError("Cannot withdraw negative amount")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def collect_interest(self, rate=0.01):
        """Add interest to the account based on current balance."""
        if rate < 0:
            raise ValueError("Interest rate cannot be negative")
        interest = self.balance * rate
        self.balance += interest
        return self.balance
    
def test_bank_transactions():
    account = BankAccount(100)
    assert account.deposit(50) == 150
    assert account.withdraw(30) == 120
    assert account.collect_interest(0.05) == 126
    try:
        account.withdraw(200)
    except ValueError as e:
        assert str(e) == "Insufficient funds"
    try:
        account.deposit(-10)
    except ValueError as e:
        assert str(e) == "Cannot deposit negative amount"
    try:
        account.withdraw(-20)
    except ValueError as e:
        assert str(e) == "Cannot withdraw negative amount"