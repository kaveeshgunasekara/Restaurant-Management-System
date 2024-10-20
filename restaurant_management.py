class MenuItem:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

class Table:
    def __init__(self, number, max_capacity):
        self.number = number
        self.max_capacity = max_capacity
        self.is_booked = False
        self.customer_name = ""
        self.num_customers = 0
        self.orders = []
        self.total_bill = 0.0

class RestaurantManager:
    def __init__(self):
        self.tables = [
            Table(1, 4),
            Table(2, 4),
            Table(3, 4),
            Table(4, 4)
        ]
        self.menu = [
            MenuItem("F001", "Chicken Fried Rice", 1500),
            MenuItem("F002", "Egg Burger with Fried Mushroom", 1000),
            MenuItem("F003", "Vegetable Pizza", 600),
            MenuItem("B001", "Avocado Milkshake", 500),
            MenuItem("B002", "Hot Fresh Milk", 400),
            MenuItem("B003", "Coca-Cola", 300)
        ]
        self.transaction_fee_percent = 2
        self.total_income = 0.0  # Track the total income for the night session

    def display_menu(self):
        print("\n===================================")
        print("               Menu               ")
        print("===================================")
        print("{:<6} {:<30} {:<10}".format("Code", "Item", "Unit Price (LKR)"))
        print("===================================")
        for item in self.menu:
            print("{:<6} {:<30} {:<10}".format(item.code, item.name, item.price))
        print("===================================")

    def book_table(self):
        print("\n== Book Table ==")
        table_number = int(input("Enter table number (1-4): "))
        customer_name = input("Enter customer name: ")
        num_customers = int(input("Enter number of customers: "))
        
        table_index = table_number - 1  # table_number is 1-based, convert to 0-based index
        if self.tables[table_index].is_booked:
            print("Sorry, this table is already booked.")
            return False
        elif num_customers > self.tables[table_index].max_capacity:
            print("Sorry, this table cannot accommodate that many customers.")
            return False
        else:
            self.tables[table_index].is_booked = True
            self.tables[table_index].customer_name = customer_name
            self.tables[table_index].num_customers = num_customers
            print(f"Table {table_number} booked successfully for {num_customers} customers.")
            return True

    def take_order(self):
        print("\n== Place Order ==")
        table_number = int(input("Enter table number (1-4) to place order: "))
        item_code = input("Enter item code from the menu: ")
        quantity = int(input("Enter quantity: "))
        
        table_index = table_number - 1  # table_number is 1-based, convert to 0-based index
        if not self.tables[table_index].is_booked:
            print("Please book a table first.")
            return False
        found_item = None
        for item in self.menu:
            if item.code == item_code:
                found_item = item
                break
        if not found_item:
            print("Invalid item code. Please select a valid item from the menu.")
            return False
        total_price = found_item.price * quantity
        self.tables[table_index].orders.append((found_item.name, quantity, total_price))
        self.tables[table_index].total_bill += total_price
        print(f"{quantity} {found_item.name}(s) added to the order for Table {table_number}.")
        return True

    def process_payment(self):
        print("\n== Process Payment ==")
        table_number = int(input("Enter table number (1-4) to process payment: "))
        payment_method = input("Enter payment method ('cash' or 'card'): ").lower()
        
        table_index = table_number - 1  # table_number is 1-based, convert to 0-based index
        if not self.tables[table_index].is_booked:
            print("No booking found for this table.")
            return False
        total_bill = self.tables[table_index].total_bill
        if payment_method == "cash":
            print(f"Total bill for Table {table_number}: LKR {total_bill}")
        elif payment_method == "card":
            transaction_fee = (total_bill * self.transaction_fee_percent) / 100
            total_bill += transaction_fee
            print(f"Total bill for Table {table_number} (including {self.transaction_fee_percent}% transaction fee): LKR {total_bill}")
        else:
            print("Invalid payment method. Please choose 'cash' or 'card'.")
            return False
        self.total_income += total_bill  # Add to total income
        self.tables[table_index].is_booked = False  # free up the table after payment
        self.tables[table_index].customer_name = ""
        self.tables[table_index].num_customers = 0
        self.tables[table_index].orders = []
        self.tables[table_index].total_bill = 0.0
        return True

    def calculate_total_income(self):
        return self.total_income

# Main program
if __name__ == "__main__":
    manager = RestaurantManager()

    while True:
        print("\nWelcome to Amaya Restaurant Management System")
        print("===========================================")
        print("1. Book Table")
        print("2. Display Menu")
        print("3. Place Order")
        print("4. Process Payment")
        print("5. Calculate Total Income")
        print("6. Exit")
        print("===========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            manager.book_table()
        elif choice == "2":
            manager.display_menu()
        elif choice == "3":
            manager.take_order()
        elif choice == "4":
            manager.process_payment()
        elif choice == "5":
            total_income = manager.calculate_total_income()
            print(f"\nTotal income for the night session: LKR {total_income}")
        elif choice == "6":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-6).")
