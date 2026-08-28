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
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient funds")
        self.balance -= amount

    def collect_interest(self, rate=0.01):
        """Add interest to the account based on current balance."""
        if rate < 0:
            raise ValueError("Interest rate cannot be negative")
        interest = self.balance * rate
        self.balance += interest
        return self.balance
