import pytest
from app.calculations import add, subtract, multiply, divide

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
]
    
)
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