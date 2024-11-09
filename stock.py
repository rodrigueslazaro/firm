#!/usr/bin/python3
import json
import os
import re
import shutil
from datetime import datetime

# Paths
inventory_path = "./inventory/"
shopping_list_file = "shopping-list.md"
history_folder = "./history/"

def update_stock_from_shopping_list():
    """Update stock quantities based on the completed items in the shopping list."""
    # Regex pattern to find checked items in markdown
    item_pattern = re.compile(r'- \[x\] (\d+) (\w+) of (.+)')

    # Read the shopping list and find all checked items
    with open(shopping_list_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        match = item_pattern.match(line)
        if match:
            purchase_qty = int(match.group(1))
            purchase_unit = match.group(2)
            item_name = match.group(3)

            # Find the corresponding JSON file and update stock
            for filename in os.listdir(inventory_path):
                if filename.endswith(".json"):
                    filepath = os.path.join(inventory_path, filename)
                    with open(filepath, 'r+') as json_file:
                        inventory_data = json.load(json_file)
                        if inventory_data['name'] == item_name:
                            add_stock = inventory_data['purchase'].get('addStock', 0)
                            inventory_data['stock']['quantity'] += add_stock

                            # Write the updated data back to the JSON file
                            json_file.seek(0)
                            json.dump(inventory_data, json_file, ensure_ascii=False, indent=4)
                            json_file.truncate()
                            print(f"Updated {item_name}: added {add_stock} to stock.")

    # Move the shopping list to the history folder with a date prefix
    move_shopping_list_to_history()

def move_shopping_list_to_history():
    """Move the shopping list to the history folder with a date prefix."""
    # Ensure the history folder exists
    os.makedirs(history_folder, exist_ok=True)

    # Get the current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Construct the new file name
    new_filename = f"{current_date}-shopping-list.md"
    new_filepath = os.path.join(history_folder, new_filename)

    # Move the file
    shutil.move(shopping_list_file, new_filepath)
    print(f"Moved shopping list to {new_filepath}")

if __name__ == "__main__":
    update_stock_from_shopping_list()
