import pytest
from src.order import Order

@pytest.mark.order
@pytest.mark.pizza
def test_multiple_pizzas():
    """Test multiple pizzas within a given order results in additively larger cost."""
    order = Order()
    order.input_pizza("thin", "liv_sauce", "pesto", "mozzarella", "pineapple")
    assert len(order.pizzas) == 1
    expected = 5 + 5 + 3 + 1 # thin + liv_sauce + pesto + pineapple
    assert order.cost == expected
    
    order.input_pizza("gluten_free", "marinara", "mozzarella", "mushrooms", "pepperoni")
    expected2 = 8 + 2 + 3 + 2 # gluten_free + marinara + mushrooms + pepperoni
    assert len(order.pizzas) == 2
    assert order.cost == expected + expected2
    
    order.input_pizza("thick", "marinara", "mozzarella", "mushrooms", "pineapple")
    expected3 = 6 + 2 + 3 + 1 # gluten_free + marinara + mushrooms + pepperoni
    assert len(order.pizzas) == 3
    assert order.cost == expected + expected2 + expected3