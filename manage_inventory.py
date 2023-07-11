import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

conn = sqlite3.connect('store.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity INTEGER,
        cost REAL
    )
''')

conn.commit()


def add_item():
    name = name_entry.get().strip()
    quantity = int(quantity_entry.get())
    cost = float(cost_entry.get())

    c.execute("INSERT INTO items (name, quantity, cost) VALUES (?, ?, ?)", (name, quantity, cost))
    conn.commit()

    name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)


# Function to update inventory
def show_inventory():
    # Fetch all items from the database
    inventory_treeview.delete(*inventory_treeview.get_children())
    inventory_treeview.insert("", "end", values=("", "", ""), tags=("header",))

    c.execute("SELECT * FROM items")
    items = c.fetchall()

    # Update the inventory treeview
    for item in items:
        name = item[1].title()
        inventory_treeview.insert("", "end", values=(name, item[2], item[3]), tags=("item",))


def update_item():
    name = name_entry.get().strip()
    quantity = int(quantity_entry.get())
    cost = float(cost_entry.get())

    # Check if the item exists in the database
    c.execute("SELECT * FROM items WHERE name=?", (name,))
    item = c.fetchone()

    if item:
        # Update the quantity and cost of the item in the database
        c.execute("UPDATE items SET quantity=?, cost=? WHERE name=?", (quantity, cost, name))
        conn.commit()
        # Clear the entry fields
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        cost_entry.delete(0, tk.END)
        # Clear the inventory listbox
        inventory_treeview.delete(*inventory_treeview.get_children())
        show_inventory()
    else:
        # Display an error message if the item doesn't exist in the database
        error_message = "Item not found in the database."
        tk.messagebox.showerror("Error", error_message)


root = tk.Tk()
root.title("Grocery Store Management")
root.geometry("650x800")
font_style = ("Courier", 24)
root.option_add("*Font", font_style)

# Label and entry fields for item details
name_label = tk.Label(root, text="Item Name:")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

cost_label = tk.Label(root, text="Cost:")
cost_label.pack()
cost_entry = tk.Entry(root)
cost_entry.pack()

# Button to add item
add_button = tk.Button(root, text="Add Item", command=add_item)
add_button.pack()

update_button = tk.Button(root, text="Update Item", command=update_item)
update_button.pack()

# Label for inventory
inventory_label = tk.Label(root, text="Inventory:")
inventory_label.pack()

# Button to update inventory
update_button = tk.Button(root, text="Show Inventory", command=show_inventory)
update_button.pack()

# Listbox to display inventory
# inventory_listbox = tk.Listbox(root)
# inventory_listbox.pack()
# inventory_listbox.config(width=40, height=15)

inventory_treeview = ttk.Treeview(root, columns=("name", "quantity", "cost"))
inventory_treeview.heading("#0", text="")
inventory_treeview.heading("name", text="Name")
inventory_treeview.heading("quantity", text="Quantity")
inventory_treeview.heading("cost", text="Cost")

# Set the column widths
inventory_treeview.column("#0", width=0, stretch=tk.NO)
inventory_treeview.column("name", width=150, anchor=tk.W)
inventory_treeview.column("quantity", width=150, anchor=tk.CENTER)
inventory_treeview.column("cost", width=150, anchor=tk.E)

# # Apply tag configuration for header and items
inventory_treeview.tag_configure("header", font=('Courier', 20, 'bold'))
inventory_treeview.tag_configure("item", font=('Courier', 20))

# Create a Scrollbar widget
scrollbar = ttk.Scrollbar(root, orient="vertical", command=inventory_treeview.yview)
scrollbar.pack(side="right", fill="y")

# Create a scrollbar for the treeview
inventory_treeview.configure(yscrollcommand=scrollbar.set)
inventory_treeview.configure(height=20)  # Change the height as desired

# Grid layout for the treeview and scrollbar
inventory_treeview.pack()

root.mainloop()
# Close the database connection when the application is closed
conn.close()
