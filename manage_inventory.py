import tkinter as tk
from tkinter import messagebox
import sqlite3

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
    inventory_listbox.insert(tk.END, "Name - Quantity - Cost")

    c.execute("SELECT * FROM items")
    items = c.fetchall()

    # Update the inventory listbox
    for item in items:
        inventory_listbox.insert(tk.END, f"{item[1].capitalize()} - {item[2]} - {item[3]}")

    inventory_listbox.delete(tk.END)


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
        inventory_listbox.delete(0, tk.END)
        # Update the inventory listbox with the updated item details
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
inventory_listbox = tk.Listbox(root)
inventory_listbox.pack()
inventory_listbox.config(width=40, height=15)

root.mainloop()

# Close the database connection when the application is closed
conn.close()
