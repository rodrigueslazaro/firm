#!/usr/bin/python3
import json
import os
import sys

# Paths to inventory and recipes
inventory_path = "./inventory/"
recipe_path = "./recipe/"

def load_inventory(ingredient):
    """Load the inventory file for a specific ingredient."""
    with open(os.path.join(inventory_path, f"{ingredient}.json")) as file:
        return json.load(file)

def update_inventory(ingredient, inventory_data):
    """Write updated inventory data back to the ingredient's JSON file."""
    with open(os.path.join(inventory_path, f"{ingredient}.json"), 'w') as file:
        json.dump(inventory_data, file, ensure_ascii=False, indent=4)

def check_and_consume(recipe_name):
    """Check if ingredients for a recipe are available in stock and consume them if so."""
    # Load the recipe file
    try:
        with open(os.path.join(recipe_path, f"{recipe_name}.json")) as file:
            recipe = json.load(file)
    except FileNotFoundError:
        print(f"Recipe '{recipe_name}' not found.")
        return

    # Track missing items
    missing_items = []
    consumed_items = []
    recipe_name = recipe['name']

    print(f"Recipe: {recipe['name']}")
    print(f"Instructions: {recipe['instructions']}")
    print("Ingredients:")
    for ingredient, required_qty in recipe['ingredients'].items():
        item = load_inventory(ingredient)
        print(f"  - {required_qty} {item['name']}")
    # Check each ingredient's availability
    for ingredient, required_qty in recipe['ingredients'].items():
        try:
            inventory_data = load_inventory(ingredient)
        except FileNotFoundError:
            missing_items.append(f"{ingredient} (ingredient not found)")
            continue

        stock_qty = inventory_data['stock']['quantity']

        # Check if enough stock is available
        if stock_qty < required_qty:
            missing_items.append(f"missing {required_qty - stock_qty} {ingredient}")
        else:
            # Deduct the required quantity from stock
            inventory_data['stock']['quantity'] -= required_qty
            update_inventory(ingredient, inventory_data)
            consumed_items.append(f"-{required_qty} {inventory_data['name']}")

    # Display results
    if missing_items:
        print(f"Insufficient ingredients for {recipe_name}: " + ", ".join(missing_items))
    else:
        print(f"{recipe_name} consumed!")
        for consumption in consumed_items:
            print(consumption)

if __name__ == "__main__":
    # Ensure a recipe name was provided
    if len(sys.argv) < 2:
        print("Usage: python3 consume.py <recipe_name>")
        sys.exit(1)

    recipe_name = sys.argv[1]
    check_and_consume(recipe_name)
