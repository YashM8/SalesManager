import tkinter as tk
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

root = tk.Tk()
root.title("Grocery Store Management")


# Function to add an item to the database
def add_item():
    name = name_entry.get().strip().lower()
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
    c.execute("SELECT * FROM items")
    items = c.fetchall()

    # Update the inventory listbox
    inventory_listbox.delete(0, tk.END)
    for item in items:
        inventory_listbox.insert(tk.END, f"{item[1]} - {item[2]} - {item[3]}")


def update_item():
    pass


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

# Listbox to display inventory
inventory_listbox = tk.Listbox(root)
inventory_listbox.pack()
inventory_listbox.insert( tk.END, "Name - Quantity - Cost")

# Button to update inventory
update_button = tk.Button(root, text="Show Inventory", command=show_inventory)
update_button.pack()

root.mainloop()

# Close the database connection when the application is closed
conn.close()
