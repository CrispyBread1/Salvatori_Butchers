class Product:
    def __init__(self, name, cost, stock_count, product_value, stock_category, sold_as):
        self.name = name
        self.cost = cost
        self.stock_count = stock_count
        self.product_value = product_value
        self.stock_category = stock_category
        self.sold_as = sold_as

    def total_profit(self):
        return self.stock_count * self.product_value
    
    def total_product_cost(self):
        return self.stock_count * self.cost
