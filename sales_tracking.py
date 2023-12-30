import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk

def track_sales(file_name):
    global window
    daily_sales = {}
    weekly_sales = {}
    monthly_sales = {}
    sales_data = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            date = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            sale = float(row[7])
            daily_sales[date.date()] = daily_sales.get(date.date(), 0) + sale
            weekly_sales[date.strftime('%Y-%U')] = weekly_sales.get(date.strftime('%Y-%U'), 0) + sale
            monthly_sales[date.strftime('%Y-%m')] = monthly_sales.get(date.strftime('%Y-%m'), 0) + sale
            sales_data.append(row)

    # create tkinter window to display sales data
    window = tk.Tk()
    window.title("Sales Data")
    window.geometry("500x600")
    window.state('zoomed')

    # create entry field for user to input date
    date_label = tk.Label(window, text="\nEnter Date (YYYY-MM-DD for Daily, YYYY-WW for Weekly, YYYY-MM for Monthly):")
    date_label.pack()
    date_entry = tk.Entry(window)
    date_entry.pack()

    # create option menu to select daily, weekly, or monthly sales data
    options = ["Select", "Daily", "Weekly", "Monthly"]
    selected_option = tk.StringVar(window)
    selected_option.set(options[0])
    option_menu = ttk.OptionMenu(window, selected_option, options[0], *options)
    option_menu.pack()

    # create label to display sales data for selected date
    sales_label = tk.Label(window, text="")
    sales_label.pack()

    # create scrollbar
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # create treeview to display sales data from csv file
    columns = ["Bill No.", "Customer Name", "Phone Number", "Doctor Name", "Datetime", "Medicine", "Quantity", "Price"]
    treeview = ttk.Treeview(window, columns=columns, show="headings", height=35, yscrollcommand=scrollbar.set)
    for col in columns:
        treeview.heading(col, text=col)
        # Set the width of each column
        treeview.column(col, width=190)
    treeview.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=treeview.yview)  # Configure the scrollbar

    back_button = tk.Button(window, text="Back", font=("Arial", 12), command=close_window)
    back_button.place(x=1400, y=50)

    def update_treeview():
        # clear treeview
        treeview.delete(*treeview.get_children())

        # get selected date and option
        date = date_entry.get()
        option = selected_option.get()

        # filter sales data based on selected date and option
        filtered_data = []
        for row in sales_data:
            row_date = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            if option == "Daily" and row_date.date() == datetime.strptime(date, '%Y-%m-%d').date():
                filtered_data.append(row)
            elif option == "Weekly" and row_date.strftime('%Y-%U') == date:
                filtered_data.append(row)
            elif option == "Monthly" and row_date.strftime('%Y-%m') == date:
                filtered_data.append(row)

        # add filtered data to treeview
        for row in filtered_data:
            treeview.insert("", "end", values=row)

    def update_sales_label(*args):
        date = date_entry.get()
        if selected_option.get() == "Daily":
            sales = daily_sales.get(datetime.strptime(date, '%Y-%m-%d').date(), 0)
        elif selected_option.get() == "Weekly":
            sales = weekly_sales.get(date, 0)
        else:
            sales = monthly_sales.get(date, 0)
        sales_label.config(text=f"Sales: {sales}")
        update_treeview()

    # update sales label and treeview when option or date is changed
    selected_option.trace("w", update_sales_label)
    date_entry.bind("<Return>", update_sales_label)

    window.protocol("WM_DELETE_WINDOW", lambda: exit())

    window.mainloop()


def close_window():
    window.destroy()

window = None


def main():
    track_sales(r'/Users/tsrk04/Desktop/-_-/SSN/2ND SEM/software dev lab/Final_SDP/sales_data.csv')

if __name__ == '__main__':
    main()
