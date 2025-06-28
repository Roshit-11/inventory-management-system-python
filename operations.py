# Import functions to read products and write/update stock and receipts
from read import read_products
from write import update_stock, generate_purchase_receipt

# Function to calculate free items based on 'buy three get one free' policy
def calculate_free_items(quantity):
    """Calculate free items based on 'buy three get one free' policy"""
    # Return the number of free items (1 free for every 3 purchased)
    return quantity // 3

# Function to process a sale transaction
def process_sale(products, product_id, quantity):
    """Process a sale transaction"""
    # Check if product_id is valid (between 1 and length of products list)
    if 0 < product_id <= len(products):
        # Get the product from the list (adjust for 0-based indexing)
        product = products[product_id - 1]
        # Calculate free items based on quantity
        free_items = calculate_free_items(quantity)
        # Total items to deduct from stock (purchased + free)
        total_items = quantity + free_items
        
        # Check if enough stock is available for the total items
        if product['quantity'] >= total_items:
            # Deduct total items from stock
            product['quantity'] -= total_items
            # Return a dictionary with sale details
            return {
                'name': product['name'],
                'brand': product['brand'],
                'quantity': quantity,
                'free': free_items,
                'price': quantity * product['selling_price']  # Total price = quantity * selling price
            }
    # Return None if product_id is invalid or insufficient stock
    return None

# Function to validate if a quantity input is a positive integer
def validate_quantity(value):
    """Validate if input is a positive integer"""
    try:
        # Attempt to convert value to integer and check if it's positive
        return int(value) > 0
    except ValueError:
        # Return False if conversion fails (non-numeric input)
        return False

# Function to display the inventory table
def display_products(_):
    # Print table header with borders
    print("--------------------------------------------------------------------------")
    print("ID   Product Name         Brand           Quantity  Price     Origin")
    print("--------------------------------------------------------------------------")
    try:
        # Open products.txt file for reading
        file = open('products.txt', 'r')
        # Read all lines from the file
        product_lines = file.readlines()
        # Close the file
        file.close()
        # Loop through each product line
        for idx in range(len(product_lines)):
            # Get the current line
            line = product_lines[idx]
            # Remove trailing newline if present
            if line.endswith('\n'):
                line = line[:len(line) - 1]
            # Split line into fields (name, brand, quantity, cost, origin)
            fields = line.split(', ')
            # Ensure the line has at least 5 fields
            if len(fields) >= 5:
                # Extract individual fields
                name = fields[0]
                brand = fields[1]
                quantity = fields[2]
                cost = fields[3]
                origin = fields[4]
                try:
                    # Calculate selling price as 2 times the cost
                    selling_price = float(cost) * 2
                    # Format selling price to 2 decimal places
                    price_str = "%.2f" % selling_price
                except:
                    # Set price to "ERROR" if calculation fails
                    price_str = "ERROR"
                # Print product ID with padding
                print(str(idx + 1), end='')
                id_len = len(str(idx + 1))
                for _ in range(5 - id_len):
                    print(' ', end='')
                # Print product name with padding
                print(name, end='')
                for _ in range(20 - len(name)):
                    print(' ', end='')
                # Print brand with padding
                print(brand, end='')
                for _ in range(15 - len(brand)):
                    print(' ', end='')
                # Print quantity with padding
                print(quantity, end='')
                for _ in range(10 - len(quantity)):
                    print(' ', end='')
                # Print selling price with padding
                print(price_str, end='')
                for _ in range(10 - len(price_str)):
                    print(' ', end='')
                # Print origin
                print(origin)
    except:
        # Print error message if file reading fails
        print("Error reading products.txt!")
    # Print table footer
    print("--------------------------------------------------------------------------")

# Function to handle the purchase process (add or update products)
def purchase_products():
    """Handle product purchases"""
    # Load products from file
    products = read_products()
    # Display purchase submenu
    print("\n=== Purchase New Products ===")
    print("1. Add new product\n2. Update existing product quantity")
    # Get user's submenu choice
    choice = input("Enter choice (1-2): ")
    
    # Handle choice 1: Add new product
    if choice == '1':
        add_new_product(products)  # Receipt handled inside
    # Handle choice 2: Update existing product quantity
    elif choice == '2':
        update_product_quantity(products)  # Receipt handled inside
    else:
        # Print error message for invalid choice
        print("Invalid choice!")

# Function to add a new product to the inventory
def add_new_product(products):
    """Add new product to inventory"""
    # Prompt for product details
    name = input("Product name: ")
    brand = input("Brand: ")
    country = input("Country: ")
    quantity = get_positive_number("Quantity: ")  # Get quantity (should be positive)
    cost = get_positive_number("Cost price (Rs): ", float)  # Get cost (should be positive float)
    
    # Check if product already exists (case-insensitive)
    if any(p['name'].lower() == name.lower() and p['brand'].lower() == brand.lower() for p in products):
        print("Product exists! Use update option.")
        return
    
    # Add new product to the list with selling price as 2 times the cost
    products.append({
        'name': name,
        'brand': brand,
        'quantity': quantity,
        'cost': cost,
        'country': country,
        'selling_price': cost * 2
    })
    
    # Update products.txt with the new product
    update_stock(products)
    
    # Generate purchase receipt for the new product
    generate_purchase_receipt(name, brand, quantity, cost)
    
    # Confirm product addition
    print("Product added")

# Function to update the quantity of an existing product
def update_product_quantity(products):
    """Update existing product stock"""
    # Check if there are any products to update
    if not products:
        print("No products!")
        return
    
    # Display current inventory
    display_products(products)
    try:
        # Prompt for product ID to update
        product_id = int(input("Product ID to update: "))
        # Validate product ID
        if not 0 < product_id <= len(products):
            raise ValueError
        
        # Get additional quantity and new cost
        quantity = get_positive_number("Additional quantity: ")
        cost = get_positive_number("New cost price (Rs): ", float)
        
        # Get the product to update
        product = products[product_id - 1]
        
        # If the new cost differs, recalculate average cost and selling price
        if product['cost'] != cost:
            total_value = (product['quantity'] * product['cost']) + (quantity * cost)
            product['quantity'] += quantity
            product['cost'] = round(total_value / product['quantity'], 2)
            product['selling_price'] = product['cost'] * 2
        
        # Update products.txt with the modified product
        update_stock(products)
        # Generate purchase receipt for the updated quantity
        generate_purchase_receipt(product['name'], product['brand'], quantity, cost)
        # Confirm stock update
        print("Stock updated!")
    
        
    except (ValueError, IndexError):
        # Print error message for invalid input (e.g., non-numeric product ID)
        print("Invalid input!")

# Function to get a positive number input from the user
def get_positive_number(prompt, type_cast=int):
    """Get valid positive number input"""
    while True:
        try:
            value = type_cast(input(prompt))
            if value > 0:
                return value
            print("Must be positive!")
        except ValueError:
            print("Invalid input!")
