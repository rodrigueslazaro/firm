#!/usr/bin/python3
import json
import os
import re
from wcwidth import wcswidth

# Path to inventory
inventory_path = "./inventory/"

# Regex pattern to detect ANSI escape codes
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def strip_ansi_codes(text):
    """Remove ANSI escape codes for accurate width calculation."""
    return ansi_escape.sub('', text)

def pad_string(text, width):
    """Pad a string to a specified width, considering wide characters."""
    clean_text = strip_ansi_codes(text)
    padding_needed = width - wcswidth(clean_text)
    return text + " " * padding_needed

def list_inventory():
    """List all items in the inventory with their current stock in a table format."""
    items = []

    # Load each inventory item
    for filename in os.listdir(inventory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(inventory_path, filename)
            with open(filepath) as file:
                inventory_data = json.load(file)
                name = inventory_data.get('name', filename.replace('.json', ''))
                stock_qty = inventory_data['stock']['quantity']
                stock_unit = inventory_data['stock']['unit']

                # Check if there is a danger level
                danger_level = inventory_data['purchase'].get('danger', None)

                # Format quantity, making it red if stock is low
                quantity_text = f"{stock_qty} {stock_unit}"
                if danger_level is not None and stock_qty <= danger_level:
                    quantity_text = f"\033[91m{quantity_text}\033[0m"  # Red color

                items.append((name, quantity_text))

    # Determine the longest item name and quantity length
    name_width = max(wcswidth(strip_ansi_codes(item[0])) for item in items) + 2
    qty_width = max(wcswidth(strip_ansi_codes(item[1])) for item in items) + 2

    # Print the table header
    print(f"| {pad_string('Item', name_width)} | {pad_string('Quantity', qty_width)} |")
    print(f"|{'-' * (name_width + 2)}|{'-' * (qty_width + 2)}|")

    # Print each item in the formatted table
    for name, quantity in items:
        print(f"| {pad_string(name, name_width)} | {pad_string(quantity, qty_width)} |")

if __name__ == "__main__":
    list_inventory()
