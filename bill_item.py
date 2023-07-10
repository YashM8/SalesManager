class Item:
    def __init__(self, name, quantity, cost):
        self.name = name
        self.quantity = quantity
        self.cost = cost

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def get_cost(self):
        return self.cost
