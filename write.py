def update_stock(products):
    """Update product stock file"""
    with open('products.txt', 'w') as file:
        for product in products:
            line = product['name'] + ", " + product['brand'] + ", " + str(product['quantity']) + ", " + str(product['cost']) + ", " + product['country'] + "\n"
            file.write(line)

def generate_sales_invoice(customer_name, items, total_amount):
    """Generate sales invoice"""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = "invoice_sale_" + timestamp + ".txt"
    
    # Build invoice content as a list of strings
    invoice_lines = []
    invoice_lines.append("=== WeCare Beauty Store ===\n")
    invoice_lines.append("Date: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    invoice_lines.append("Customer Name: " + customer_name + "\n")
    invoice_lines.append("\nPurchased Items:\n")
    invoice_lines.append("-" * 50 + "\n")
    
    # List purchased items
    for item in items:
        line = item['name'].ljust(15) + " " + item['brand'].ljust(15)
        line += str(item['quantity']) + "(+" + str(item['free']) + ") \t" + str(item['price']) + "\n"
        invoice_lines.append(line)
    
    invoice_lines.append("-" * 50 + "\n")
    invoice_lines.append("Total Amount: Rs. " + str(total_amount) + "\n")
    
    # Write to file
    with open(filename, 'w') as file:
        file.writelines(invoice_lines)
    
    # Print to IDLE shell
    print("".join(invoice_lines))
    
    print("Sales invoice generated: " + filename)

def generate_purchase_receipt(name, brand, quantity, cost):
    """Generate purchase invoice"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "invoice_purchase_" + timestamp + ".txt"
    
    # Calculate total, VAT, and grand total
    total = quantity * cost
    vat = total * 0.13
    grand_total = total + vat
    
    # Build receipt content as a list of strings
    receipt_lines = []
    receipt_lines.append("=== WeCare Beauty Store ===\n")
    receipt_lines.append("Date: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    receipt_lines.append("Product: " + name + "\n")
    receipt_lines.append("Brand: " + brand + "\n")
    receipt_lines.append("Quantity: " + str(quantity) + "\n")
    receipt_lines.append("Cost: Rs." + str(cost) + "\n")
    receipt_lines.append("Total: Rs." + str(total) + "\n")
    receipt_lines.append("VAT (13%): Rs." + str(round(vat, 2)) + "\n")
    receipt_lines.append("Grand Total: Rs." + str(round(grand_total, 2)) + "\n")
    
    # Write to file
    with open(filename, 'w') as file:
        file.writelines(receipt_lines)
    
    # Print to IDLE shell
    print("".join(receipt_lines))
    
    print("Purchase receipt generated: " + filename)
