from model_objects import Offer
from receipt import Receipt


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        [self._add_to(receipt, item) for item in the_cart.items]
        the_cart.handle_offers(receipt, self.offers, self.catalog)
        return receipt
    
    def _add_to(self, receipt, item):
        product = item.product
        quantity = item.quantity
        unit_price = self.catalog.unit_price(product)
        price = quantity * unit_price
        receipt.add_product(product, quantity, unit_price, price)
        return receipt
