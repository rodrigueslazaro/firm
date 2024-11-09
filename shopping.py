#!/usr/bin/python3
import json
import os

# Path to inventory
inventory_path = "./inventory/"

def list_items_in_danger():
    """List all items in the inventory that are in their danger zone."""
    items_in_danger = []

    # Load each inventory item
    for filename in os.listdir(inventory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(inventory_path, filename)
            with open(filepath) as file:
                inventory_data = json.load(file)
                name = inventory_data['name']
                purchase_qty = inventory_data['purchase']['quantity']
                purchase_unit = inventory_data['purchase']['unit']
                danger_level = inventory_data['purchase'].get('danger', None)
                stock_qty = inventory_data['stock']['quantity']

                # Check if the item is in the danger zone
                if danger_level is not None and stock_qty <= danger_level:
                    items_in_danger.append((name, purchase_qty, purchase_unit))

    # Print items that are in danger
    if items_in_danger:
        print("🛒 Shopping list created!")
        with open("shopping-list.md", "a+") as file:
            file.write("### 🛒 Shopping List\n")
        for name, purchase_qty, purchase_unit in items_in_danger:
            with open("shopping-list.md", "a+") as file:
                file.write(f"- [ ] {purchase_qty} {purchase_unit} of {name}\n")
    else:
        print("No items are currently in the danger zone.")

if __name__ == "__main__":
    list_items_in_danger()
