from model_objects import  Discount

class PercentDiscountStrategy:
        def _calculate_discount(self, product, offer):
            discount_amount = -product.quantity * product.unit_price * (offer.argument / 100.0)
            return Discount(product.name, f"{offer.argument} % off", discount_amount)

    
class AForBStrategy:
    def __init__(self, buy, pay):
        self.buy = buy
        self.pay = pay

    def _calculate_discount(self, product, offer):
        offer_price = self.pay * product.unit_price
        packs = product.int_quantity // self.buy
        remaining_items = product.int_quantity % self.buy
        discount_amount = packs * offer_price + remaining_items * product.unit_price
        total_discount = (product.int_quantity * product.unit_price) - discount_amount
        return Discount(product.name, f"{self.buy} for {offer_price}", -total_discount)


class NForAmountStrategy:
    def __init__(self, pack_size):
        self.pack_size = pack_size
    
    def _calculate_discount(self, product, offer):
        packs = product.int_quantity // self.pack_size
        remaining_items = product.int_quantity % self.pack_size
        discount_amount = packs * offer.argument + remaining_items * product.unit_price
        total_discount = (product.int_quantity * product.unit_price) - discount_amount
        return Discount(product.name, f"{self.pack_size} for {offer.argument}", -total_discount)

