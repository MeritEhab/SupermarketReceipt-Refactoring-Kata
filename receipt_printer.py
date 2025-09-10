from model_objects import ProductUnit

class ReceiptPrinter():
    def __init__(self, columns=40):
        self.columns = columns

    def _print_price(self, price):
        return f"{price:.2f}"

    def _print_quantity(self, item):
        if ProductUnit.EACH == item.product.unit:
            return str(int(item.quantity))
        return f"{item.quantity:.3f}"


class TextReceiptPrinter(ReceiptPrinter):    
    def print_receipt(self, receipt):
        lines = []
        for item in receipt.items:
            lines.append(self._print_receipt_item(item))
        for discount in receipt.discounts:
            lines.append(self._print_discount(discount))
        lines.append(self._present_total(receipt))
        return "".join(str(line) for line in lines)
  
    def _print_receipt_item(self, item):
        total_price_printed = self._print_price(item.total_price)
        name = item.product.name
        line = self._format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self._print_price(item.price)} * {self._print_quantity(item)}\n"
        return line

    def _print_discount(self, discount):
        name = f"{discount.description} ({discount.product.name})"
        value = self._print_price(discount.discount_amount)
        return self._format_line_with_whitespace(name, value)
    
    def _format_line_with_whitespace(self, name, value):
        whitespace = self.columns - len(name) - len(value)
        return f"{name}{' ' * whitespace}{value}\n"

    def _present_total(self, receipt):
        value = self._print_price(receipt.total_price())
        return f"\n{self._format_line_with_whitespace('Total: ', value)}"


class HtmlReceiptPrinter(ReceiptPrinter):
    def print_receipt(self, receipt):
        items = "".join(self._print_receipt_item(item) for item in receipt.items)
        discounts = "".join(self._print_discount(d) for d in receipt.discounts)
        total = self._present_total(receipt)
        return self._html_receipt_format(items, discounts, total)

    def _print_receipt_item(self, item):
        line = f"<tr><td>{item.product.name}</td><td>{self._print_price(item.total_price)}</td></tr>"
        if item.quantity != 1:
            line = f"<tr><td>{item.product.name}<br>{self._print_price(item.price)} * {self._print_quantity(item)}</td><td>{self._print_price(item.total_price)}</td></tr>"
        return line
    
    def _print_discount(self, discount):
        return f"<tr><td><strong>Discount</strong></td><td>{discount.description}</td> <td>({discount.product.name}):</td> <td>{self._print_price(discount.discount_amount)}</td></tr>"

    def _present_total(self, receipt):
        return f"<tr><td><strong>Total:</strong></td> <td><strong>{self._print_price(receipt.total_price())}</strong></td></tr>"

    def _html_receipt_format(self, items, discounts, total):
        return f"""
            <!doctype html>
            <html lang=\"en\">
                <head><meta charset=\"utf-8\"><title>Receipt</title></head>
                <body>
                    <h1>Receipt</h1>
                    <table cellspacing="15">
                        {items}
                        {discounts}
                        <tr></tr><tr></tr>
                        {total}
                    </table>
                </body>
            </html>
        """.strip()
