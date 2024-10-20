import tkinter as tk
from tkinter import messagebox

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

class RestaurantManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Amaya Restaurant Management System")

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

        self.create_widgets()

    def create_widgets(self):
        # Label
        lbl_title = tk.Label(self.root, text="Amaya Restaurant Management System", font=("Helvetica", 16))
        lbl_title.pack(pady=10)

        # Buttons
        btn_book_table = tk.Button(self.root, text="Book Table", width=20, command=self.book_table)
        btn_book_table.pack(pady=5)

        btn_display_menu = tk.Button(self.root, text="Display Menu", width=20, command=self.display_menu)
        btn_display_menu.pack(pady=5)

        btn_place_order = tk.Button(self.root, text="Place Order", width=20, command=self.place_order)
        btn_place_order.pack(pady=5)

        btn_process_payment = tk.Button(self.root, text="Process Payment", width=20, command=self.process_payment)
        btn_process_payment.pack(pady=5)

        btn_calculate_income = tk.Button(self.root, text="Calculate Total Income", width=20, command=self.calculate_income)
        btn_calculate_income.pack(pady=5)

        btn_exit = tk.Button(self.root, text="Exit", width=20, command=self.root.quit)
        btn_exit.pack(pady=5)

    def display_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Menu")

        lbl_menu = tk.Label(menu_window, text="Menu", font=("Helvetica", 14))
        lbl_menu.pack(pady=10)

        for item in self.menu:
            lbl_item = tk.Label(menu_window, text=f"{item.code}: {item.name} - LKR {item.price}")
            lbl_item.pack()

    def book_table(self):
        book_table_window = tk.Toplevel(self.root)
        book_table_window.title("Book Table")

        lbl_book_table = tk.Label(book_table_window, text="Book Table", font=("Helvetica", 14))
        lbl_book_table.pack(pady=10)

        lbl_table_number = tk.Label(book_table_window, text="Enter table number (1-4):")
        lbl_table_number.pack()
        entry_table_number = tk.Entry(book_table_window)
        entry_table_number.pack()

        lbl_customer_name = tk.Label(book_table_window, text="Enter customer name:")
        lbl_customer_name.pack()
        entry_customer_name = tk.Entry(book_table_window)
        entry_customer_name.pack()

        lbl_num_customers = tk.Label(book_table_window, text="Enter number of customers:")
        lbl_num_customers.pack()
        entry_num_customers = tk.Entry(book_table_window)
        entry_num_customers.pack()

        btn_book = tk.Button(book_table_window, text="Book", command=lambda: self.book_confirm(book_table_window,
                                                                                              entry_table_number.get(),
                                                                                              entry_customer_name.get(),
                                                                                              entry_num_customers.get()))
        btn_book.pack(pady=5)

    def book_confirm(self, book_table_window, table_number, customer_name, num_customers):
        try:
            table_number = int(table_number)
            num_customers = int(num_customers)

            if table_number < 1 or table_number > 4:
                raise ValueError("Table number must be between 1 and 4.")

            table_index = table_number - 1

            if self.tables[table_index].is_booked:
                messagebox.showerror("Error", "Sorry, this table is already booked.")
                return

            if num_customers > self.tables[table_index].max_capacity:
                messagebox.showerror("Error", "Sorry, this table cannot accommodate that many customers.")
                return

            self.tables[table_index].is_booked = True
            self.tables[table_index].customer_name = customer_name
            self.tables[table_index].num_customers = num_customers

            messagebox.showinfo("Success", f"Table {table_number} booked successfully for {num_customers} customers.")

            book_table_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def place_order(self):
        place_order_window = tk.Toplevel(self.root)
        place_order_window.title("Place Order")

        lbl_place_order = tk.Label(place_order_window, text="Place Order", font=("Helvetica", 14))
        lbl_place_order.pack(pady=10)

        lbl_table_number = tk.Label(place_order_window, text="Enter table number (1-4):")
        lbl_table_number.pack()
        entry_table_number = tk.Entry(place_order_window)
        entry_table_number.pack()

        lbl_item_code = tk.Label(place_order_window, text="Enter item code from the menu:")
        lbl_item_code.pack()
        entry_item_code = tk.Entry(place_order_window)
        entry_item_code.pack()

        lbl_quantity = tk.Label(place_order_window, text="Enter quantity:")
        lbl_quantity.pack()
        entry_quantity = tk.Entry(place_order_window)
        entry_quantity.pack()

        btn_place = tk.Button(place_order_window, text="Place Order", command=lambda: self.place_confirm(place_order_window,
                                                                                                        entry_table_number.get(),
                                                                                                        entry_item_code.get(),
                                                                                                        entry_quantity.get()))
        btn_place.pack(pady=5)

    def place_confirm(self, place_order_window, table_number, item_code, quantity):
        try:
            table_number = int(table_number)
            quantity = int(quantity)

            if table_number < 1 or table_number > 4:
                raise ValueError("Table number must be between 1 and 4.")

            table_index = table_number - 1

            if not self.tables[table_index].is_booked:
                messagebox.showerror("Error", "Please book a table first.")
                return

            found_item = None
            for item in self.menu:
                if item.code == item_code:
                    found_item = item
                    break

            if not found_item:
                messagebox.showerror("Error", "Invalid item code. Please select a valid item from the menu.")
                return

            total_price = found_item.price * quantity
            self.tables[table_index].orders.append((found_item.name, quantity, total_price))
            self.tables[table_index].total_bill += total_price

            messagebox.showinfo("Success", f"{quantity} {found_item.name}(s) added to the order for Table {table_number}.")

            place_order_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def process_payment(self):
        process_payment_window = tk.Toplevel(self.root)
        process_payment_window.title("Process Payment")

        lbl_process_payment = tk.Label(process_payment_window, text="Process Payment", font=("Helvetica", 14))
        lbl_process_payment.pack(pady=10)

        lbl_table_number = tk.Label(process_payment_window, text="Enter table number (1-4):")
        lbl_table_number.pack()
        entry_table_number = tk.Entry(process_payment_window)
        entry_table_number.pack()

        lbl_payment_method = tk.Label(process_payment_window, text="Enter payment method ('cash' or 'card'):")
        lbl_payment_method.pack()
        entry_payment_method = tk.Entry(process_payment_window)
        entry_payment_method.pack()

        btn_process = tk.Button(process_payment_window, text="Process Payment", command=lambda: self.process_confirm(process_payment_window,
                                                                                                                entry_table_number.get(),
                                                                                                                entry_payment_method.get()))
        btn_process.pack(pady=5)

    def process_confirm(self, process_payment_window, table_number, payment_method):
        try:
            table_number = int(table_number)

            if table_number < 1 or table_number > 4:
                raise ValueError("Table number must be between 1 and 4.")

            table_index = table_number - 1

            if not self.tables[table_index].is_booked:
                messagebox.showerror("Error", "No booking found for this table.")
                return

            total_bill = self.tables[table_index].total_bill

            if payment_method.lower() == "card":
                transaction_fee = (total_bill * self.transaction_fee_percent) / 100
                total_bill += transaction_fee

            messagebox.showinfo("Payment Summary", f"Total bill for Table {table_number}: LKR {total_bill}")

            self.tables[table_index].is_booked = False
            self.tables[table_index].customer_name = ""
            self.tables[table_index].num_customers = 0
            self.tables[table_index].orders = []
            self.tables[table_index].total_bill = 0.0

            process_payment_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def calculate_income(self):
        total_income = 0.0
        for table in self.tables:
            if table.is_booked:
                total_income += table.total_bill

        messagebox.showinfo("Total Income", f"Total income for the night session: LKR {total_income}")

# Main function for running the GUI
def main():
    root = tk.Tk()
    app = RestaurantManagerGUI(root)
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
