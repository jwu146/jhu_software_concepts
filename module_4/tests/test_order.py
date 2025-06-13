import pytest
from src.order import Order

@pytest.mark.order
def test_order_init():
    """Test order initialization."""
    order = Order()
    assert order.pizzas == []
    assert order.cost == 0
    assert order.paid is False

@pytest.mark.order
def test_order_str():
    """Test string representation of order with and without pizzas."""
    order = Order()
    order_str = str(order)
    test_str = "No pizzas in this order."
    assert order_str == test_str
    
    order.input_pizza("thin", "liv_sauce", "pesto", "mozzarella", "pineapple")
    order.input_pizza("gluten_free", "marinara", "mozzarella", "mushrooms", "pepperoni")
    order_str = str(order)
    test_str = (f"Customer Requested:\n"
                f"Crust: thin, Sauce: ['liv_sauce', 'pesto'], Cheese: mozzarella, Toppings: ['pineapple'], Cost: 14\n"
                f"Crust: gluten_free, Sauce: ['marinara'], Cheese: mozzarella, Toppings: ['mushrooms', 'pepperoni'], Cost: 15\n")
    assert order_str == test_str

@pytest.mark.order
def test_order_input_pizza_and_cost():
    """Test input_pizza() updates cost correctly."""
    order = Order()
    order.input_pizza("thin", "liv_sauce", "pesto", "mozzarella", "pineapple")
    assert len(order.pizzas) == 1
    expected = 5 + 5 + 3 + 1 # thin + liv_sauce + pesto + pineapple
    assert order.cost == expected

@pytest.mark.order
def test_order_paid():
    """Test order_paid() marks the order as paid."""
    order = Order()
    assert not order.paid
    order.order_paid()
    assert order.paid
