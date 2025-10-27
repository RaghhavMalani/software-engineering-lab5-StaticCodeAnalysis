import json
from datetime import datetime
# FIX (F401 / W0611): Removed unused 'import sys'

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Adds an item to the stock_data."""

    # FIX (W0102): Use None as default for mutable types
    if logs is None:
        logs = []

    if not item:
        return

    # FIX (Suggested): Add type checking for robustness
    if not isinstance(qty, int):
        print(f"Error: Quantity '{qty}' for item '{item}' is not a number.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty

    # FIX (C0209): Use f-string for formatting
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Removes a specified quantity of an item from stock."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    # FIX (W0702 / E722): Specify the exception type
    except KeyError:
        print(f"Error: Item '{item}' not found in inventory. Cannot remove.")
    # FIX (Suggested): Also good to catch type errors
    except TypeError:
        print(f"Error: Invalid quantity '{qty}' for item '{item}'.")


def get_qty(item):
    """Gets the current quantity of a specific item."""
    return stock_data.get(item, 0)  # Use .get() for safety


def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""

    global stock_data  # pylint: disable=global-statement
    # FIX (R1732 / W1514): Use 'with' statement and specify encoding
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        print(f"Info: '{file}' not found. Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode '{file}'. Starting with empty inventory.")
        stock_data = {}


def save_data(file="inventory.json"):
    """Saves the current inventory data to a JSON file."""

    # FIX (R1732 / W1514): Use 'with' statement and specify encoding
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)  # Add indent for readability


def print_data():
    """Prints a report of all items and their quantities."""
    print("--- Items Report ---")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------")


def check_low_items(threshold=5):
    """Returns a list of items below the given threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to run the inventory system demo."""
    load_data()  # Start by loading existing data

    # FIX (C0103): Renamed functions to snake_case
    add_item("apple", 10)
    add_item("banana", 20)
    add_item("orange", 15)

    # This call will now be handled gracefully by our type check
    add_item("milk", "ten")

    remove_item("apple", 3)
    remove_item("grape", 1)  # This will now print a safe error

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")

    print_data()
    save_data()

    # FIX (W0123 / B307): Removed dangerous 'eval()' call
    # eval("print('eval used')")
    print("Eval call removed for security.")


# FIX (F401): Removed unused 'import logging' from top of file

if __name__ == "__main__":
    main()

# FIX (C0304): Added final newline
