import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
from datetime import datetime
from medicine_prices import medicine_prices

# Node class represents a single item in the inventory queue
class Node:
    def __init__(self, name, expiry_date, quantity, bin_location, price):
        self.name = name
        self.expiry_date = expiry_date
        self.quantity = quantity
        self.bin_location = bin_location
        self.price = price
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self.size

    def append(self, name, expiry_date, quantity, bin_location, price):
        temp = Node(name, expiry_date, quantity, bin_location, price)
        if self.is_empty():
            self.head = temp
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = temp
        self.size += 1

    def remove(self, name=None):
        if self.is_empty():
            return

        if name is not None:
            if self.head.name == name:
                self.head = self.head.next
                self.size -= 1
                return

            current = self.head
            while current.next is not None:
                if current.next.name == name:
                    current.next = current.next.next
                    self.size -= 1
                    return
                current = current.next

    def find_previousnode(self, name=None):
        if self.is_empty():
            return None

        if name is not None:
            current = self.head
            while current.next is not None:
                if current.next.name == name:
                    return current
                current = current.next

        return None

    def get_items(self):
        # Retrieve all items from the linked list
        items = []
        current = self.head
        while current:
            items.append(current)
            current = current.next

        return items
    
def exit_window():
    exit()

# InventorySystem class represents the GUI application for the inventory system
class InventorySystem:
    def __init__(self, root):
        self.root = root
        self.inventory_list = LinkedList()

        self.root.title("Inventory System")

        self.treeview = ttk.Treeview(root, columns=("Name", "Expiry_date", "Quantity", "Bin Location", "Price"), show="headings")
        self.treeview.heading("Name", text="Name")
        self.treeview.heading("Expiry_date", text="Expiry Date")
        self.treeview.heading("Quantity", text="Quantity")
        self.treeview.heading("Bin Location", text="Bin Location")
        self.treeview.heading("Price", text="Price")
        self.treeview.pack(pady=10)

        entry_frame = ttk.Frame(root)
        entry_frame.pack()

        # Entry fields for Name, Expiry Date, Quantity, Bin Location, and Price
        self.entry_name = ttk.Entry(entry_frame, width=20)
        self.entry_name.grid(row=2, column=5, columnspan=10, padx=5, pady=5)
        self.entry_expiry_date = ttk.Entry(entry_frame, width=15)
        self.entry_expiry_date.grid(row=3, column=5, columnspan=10, padx=5, pady=5)
        self.entry_quantity = ttk.Entry(entry_frame, width=15)
        self.entry_quantity.grid(row=4, column=5, columnspan=10, padx=5, pady=5)
        self.entry_bin_location = ttk.Entry(entry_frame, width=10)
        self.entry_bin_location.grid(row=5, column=5, columnspan=10, padx=5, pady=5)
        self.entry_price = ttk.Entry(entry_frame, width=10)
        self.entry_price.grid(row=6, column=5, columnspan=10, padx=5, pady=5)

        # Labels for entry fields
        ttk.Label(entry_frame, text="Name:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(entry_frame, text="Expiry Date:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(entry_frame, text="Quantity:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Label(entry_frame, text="Bin Location:").grid(row=5, column=0, padx=5, pady=5)
        ttk.Label(entry_frame, text="Price:").grid(row=6, column=0, padx=5, pady=5)

        button_frame = ttk.Frame(root)
        button_frame.pack()

        # Buttons for adding to inventory, updating inventory, searching inventory, and displaying all inventories
        ttk.Button(button_frame, text="Add to Inventory", command=self.add_to_inventory).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Update", command=self.update_inventory).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Search", command=self.search_inventory).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Display All", command=self.display_all_inventory).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_item).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(button_frame, text="Back", command=self.close_window).grid(row=0, column=5, padx=5, pady=5)

        self.load_data()

    def close_window(self):
        self.root.destroy()

    def display_all_inventory(self):
        # Display all the items in the inventory_queue in the treeview widget
        self.treeview.delete(*self.treeview.get_children())
        items = self.inventory_list.get_items()

        # Sort the items based on the expiry date
        items.sort(key=lambda x: datetime.strptime(x.expiry_date, "%Y-%m-%d"))

        for item in items:
            self.treeview.insert("", "end", values=(item.name, item.expiry_date, item.quantity, item.bin_location, item.price))

    def load_data(self):
        # Load data from the inventory.csv file and populate the inventory_list
        try:
            with open("inventory.csv", newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 5:  # Check if the row has the correct number of values
                        name, expiry_date, quantity, bin_location, price = row
                        self.inventory_list.append(name, expiry_date, quantity, bin_location, price)
                        medicine_prices[name.lower()] = float(price)
                    else:
                        # Show a warning message if the row does not have the expected number of values
                        messagebox.showwarning("Warning", "Invalid data format in inventory file.")
        except FileNotFoundError:
            # Do nothing if the inventory file is not found
            pass

        self.display_all_inventory()
        return medicine_prices

    import csv

    def save_data(self):
        # Save the inventory_queue data to the inventory.csv file
        with open("inventory.csv", "w", newline='') as file:
            writer = csv.writer(file)
            current = self.inventory_list.head
            while current:
                writer.writerow([current.name, current.expiry_date, current.quantity, current.bin_location, current.price])
                current = current.next

        # Save the medicine prices to the medicine_prices.csv file
        with open("medicine_prices.csv", "w", newline='') as file:
            writer = csv.writer(file)
            current = self.inventory_queue.front
            while current:
                writer.writerow([current.name, current.price])
                current = current.next

    def delete_data(self):
        #Clears the field for the netry of new data
        self.entry_name.delete(0, tk.END)
        self.entry_bin_location.delete(0, tk.END)
        self.entry_expiry_date.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

    def add_to_inventory(self):
        # Add an item to the inventpry_list based on the entry fields
        name = self.entry_name.get()
        expiry_date = self.entry_expiry_date.get()
        quantity = self.entry_quantity.get()
        bin_location = self.entry_bin_location.get()
        price = self.entry_price.get()

        if name and expiry_date and quantity and bin_location and price:
            self.inventory_list.append(name, expiry_date, quantity, bin_location, price)
            messagebox.showinfo("Success", "Product added to inventory")
            self.display_all_inventory()
            self.save_data()
            self.delete_data()
        else:
            messagebox.showwarning("Warning", "Please fill all the fields")

    def update_inventory(self):
        # Update an item in the inventory_list based on the entry fields and name
        name = self.entry_name.get()
        expiry_date = self.entry_expiry_date.get()
        quantity = self.entry_quantity.get()
        bin_location = self.entry_bin_location.get()
        price = self.entry_price.get()

        if name and expiry_date and quantity and bin_location and price:
            # Search for the item to update
            previous_node = self.inventory_list.find_previousnode(name=name)
            if previous_node is not None:
                node = previous_node.next
                node.name = name
                node.expiry_date = expiry_date
                node.quantity = quantity
                node.bin_location = bin_location
                node.price = price
                messagebox.showinfo("Success", "Inventory updated")
                self.display_all_inventory()
                self.save_data()
                self.delete_data()
            else:
                messagebox.showwarning("Warning", "Item not found in the inventory")
        else:
            messagebox.showwarning("Warning", "Please fill all the fields")

    def search_inventory(self):
        # Search for an item in the inventory_queue based on the entry fields
        name = self.entry_name.get()
        expiry_date = self.entry_expiry_date.get()
        quantity = self.entry_quantity.get()
        bin_location = self.entry_bin_location.get()

        if name or expiry_date or quantity or bin_location:
            # If any of the entry fields are filled, search for matching items in the inventory_list
            results = []
            current = self.inventory_list.head
            while current:
                if (name and current.name == name) or \
                        (expiry_date and current.expiry_date == expiry_date) or \
                        (quantity and current.quantity == quantity) or \
                        (bin_location and current.bin_location == bin_location):
                    results.append(current)
                current = current.next

            if results:
                self.display_search_results(results)
                self.delete_data()
            else:
                messagebox.showinfo("Search Results", "No matching items found in the inventory")
        else:
            # Show a warning message box if all the entry fields are empty
            messagebox.showwarning("Warning", "Please enter at least one search criteria")

    def display_search_results(self, results):
        # Display the search results in the treeview widget
        self.treeview.delete(*self.treeview.get_children())

        for item in results:
            self.treeview.insert("", "end", values=(item.name, item.expiry_date, item.quantity, item.bin_location, item.price))

    def delete_item(self):
        # Delete the selected item from the inventory_list
        selected_item = self.treeview.focus()
        if selected_item:
            item_values = self.treeview.item(selected_item, "values")
            item_name = item_values[0]
            self.inventory_list.remove(name=item_name)
            self.treeview.delete(selected_item)
            self.save_data()
            self.delete_data()
            messagebox.showinfo("Success", "Item deleted from inventory")
        else:
            messagebox.showwarning("Warning", "Please select an item to delete")


def main():
    # Create the main window
    root = tk.Tk()

    # Create an instance of the InventorySystem class
    inventory_system = InventorySystem(root)
    
    root.protocol("WM_DELETE_WINDOW", lambda: exit_window())

    # Run the main event loop
    root.mainloop()


root = None
main()
