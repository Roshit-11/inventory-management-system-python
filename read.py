def read_products():
    # Initialize empty product list
    products = []
    try:
        # Display product table header
        
        
        # Read product data from file
        with open('products.txt', 'r') as file:
            # Process file content
            file_content = file.read()
            product_lines = file_content.split('\n')
            product_data = {}

            # Create product dictionary
            for serial_number in range(1, len(product_lines)+1):
                product_data[serial_number] = product_lines[serial_number-1].split(', ')
            
            # Convert to system format
            for product_id, details in product_data.items():
                if len(details) >= 5:  
                    try:
                        products.append({
                            'name': details[0],
                            'brand': details[1],
                            'quantity': int(details[2]),
                            'cost': float(details[3]),
                            'country': details[4],
                            'selling_price': float(details[3]) * 3
                        })
                    except (ValueError, IndexError):
                        print(F"Error parsing product ID {product_id}")
        
        # Close table display
        print('-'*75)
        return products
    
    except FileNotFoundError:
        print("Error: products.txt file not found!")
        return []
