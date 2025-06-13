import pytest
from src.pizza import Pizza

@pytest.fixture
def sample_pizza():
    """Returns a standard pizza used by all pizza tests."""
    return Pizza("thin", "liv_sauce", "pesto", "mozzarella", "pineapple")

@pytest.mark.pizza
def test_pizza_init(sample_pizza):
    """Tests the following for pizza __init__:
    1) Test return an initialized pizza.
    2) Test pizza should have crust (str), sauce (list[str]), cheese (str), toppings (list[str])
    3) Test pizza should return a non-zero cost
    """
    pizza = sample_pizza
    assert isinstance(pizza, Pizza)
    assert isinstance(pizza.crust, str)
    assert isinstance(pizza.sauce, list)
    assert all(isinstance(s, str) for s in pizza.sauce)
    assert isinstance(pizza.cheese, str)
    assert isinstance(pizza.toppings, list)
    assert all(isinstance(t, str) for t in pizza.toppings)
    assert pizza.cost() > 0

@pytest.mark.pizza
def test_pizza_str(sample_pizza):
    """Tests pizza __str__ returns a string containing the pizza and cost."""
    pizza = sample_pizza
    pizza_str = str(pizza)
    test_pizza = f"Crust: thin, Sauce: ['liv_sauce', 'pesto'], Cheese: mozzarella, Toppings: ['pineapple'], Cost: 14"
    assert isinstance(pizza_str, str)
    assert pizza_str == test_pizza

@pytest.mark.pizza
def test_pizza_cost(sample_pizza):
    """Test pizza cost returns correct cost for an input pizza."""
    pizza = sample_pizza
    expected = 5 + 5 + 3 + 1 # thin + liv_sauce + pesto + pineapple
    assert pizza.cost() == expected
