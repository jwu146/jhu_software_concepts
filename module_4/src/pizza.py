class Pizza:
    """
    Represents a limited-customizable pizza with unordered ingredient types: crust, sauce, cheese, and toppings.

    :ivar str crust: Select ONE crust type for the pizza (thin, thick, gluten_free).
    :ivar str sauce: Select AT LEAST ONE sauce type for the pizza (marinara, pesto, liv_sauce).
    :ivar str cheese: Select cheese type for the pizza (mozzarella).
    :ivar str toppings: Select AT LEAST ONE toppings type for the pizza (pineapple, pepperoni, mushrooms).

    Raises ValueError if required components are missing.
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
        Initializes a Pizza object from a flexible set of unordered ingredients.
        Categorizes each ingredient as a crust, sauce, cheese, or topping.
        """
        self.crust = None
        self.sauce = []
        self.cheese = None
        self.toppings = []

        for ing in ingredients:
            ing_str = str(ing)
            if ing_str in self.CRUST_COST and self.crust is None:
                self.crust = ing_str
            elif ing_str in self.CRUST_COST and self.crust is not None:
                raise ValueError(f"Multiple crusts selected: {self.crust} and {ing_str}. Please select only one crust.")
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
        return int(total)
