
class ReceiptItem:
    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class Receipt:
    def __init__(self):
        self._items = []
        self._discounts = []

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]

    def total_price(self):
        total = 0
        total += sum(item.total_price for item in self.items)
        total += sum(discount.discount_amount for discount in self.discounts)
        return total

    def add_product(self, product, quantity, price, total_price):
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount):
        self._discounts.append(discount)
