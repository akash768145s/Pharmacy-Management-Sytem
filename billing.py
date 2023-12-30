import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from Queue import LinkedQueue


class BillingModule:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Billing Module")
        self.root.state('zoomed')

        # Set the default font for the root window
        self.root.option_add("*Font", ("Arial", 12))

        self.cart_queue = LinkedQueue()
        self.sales = LinkedQueue()
        self.medicine_prices = {}
        self.total = 0.0

        self.open_window()

        # Create and configure the UI elements
        self.name_label = ttk.Label(self.root, text="Name:")
        self.name_entry = ttk.Entry(self.root, width=30)
        self.phone_label = ttk.Label(self.root, text="Phone Number:")
        self.phone_entry = ttk.Entry(self.root, width=30)
        self.doctor_label = ttk.Label(self.root, text="Doctor Name:")
        self.doctor_entry = ttk.Entry(self.root, width=30)

        self.date_label = ttk.Label(self.root, text="Date/Time: ")

        self.medicine_label = ttk.Label(self.root, text="Medicine:")
        self.medicine_entry = ttk.Entry(self.root, width=30)
        self.quantity_label = ttk.Label(self.root, text="Quantity:")
        self.quantity_entry = ttk.Entry(self.root, width=30)

        self.add_button = ttk.Button(self.root, text="Add to Cart", command=self.add_to_cart)
        self.delete_button = ttk.Button(self.root, text="Delete from Cart", command=self.delete_from_cart, style="Delete.TButton")
        self.new_button = ttk.Button(self.root, text="New bill", command=self.new_bill)
        self.back_button = ttk.Button(self.root, text="Back", command=self.exit_window)

        self.cart_label = ttk.Label(self.root, text="Cart:")
        self.cart_frame = ttk.Frame(self.root)

        self.cart_treeview = ttk.Treeview(self.cart_frame, columns=("Medicine", "Price", "Quantity"), show="headings", height=20)
        self.cart_treeview.column("Medicine", width=220)
        self.cart_treeview.column("Price", width=220)
        self.cart_treeview.column("Quantity", width=220)

        self.cart_treeview.heading("Medicine", text="Medicine", anchor=tk.CENTER)
        self.cart_treeview.heading("Price", text="Price", anchor=tk.CENTER)
        self.cart_treeview.heading("Quantity", text="Quantity", anchor=tk.CENTER)

        # Increase font size of column headers
        self.cart_treeview.tag_configure("header", font=("Arial", 12, "bold"))
        self.cart_treeview.tag_configure("values", font=("Arial", 12))

        self.cart_scrollbar = ttk.Scrollbar(self.cart_frame, orient="vertical", command=self.cart_treeview.yview)
        self.cart_treeview.configure(yscrollcommand=self.cart_scrollbar.set)

        self.cart_scrollbar.pack(side="right", fill="y")
        self.cart_treeview.pack(side="left", fill="both", expand=True)

        self.total_label = ttk.Label(self.root, text="Total: ₹0.00")
        self.checkout_button = ttk.Button(self.root, text="Checkout", command=self.checkout)
        self.invoice_text = ScrolledText(self.root, font=("Arial", 12), width=50, height=15)

        # Grid layout for UI elements
        self.name_label.grid(row=0, column=0, sticky=tk.E, pady=(40, 0))
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=(40, 0))
        self.phone_label.grid(row=1, column=0, sticky=tk.E)
        self.phone_entry.grid(row=1, column=1, sticky=tk.W)
        self.doctor_label.grid(row=2, column=0, sticky=tk.E)
        self.doctor_entry.grid(row=2, column=1, sticky=tk.W)
        self.date_label.grid(row=3, column=0, pady=20)

        self.update_datetime()

        self.medicine_label.grid(row=4, column=0, sticky=tk.E, pady=(20, 0))
        self.medicine_entry.grid(row=4, column=1, pady=(20, 0))
        self.quantity_label.grid(row=5, column=0, sticky=tk.E)
        self.quantity_entry.grid(row=5, column=1)
        
        self.add_button.grid(row=6, column=1, sticky=tk.W, pady=(30,0))
        self.delete_button.grid(row=6, column=1, padx=(40, 0), pady=(30, 0))

        self.cart_label.grid(row=7, column=0, sticky=tk.W, pady=(10,0))
        self.cart_frame.grid(row=8, columnspan=4, padx=(20, 0), pady=(0, 15))

        self.total_label.grid(row=9, column=2, sticky=tk.E)
        self.checkout_button.grid(row=9, columnspan=4)  
        self.new_button.grid(row=9, column=4,sticky=tk.E, padx=(0,175),pady=(10,0))
        self.back_button.grid(row=9, column=4,sticky=tk.E, padx=(0,55),pady=(10,0))

        self.invoice_text.grid(row=0, column=4, rowspan=9, padx=(0, 20), pady=(40, 0), sticky="nsew")
        self.root.grid_columnconfigure(4, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_window)

        self.root.mainloop()

    def checkout(self):
        """
        Generate an invoice based on the entered details and medicines.
        """
        customer_name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        doctor_name = self.doctor_entry.get()

        if not customer_name or not phone_number or not doctor_name:
            messagebox.showwarning("Warning", "Please fill in all the fields")
            return
        elif not self.is_valid_phone_number(phone_number):
            return

        bill_number = self.get_bill_number()

        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

        invoice = "                                                                      SRI MURUGAN MEDICALS\n\n"
        invoice += "         ------------------------------------------------------------------- Invoice ----------------------------------------------------------------------\n"
        invoice += f"       Bill Number: {bill_number}\n"
        invoice += f"       Date/Time: {current_datetime}\n\n"
        invoice += f"       Customer Name: {customer_name}\n"
        invoice += f"       Phone Number: {phone_number}\n"
        invoice += f"       Doctor Name: {doctor_name}\n\n"
        invoice += "         ---------------------------------------------------------------------------------------------------------------------------------------------------\n\n"
        invoice += "        Medicine            Price              Quantity            Total Price\n"

        for child in self.cart_treeview.get_children():
            medicine = self.cart_treeview.item(child)["values"][0]
            price = self.cart_treeview.item(child)["values"][1]
            quantity = self.cart_treeview.item(child)["values"][2]
            invoice += f"        {medicine}                 {price}                 {quantity}                    {float(price)*int(quantity)}\n"
            
            self.save_sales_data(bill_number, customer_name, phone_number, doctor_name, current_datetime, medicine, quantity, float(price) * int(quantity))

        invoice += "         ---------------------------------------------------------------------------------------------------------------------------------------------------\n\n"
        invoice += f"                                                                        Total:   {self.total}"

        self.invoice_text.delete("1.0", tk.END)
        self.invoice_text.insert(tk.END, invoice)

    def delete_from_cart(self):
        """
        Delete the selected row from the cart and Treeview.
        """
        selected_item = self.cart_treeview.selection()
        if selected_item:
            item_values = self.cart_treeview.item(selected_item, "values")
            medicine, price, quantity = item_values
            self.cart_treeview.delete(selected_item)
            self.total -= float(price) * int(quantity)
            self.total_label.config(text="Total: ₹%.2f" % self.total)
            self.cart_queue.remove((medicine, price, quantity))

    def exit_window(self):
        """
        Perform necessary actions before closing the window.
        """
        # Write the medicine prices dictionary back into the CSV file
        with open('medicine_prices.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for name, price in self.medicine_prices.items():
                writer.writerow([name, price])

        # Add sales data to the file
        self.add_sales_to_file()

        self.root.destroy()

    def open_window(self):
        """
        Open the main window and perform necessary initializations.
        """
        try:
            with open('medicine_prices.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        name, price = row
                        self.medicine_prices[name] = float(price)
        except FileNotFoundError:
            with open('medicine_prices.csv', mode='w') as file:
                pass

        self.add_sales_to_queue()

    def update_datetime(self):
        """
        Update the current date and time label.
        """
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        self.date_label.config(text="Date/Time: " + current_datetime)
        self.root.after(1000, self.update_datetime)

    def is_valid_phone_number(self, phone_number):
        """
        Check if the given phone number is valid.

        Args:
            phone_number (str): The phone number to check.

        Returns:
            bool: True if the phone number is valid, False otherwise.
        """
        if not phone_number.isdigit() or len(phone_number) != 10:
            messagebox.showwarning("Warning", "Phone number must have 10 digits")
            self.phone_entry.delete(0, tk.END)
            return False
        return True

    def add_sales_to_queue(self):
        """
        Add sales data from the file to the sales queue.
        """
        try:
            with open('sales_data.csv', mode='r', newline='') as file:
                sales_data = csv.reader(file)
                for line in sales_data:
                    self.sales.enqueue(line)
        except Exception:
            pass

    def add_sales_to_file(self):
        """
        Write sales data from the sales queue to the file.
        """
        with open('sales_data.csv', mode='w', newline='') as file:
            sales_data = csv.writer(file)
            for _ in range(len(self.sales)):
                sales_data.writerow(self.sales.dequeue())

    def save_sales_data(self, bill_number, customer_name, phone_number, doctor_name, current_datetime, medicine, quantity, price):
        """
        Save the sales data to the sales queue.

        Args:
            bill_number (str): The bill number.
            customer_name (str): The customer's name.
            phone_number (str): The customer's phone number.
            doctor_name (str): The doctor's name.
            current_datetime (str): The current date and time.
            medicine (str): The medicine name.
            quantity (str): The quantity of the medicine.
            price (float): The price of the medicine.
        """
        self.sales.enqueue([bill_number, customer_name, phone_number, doctor_name, current_datetime, medicine, quantity, price])

    def get_bill_number(self):
        """
        Get the next bill number.

        Returns:
            int: The next bill number.
        """
        bill_number = 0
        try:
            bill_number = int(self.sales.last_element()[0])
        except Exception:
            pass
        return bill_number + 1

    def reduce_quantity(self, medicine, quantity):
        """
        Reduce the quantity of the given medicine in the inventory.
        """
        inventory = []

        # Read the inventory data from the CSV file
        with open('inventory.csv', mode='r') as file:
            reader = csv.reader(file)
            inventory = list(reader)

        # Find the medicine with the earliest expiry date and reduce its quantity
        earliest_expiry = None
        earliest_expiry_index = -1
        for i, item in enumerate(inventory):
            item_name, item_expiry, item_quantity, bin_location, price = item
            if item_name == medicine:
                expiry_date = datetime.strptime(item_expiry, "%Y-%m-%d").date()
                if earliest_expiry is None or expiry_date < earliest_expiry:
                    earliest_expiry = expiry_date
                    earliest_expiry_index = i

        # Reduce the quantity of the medicine with the earliest expiry date
        if earliest_expiry_index != -1:
            item_quantity = int(inventory[earliest_expiry_index][2])
            updated_quantity = item_quantity - int(quantity)
            if updated_quantity > 0:
                inventory[earliest_expiry_index][2] = str(updated_quantity)
            elif updated_quantity == 0:
                inventory.pop(earliest_expiry_index)
                del self.medicine_prices[medicine]
            else:
                messagebox.showwarning("Warning", "Not enough medicines")
                return True
        else:
            messagebox.showwarning("Warning", "Medicine is not available")
            return True

        # Write the updated inventory data back to the CSV file
        with open('inventory.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(inventory)

    def add_to_cart(self):
        medicine = self.medicine_entry.get()
        quantity = self.quantity_entry.get()

        if not medicine or not quantity:
            messagebox.showwarning("Warning", "Enter all fields")
        else:
            # Fetch medicine price from the CSV file
            price = self.get_medicine_price(medicine)

            if price is not None:
                if self.reduce_quantity(medicine, quantity):
                    return
                self.cart_queue.enqueue((medicine, price, quantity))
                self.cart_treeview.insert("", tk.END, values=(medicine, price, quantity), tags=("values",))
                self.update_total_price()
            else:
                messagebox.showwarning("Warning", "Medicine is not available")

        self.medicine_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def get_medicine_price(self, medicine):
        with open("medicine_prices.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == medicine:
                    return row[1]

        return None

    def update_total_price(self):
        self.total = 0.0
        for item in self.cart_queue:
            self.total += float(item[1]) * int(item[2])

        self.total_label.config(text="Total: ₹%.2f" % self.total)

    def new_bill(self):
        # Clear the cart, reset total price, and update medicine prices dictionary and cart queue
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.doctor_entry.delete(0, tk.END)
        self.cart_treeview.delete(*self.cart_treeview.get_children())
        self.total = 0.0
        self.total_label.config(text="Total: ₹%.2f" % self.total)
        self.cart_queue = LinkedQueue()
        self.medicine_prices.clear()
        self.invoice_text.delete("1.0", tk.END)


def main():
    billing_module = BillingModule()

main()
