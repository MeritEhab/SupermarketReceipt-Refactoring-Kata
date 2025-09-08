import math

from model_objects import ProductQuantity, SpecialOfferType, Discount


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        for product, quantity in self._product_quantities.items():
            if self._product_has_offer(product, offers):
                offer = offers[product]
                product_obj = Product(product, quantity, catalog)
                discount = None
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and product_obj.int_quantity > 2:
                    offer.argument = 2 * product_obj.unit_price
                    discount = self._calc_n_packs_for_amount(3, product_obj, offer)

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT and product_obj.int_quantity >= 2:
                        discount = self._calc_n_packs_for_amount(2, product_obj, offer)

                if offer.offer_type == SpecialOfferType.PERCENT_DISCOUNT:
                    discount = self._calc_percentage_discount_offer(product_obj, offer)

                if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT and product_obj.int_quantity >= 5:
                    discount = self._calc_n_packs_for_amount(5, product_obj, offer)
                    
                if discount:
                    receipt.add_discount(discount)
    
    def _product_has_offer(self, product, offers):
        return product in offers.keys()

    def _calc_percentage_discount_offer(self, product, offer):
        return Discount(product.name, str(offer.argument) + "% off",
                                        -product.quantity * product.unit_price * offer.argument / 100.0)
    def _calc_n_packs_for_amount(self, pack, product, offer):
        number_of_packs = product.int_quantity // pack
        remaining_items = product.int_quantity % pack
        price_after_discount = number_of_packs * offer.argument + remaining_items * product.unit_price
        total_discount = (product.int_quantity * product.unit_price) - price_after_discount
        return Discount(product.name, f"{pack} for {offer.argument}", -total_discount)


class Product:
    def __init__(self, name, quantity, catalog):
        self.name = name
        self.quantity = quantity
        self.catalog = catalog
    
    @property
    def unit_price(self):
        return self.catalog.unit_price(self.name)
    
    @property
    def int_quantity(self):
        return int(self.quantity)

