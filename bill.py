import tkinter as tk
import sqlite3
from datetime import datetime
from bill_item import *

add_count = 1
calc_items = []


def add():
    global add_count

    name = item_entry.get().lower()
    quant = int(quantity_entry.get())

    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name=?", (name,))
    result = cursor.fetchall()

    calc_items.append(Item(result[0][1], quant, result[0][3]))

    cursor.execute("UPDATE items SET quantity = quantity - ? WHERE name = ?", (quant, name))
    conn.commit()

    item_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

    status_label.config(text=f"Added Item {add_count}")
    add_count += 1


def print_bill():
    bill_count = 0

    receipt_listbox.insert(tk.END, datetime.now().strftime("Date - %Y-%m-%d | %H:%M:%S"))
    receipt_listbox.insert(tk.END, "\n")

    receipt_listbox.insert(tk.END, "Name - Quantity - Cost")

    for thing in calc_items:
        bill_count += thing.quantity * thing.cost
        receipt_listbox.insert(tk.END, f"{thing.name} - {thing.quantity} - {thing.quantity * thing.cost}")

    receipt_listbox.insert(tk.END, "\n")
    receipt_listbox.insert(tk.END, f"Total Cost - {bill_count}")


root = tk.Tk()
root.title("Receipt")
root.geometry("650x800")
font_style = ("Courier", 24)
root.option_add("*Font", font_style)

# Adjusting font size

status_label = tk.Label(root, text="Status:")
status_label.pack()

item_label = tk.Label(root, text="Item Name:")
item_label.pack()

item_entry = tk.Entry(root)
item_entry.pack()

quantity_label = tk.Label(root, text="Enter Quantity:")
quantity_label.pack()

quantity_entry = tk.Entry(root)
quantity_entry.pack()

add_button = tk.Button(root, text="Add", command=add)
add_button.pack()

generate_button = tk.Button(root, text="Generate Receipt", command=print_bill)
generate_button.pack()

receipt_label = tk.Label(root, text="Receipt:")
receipt_label.pack()

receipt_listbox = tk.Listbox(root)
receipt_listbox.pack()
receipt_listbox.config(width=40, height=20)

root.mainloop()
