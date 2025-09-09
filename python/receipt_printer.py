from model_objects import ProductUnit

class ReceiptPrinter:

    def __init__(self, columns=40):
        self.columns = columns
    
    def print_receipt(self, receipt):
        lines = []
        for item in receipt.items:
            lines.append(self.print_receipt_item(item))
        for discount in receipt.discounts:
            lines.append(self.print_discount(discount))
        lines.append(self.present_total(receipt))
        return "".join(str(line) for line in lines)
  
    
    def print_receipt_item(self, item):
        total_price_printed = self.print_price(item.total_price)
        name = item.product.name
        line = self.format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"
        return line

    def format_line_with_whitespace(self, name, value):
        whitespace = self.columns - len(name) - len(value)
        return f"{name}{' ' * whitespace}{value}\n"

    def print_price(self, price):
        return f"{price:.2f}"

    def print_quantity(self, item):
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        return f"{item.quantity:.3f}"

    def print_discount(self, discount):
        name = f"{discount.description} ({discount.product.name})"
        value = self.print_price(discount.discount_amount)
        return self.format_line_with_whitespace(name, value)

    def present_total(self, receipt):
        value = self.print_price(receipt.total_price())
        return f"\n{self.format_line_with_whitespace('Total: ', value)}"
