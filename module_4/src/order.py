from .pizza import Pizza

class Order:
    """
    Represents a pizza order by a customer.

    :ivar pizzas: List of Pizza objects in the order.
    :vartype pizzas: list of Pizza
    :ivar cost: Total cost of the order.
    :vartype cost: float
    :ivar paid: Whether the order has been paid.
    :vartype paid: bool
    """

    def __init__(self):
        """
        Initializes an empty order.

        Sets up an empty list of pizzas, initializes the cost to zero,
        and marks the order as unpaid.
        """
        self.pizzas = []
        self.cost = 0
        self.paid = False

    def __str__(self):
        """
        Returns a string showing the customer's complete order.

        :return: A formatted string representing all pizzas in the order.
            If the order is empty, indicates no pizzas in the order.
        :rtype: str
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

        :param ingredients: Ingredients for the Pizza (order doesn't matter).
        :type ingredients: str
        :return: None
        """
        pizza = Pizza(*ingredients)
        self.pizzas.append(pizza)
        self.cost += pizza.cost()

    def order_paid(self):
        """
        Marks the order as paid.

        Sets the 'paid' attribute to True.

        :return: None
        """
        self.paid = True
