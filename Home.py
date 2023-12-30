'''
This module Integrates the three main modules, namely Inventory Management, Billing Management,
Sales Tracking into a single Home Page for the users to select from. 

Authors: Ritujaa B <ritujaa2210209@ssn.edu.in>
         Sadakopa Ramakrishnan T <sadakopa2210221@ssn.edu.in>

Modified on 12 Jul 2023
'''

import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime, timedelta

# Create the root window
root = tk.Tk()
root.title('HOME PAGE')
root.geometry("500x600")
root.state('zoomed')

# Create the label for the welcome message
pharmacy_label = tk.Label(root, text="\nWelcome to the Home Page\n\nSelect suitable option", font=("Arial", 30))
pharmacy_label.pack(pady=10)

def import_billing_module():
    """Import and execute the billing module."""
    import billing
    billing.main()

def import_inventory_module():
    """Import and execute the inventory management module."""
    import Inventory_Management
    Inventory_Management.main()

def import_sales_tracking_module():
    """Import and execute the sales tracking module."""
    import sales_tracking
    sales_tracking.main()

def load_data():
    """
    Load data from the inventory.csv file and return a list of alerts for medicines that are about to expire or have low quantity.
    """
    alerts = []

    try:
        with open("inventory.csv", newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 5:
                    name, expiry_date, quantity, bin_location, price = row

                    # Check if the expiry date is approaching or less than a month
                    expiry_datetime = datetime.strptime(expiry_date, "%Y-%m-%d")
                    today = datetime.now()
                    one_month_from_now = today + timedelta(days=30)
                    if expiry_datetime <= today:
                        alert_text = f"ALERT: The medicine '{name}' has expired!"
                        alerts.append(alert_text)
                    elif expiry_datetime <= one_month_from_now:
                        days_left = (expiry_datetime - today).days
                        alert_text = f"ALERT: The medicine '{name}' will expire in {days_left} days!"
                        alerts.append(alert_text)

                    # Check if the quantity is less than 20
                    if int(quantity) < 20:
                        alert_text = f"ALERT: The quantity of '{name}' is less than 20!"
                        alerts.append(alert_text)

    except FileNotFoundError:
        pass

    return alerts

def open_alerts_window():
    """Open a new window to display the alerts."""
    alerts = load_data()

    alerts_window = tk.Toplevel(root)
    alerts_window.title("ALERTS")
    alerts_window.geometry("600x400")

    alerts_label = tk.Label(alerts_window, text="Alerts", font=("Arial", 20))
    alerts_label.pack(pady=10)

    # Create a text widget to display the alerts
    alerts_text = tk.Text(alerts_window, font=("Arial", 12), width=50, height=15)
    alerts_text.pack(padx=20, pady=20)

    # Display the alerts in the text widget
    for alert in alerts:
        alerts_text.insert(tk.END, alert + "\n")

    alerts_text.config(state=tk.DISABLED)  # Disable editing of the text widget

# Create the buttons for inventory, billing, sales tracking, and alerts
inventory_button = tk.Button(root, text="INVENTORY", font=("Arial", 20), width=25, height=5, bg="#272A37", fg="white", command=import_inventory_module)
billing_button = tk.Button(root, text="BILLING", font=("Arial", 20), width=25, height=5, bg="#272A37",  fg="white", command=import_billing_module)
track_button = tk.Button(root, text="TRACK SALES", font=("Arial", 20), width=25, height=5, bg="#272A37", fg="white", command=import_sales_tracking_module)
alerts_button = tk.Button(root, text="ALERTS", font=("Arial", 20), width=25, height=5, bg="#272A37", fg="white", command=open_alerts_window)

# Position the buttons on the root window
inventory_button.place(relx=.2, rely=0.5, anchor=tk.CENTER)
billing_button.place(relx=.5, rely=0.5, anchor=tk.CENTER)
track_button.place(relx=.8, rely=0.5, anchor=tk.CENTER)
alerts_button.place(relx=.5, rely=0.8, anchor=tk.CENTER)


root.protocol("WM_DELETE_WINDOW", lambda: exit())

# Run the main event loop
root.mainloop()
