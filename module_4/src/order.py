from src.pizza import Pizza

class Order:
    """
    A class to place a pizza order by a customer.
    """

    def __init__(self):
        """
        Initializes an empty order.
        """
        self.pizzas = []
        self.cost = 0
        self.paid = False

    def __str__(self):
        """
        Returns a string showing the customer's complete order.
        """
        if not self.pizzas:
            pizzas_str = "No pizzas in this order."
            return pizzas_str
        else:
            pizzas_str = "\n".join(str(pizza) for pizza in self.pizzas)
            return (
                f"Customer Requested:\n"
                f"{pizzas_str}\n"
            )

    def input_pizza(self, *ingredients):
        """
        Adds a pizza to the order, categorizing ingredients automatically.

        :param ingredients: Ingredients for the Pizza (order doesn't matter). See Pizza class for ingredient details.
        :type ingredients: str
        """
        pizza = Pizza(*ingredients)
        self.pizzas.append(pizza)
        self.cost += pizza.cost()

    def order_paid(self):
        """
        Marks the order as paid.
        """
        self.paid = True
