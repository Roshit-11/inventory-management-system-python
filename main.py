# Import necessary functions from other modules
from read import read_products
from operations import display_products, process_sale, validate_quantity, purchase_products
from write import generate_sales_invoice, update_stock

# Main function to run the store management system
def main():
    # Infinite loop to keep the menu running until exit
    while True:
        
        # Display menu options
        print("1. Make Sale")
        print("2. Purchase Products")
        print("3. View Inventory")
        print("4. Exit")
        
        # Get user's menu choice
        choice = input("\nEnter your choice (1-4): ")
        
        # Handle option 1: Make Sale
        if choice == '1':
            # Load products from file
            products = read_products()
            # Check if there are any products available
            if not products:
                print("No products available!")
                continue
            
            # Display current inventory
            display_products(products)
            # Get customer name for the sale
            customer_name = input("\nEnter customer name: ")
            # Initialize empty cart and total amount
            cart_items = []
            total_amount = 0
            
            # Inner loop to add items to the cart
            while True:
                try: 
                    # Get product ID from user
                    product_id = int(input("\nEnter product ID (0 to finish): "))
                    # Exit inner loop if user enters 0
                    if product_id == 0:
                        print("Invalid id, ending the sale process and checking you out with your stuffs.")
                        break
                    
                    # Get quantity for the selected product
                    quantity = input("Enter quantity: ")
                    # Validate quantity is positive
                    if not validate_quantity(quantity):
                        print("Invalid quantity! Please enter a positive number.")
                        continue
                    
                    # Convert quantity to integer
                    quantity = int(quantity)
                    # Process the sale for the selected product and quantity
                    result = process_sale(products, product_id, quantity)
                    
                    # Add item to cart if sale is successful
                    if result:
                        cart_items.append(result)
                        total_amount += result['price']
                        # Display item added to cart with free items
                        print("Added to cart: " + result['name'] + " x " + str(quantity) + " (+" + str(result['free']) + " free)")
                    else:
                        # Display error if product ID is invalid or stock is insufficient
                        print("Invalid product ID or insufficient stock!")
                        
                except ValueError:
                    # Handle non-numeric input for product ID or quantity
                    print("Invalid input! Please enter a number.")
            
            # Generate invoice and update stock if items were added to cart
            if cart_items:
                generate_sales_invoice(customer_name, cart_items, total_amount)
                update_stock(products)
                print("\nSale completed successfully!")
                
        # Handle option 2: Purchase Products
        elif choice == '2':
            
            # Delegate purchase process to operations module
            purchase_products()
            
        # Handle option 3: View Inventory
        elif choice == '3':
            # Load products from file
            products = read_products()
            # Check if there are any products available
            if not products:
                print("No products available!")
                continue
            # Display current inventory
            display_products(products)
            
        # Handle option 4: Exit
        elif choice == '4':
            # Load products (though not used here, likely for consistency)
            products = read_products()
            # Display goodbye message and exit loop
            print("Thank you for using WeCare Beauty Store System!")
            break
            
        else:
            # Handle invalid menu choice
            print("Invalid choice! Please try again.")

# Entry point to run the program
if __name__ == "__main__":
    main()
