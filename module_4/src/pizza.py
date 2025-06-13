class Pizza:
    """
    Represents a customizable pizza with crust, sauce, cheese, and toppings.

    :cvar dict CRUST_COST: Cost associated with each crust type.
    :cvar dict SAUCE_COST: Cost associated with each sauce.
    :cvar dict TOPPING_COST: Cost associated with each topping.
    :cvar str CHEESE: Default cheese type.
    :cvar int CHEESE_COST: Cost for cheese (included by default).
    :ivar str crust: Selected crust type for the pizza.
    :ivar list sauce: List of selected sauces.
    :ivar str cheese: Selected cheese (defaults to mozzarella).
    :ivar list toppings: List of selected toppings.
    """

    CRUST_COST = {
        "thin": 5,
        "thick": 6,
        "gluten_free": 8,
    }
    SAUCE_COST = {
        "marinara": 2,
        "pesto": 3,
        "liv_sauce": 5,
    }
    TOPPING_COST = {
        "pineapple": 1,
        "pepperoni": 2,
        "mushrooms": 3,
    }
    CHEESE = "mozzarella"
    CHEESE_COST = 0  # Included and is free

    def __init__(self, *ingredients):
        """
        Initializes a Pizza object from a flexible set of ingredients.

        Categorizes each ingredient as a crust, sauce, cheese, or topping.
        Raises ValueError if required components are missing.

        :param ingredients: Variable number of strings representing ingredients.
        :type ingredients: str
        :raises ValueError: If any required pizza component is missing.
        """
        self.crust = None
        self.sauce = []
        self.cheese = None
        self.toppings = []

        for ing in ingredients:
            ing_str = str(ing)
            if ing_str in self.CRUST_COST and self.crust is None:
                self.crust = ing_str
            elif ing_str in self.SAUCE_COST:
                self.sauce.append(ing_str)
            elif ing_str == self.CHEESE:
                self.cheese = ing_str
            elif ing_str in self.TOPPING_COST:
                self.toppings.append(ing_str)

        # Defaults and checks
        if self.cheese is None:
            self.cheese = self.CHEESE
        if not self.sauce:
            raise ValueError("At least one valid sauce is required")
        if not self.toppings:
            raise ValueError("At least one valid topping is required")
        if self.crust is None:
            raise ValueError("A valid crust is required")

    def __str__(self):
        """
        Returns a string representation of the pizza, including the cost.

        :return: Description of the pizza and its total cost.
        :rtype: str
        """
        return (f"Crust: {self.crust}, Sauce: {self.sauce}, Cheese: {self.cheese}, Toppings: {self.toppings}, "
                f"Cost: {self.cost()}")

    def cost(self) -> int:
        """
        Calculates the cost of the pizza based on selected options.

        :return: The total cost of the pizza.
        :rtype: int
        """
        total = 0
        total += self.CRUST_COST.get(self.crust, 0)
        total += sum(self.SAUCE_COST.get(s, 0) for s in self.sauce)
        total += self.CHEESE_COST
        total += sum(self.TOPPING_COST.get(t, 0) for t in self.toppings)
        return total
