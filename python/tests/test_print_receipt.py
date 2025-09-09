import os
import unittest
import sys

from assertpy import assert_that

from model_objects import Product, ProductUnit, Discount
from receipt import Receipt
from receipt_printer import ReceiptPrinter


class TestPrintReceipt(unittest.TestCase):
    def setUp(self):
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.apples = Product("apples", ProductUnit.KILO)
        self.receipt = Receipt()
        self.class_name = self.__class__.__name__

    def test_one_line_item(self):
        function_name = sys._getframe().f_code.co_name
        self.receipt.add_product(self.toothbrush, 1, 0.99, 0.99)
        self.given(function_name, self.receipt).expect_formatted_text_receipt()

    def test_quantity_two(self):
        function_name = sys._getframe().f_code.co_name
        self.receipt.add_product(self.toothbrush, 2, 0.99, 0.99 * 2)
        self.given(function_name, self.receipt).expect_formatted_text_receipt()

    def test_loose_weight(self):
        function_name = sys._getframe().f_code.co_name
        self.receipt.add_product(self.apples, 2.3, 1.99, 1.99 * 2.3)
        self.given(function_name, self.receipt).expect_formatted_text_receipt()

    def test_total(self):
        function_name = sys._getframe().f_code.co_name
        self.receipt.add_product(self.toothbrush, 1, 0.99, 0.99 * 2)
        self.receipt.add_product(self.apples, 0.75, 1.99, 1.99 * 0.75)
        self.given(function_name, self.receipt).expect_formatted_text_receipt()

    def test_discounts(self):
        function_name = sys._getframe().f_code.co_name
        self.receipt.add_discount(Discount(self.apples, "3 for 2", -0.99))
        self.given(function_name, self.receipt).expect_formatted_text_receipt()

    def test_whole_receipt(self):
        function_name = sys._getframe().f_code.co_name
        self.receipt.add_product(self.toothbrush, 1, 0.99, 0.99)
        self.receipt.add_product(self.toothbrush, 2, 0.99, 0.99*2)
        self.receipt.add_product(self.apples, 0.75, 1.99, 1.99 * 0.75)
        self.receipt.add_discount(Discount(self.apples, "3 for 2", -0.99))
        self.given(function_name, self.receipt).expect_formatted_text_receipt()

    def _get_receipt_comparable_result(self, file_name):
        receipts_dir = os.path.join(os.getcwd(), "tests", "approved_files")
        with open(os.path.join(receipts_dir, file_name), 'r') as f:
            return f.read()
    
    def given(self, function_name, receipt):
        self.expected_output = self._get_receipt_comparable_result(f"{self.class_name}.{function_name}.txt")
        self.result = ReceiptPrinter().print_receipt(receipt)
        return self

    def expect_formatted_text_receipt(self):
        assert_that(self.result).is_equal_to(self.expected_output)
