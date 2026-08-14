import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected
    
def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(10, 10) == 0
    assert subtract(-1, 1) == -2

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(0, 5) == 0
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
    assert divide(-6, 2) == -3

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
        
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100
    
def test_bankdefault_amount(zero_bank_account):
    assert zero_bank_account.balance == 0  
    
def test_withdraw(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 50
    
def test_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 150
    
def test_collect_interest(bank_account):
    bank_account.collect_interest(0.05)  # 5% interest
    assert round(bank_account.balance, 2) == 105.0


@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (200, 100, 100),
    (700, 100, 600),
    (1200, 400, 800),
])
    
def test_bank_transactions(zero_bank_account, deposited, withdrawn, expected):
    account = zero_bank_account
    account.deposit(deposited)
    account.withdraw(withdrawn)
    assert account.balance == expected