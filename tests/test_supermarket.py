import unittest
from assertpy import assert_that

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


class TestSupermarket(unittest.TestCase):
    def setUp(self):
        self.catalog = self.make_catalog()
        self.teller = Teller(self.catalog)
        self.cart = ShoppingCart()

    def test_empty_cart_costs_nothing(self):
        self.given_cart_with(None, 0)
        self.expect_receipt_properties(0, 0, 0)

    def test_no_offers(self):
        self.given_cart_with(self.apples, 2.5)
        self.expect_receipt_properties(4.975, 0, 1)
        self.expect_receipt_item_properties(self.receipt.items[0], self.apples, 1.99, 2.5 * 1.99, 2.5)

    def test_percent_discount(self):
        self.teller.add_special_offer(SpecialOfferType.PERCENT_DISCOUNT, self.toothbrush, 10.0)
        self.given_cart_with(self.toothbrush, 3)
        self.expect_receipt_properties(2.673, 1, 1)
        self.expect_receipt_item_properties(self.receipt.items[0], self.toothbrush, 0.99, 3 * 0.99, 3)

        self.teller.add_special_offer(SpecialOfferType.PERCENT_DISCOUNT, self.apples, 30.0)
        self.given_cart_with(self.apples, 5)
        self.expect_receipt_properties(9.637, 2, 2)
        self.expect_receipt_item_properties(self.receipt.items[1], self.apples, 1.99, 5 * 1.99, 5)
    
    def test_three_for_two_offer(self):
        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.milk, 0)
        self.given_cart_with(self.milk, 5)
        self.expect_receipt_properties(12.0, 1, 1)
        self.expect_receipt_item_properties(self.receipt.items[0], self.milk, 3.0, 5 * 3.0, 5)
    
    def test_two_for_amount_offer(self):
        self.teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, self.yogurt, 2.0)
        self.given_cart_with(self.yogurt, 6)
        self.expect_receipt_properties(6.0, 1, 1)
        self.expect_receipt_item_properties(self.receipt.items[0], self.yogurt, 1.20, 6 * 1.20, 6)
    
    def test_five_for_amount_offer(self):
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.toothpaste, 7.49)
        self.given_cart_with(self.toothpaste, 5)
        self.expect_receipt_properties(7.49, 1, 1)
        self.expect_receipt_item_properties(self.receipt.items[0], self.toothpaste, 1.79, 5 * 1.79, 5)
    
    def test_receipt_with_all_offers(self):
        self.teller.add_special_offer(SpecialOfferType.PERCENT_DISCOUNT, self.toothbrush, 10.0)
        self.teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, self.milk, 0)
        self.teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, self.toothpaste, 7.49)
        self.given_cart_with(self.apples, 2.5)
        self.given_cart_with(self.toothbrush, 3)
        self.given_cart_with(self.milk, 5)
        self.given_cart_with(self.toothpaste, 5)
        self.expect_receipt_properties(27.138, 3, 4)
        self.expect_receipt_item_properties(self.receipt.items[0], self.apples, 1.99, 2.5 * 1.99, 2.5)
        self.expect_receipt_item_properties(self.receipt.items[1], self.toothbrush, 0.99, 3 * 0.99, 3)
        self.expect_receipt_item_properties(self.receipt.items[2], self.milk, 3.0, 5 * 3.0, 5)
        self.expect_receipt_item_properties(self.receipt.items[3], self.toothpaste, 1.79, 5 * 1.79, 5)
    
    def test_bundle_offer(self):
        bundle = {self.toothbrush: 1, self.toothpaste: 1}
        self.teller.add_special_offer(SpecialOfferType.BUNDLE_DISCOUNT, self.toothbrush, bundle)
        self.given_cart_with(self.toothbrush, 2)
        self.given_cart_with(self.toothpaste, 1)
        self.expect_receipt_properties(3.492, 1, 2)

    def make_catalog(self):
        catalog = FakeCatalog()
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(self.toothbrush, 0.99)
        self.apples = Product("apples", ProductUnit.KILO)
        catalog.add_product(self.apples, 1.99)
        self.milk = Product("milk", ProductUnit.EACH)
        catalog.add_product(self.milk, 3.0)
        self.yogurt = Product("yogurt", ProductUnit.EACH)
        catalog.add_product(self.yogurt, 1.20)
        self.toothpaste = Product("toothpaste", ProductUnit.EACH)
        catalog.add_product(self.toothpaste, 1.79)
        return catalog
    
    def given_cart_with(self, product, quantity):
        if product: self.cart.add_item_quantity(product, quantity)
        self.receipt = self.teller.checks_out_articles_from(self.cart)
        return self
    
    def expect_receipt_properties(self, total_price, discounts, items):
        self.assertAlmostEqual(self.receipt.total_price(), total_price, 2)
        assert_that(self.receipt.discounts).is_length(discounts)
        assert_that(self.receipt.items).is_length(items)
    
    def expect_receipt_item_properties(self, item, product, price, total_price, quantity):
        assert_that(item.product).is_equal_to(product)
        assert_that(item.price).is_equal_to(price)
        assert_that(item.total_price).is_equal_to(total_price)
        assert_that(item.quantity).is_equal_to(quantity)