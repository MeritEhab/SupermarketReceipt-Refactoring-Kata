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

class BundleStrategy:
    def __init__(self, products, catalog):
        self.products = products
        self.catalog = catalog
    
    def _calculate_discount(self, product, offer):
        bundle_items = offer.argument
        bundle_name = (f"{product} " for product in bundle_items.keys())
        complete_bundles = self._count_complete_bundles(bundle_items)
        if not complete_bundles: return
        single_bundle_price = sum(self.catalog.unit_price(product) * required_qty for product, required_qty in bundle_items.items())
        discount_amount = (single_bundle_price * complete_bundles) * (10 / 100.0)
        return Discount(bundle_name, "Bundle 10% off", -discount_amount)
    
    def _count_complete_bundles(self, bundle_items):
        item_appearance = []
        for bundle_item, bundle_item_qty in bundle_items.items():
            cart_quantity = self.products.get(bundle_item, 0)
            if bundle_item_qty > 0:
                item_appearance.append(cart_quantity // bundle_item_qty)
            else:
                item_appearance.append(0)
        if not item_appearance: return
        complete_bundles = min(item_appearance)
        return complete_bundles