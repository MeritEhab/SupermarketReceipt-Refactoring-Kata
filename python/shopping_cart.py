from model_objects import ProductQuantity, SpecialOfferType
import discount_strategies as strategies

class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_qty = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        self._product_qty[product] = self._product_qty.get(product, 0.0) + quantity

    def apply_offers(self, receipt, offers, catalog):
        OfferHandler(self._product_qty, catalog).handle(receipt, offers)


class OfferHandler:
    def __init__(self, products, catalog):
        self.products = products
        self.catalog = catalog
        self._strategies = self._register_offer_strategies()

    def handle(self, receipt, offers):
        for product_name, quantity in self.products.items():
            if product_name not in offers: continue 
            offer = offers.get(product_name)
            product = Product(product_name, quantity, self.catalog)
            strategy = self._strategies.get(offer.offer_type)
            if strategy: discount = strategy._calculate_discount(product, offer)
            if discount: receipt.add_discount(discount)
    
    def _register_offer_strategies(self):
        return {
            SpecialOfferType.PERCENT_DISCOUNT: strategies.PercentDiscountStrategy(),
            SpecialOfferType.THREE_FOR_TWO: strategies.AForBStrategy(buy=3, pay=2),
            SpecialOfferType.TWO_FOR_AMOUNT: strategies.NForAmountStrategy(pack_size=2),
            SpecialOfferType.FIVE_FOR_AMOUNT: strategies.NForAmountStrategy(pack_size=5),
            SpecialOfferType.BUNDLE_DISCOUNT: strategies.BundleStrategy(self.products, self.catalog)
        }


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

