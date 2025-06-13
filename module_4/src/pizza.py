class Pizza:
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
        Allows flexible input: Pizza("thin", "liv_sauce", "pesto", "mozzarella", "mushrooms", "pepperoni")
        Categorizes ingredients into crust, sauces, cheese, toppings and initializes pizza object.
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
        """Returns string of the pizza and the cost."""
        return (f"Crust: {self.crust}, Sauce: {self.sauce}, Cheese: {self.cheese}, Toppings: {self.toppings}, "
                f"Cost: {self.cost()}")

    def cost(self) -> int:
        """Calculates the cost of the pizza."""
        total = 0
        total += self.CRUST_COST.get(self.crust, 0)
        total += sum(self.SAUCE_COST.get(s, 0) for s in self.sauce)
        total += self.CHEESE_COST
        total += sum(self.TOPPING_COST.get(t, 0) for t in self.toppings)
        return total
