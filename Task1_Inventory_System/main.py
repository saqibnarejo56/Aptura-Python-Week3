from inventory import Inventory


def display_products(inventory, products):
    if not products:
        print("\nNo products found.")
        return

    print(
        "\n"
        f"{'ID':<10}"
        f"{'Name':<25}"
        f"{'Category':<20}"
        f"{'Price':<15}"
        f"{'Quantity':<10}"
    )

    print("-" * 80)

    for product in products:
        category = inventory.get_category(
            product.category_id
        )

        category_name = (
            category.name
            if category
            else product.category_id
        )

        print(
            f"{product.product_id:<10}"
            f"{product.name:<25}"
            f"{category_name:<20}"
            f"{product.price:<15.2f}"
            f"{product.quantity:<10}"
        )


def display_transactions(transactions):
    if not transactions:
        print("\nNo stock transactions found.")
        return

    print(
        "\n"
        f"{'Transaction ID':<16}"
        f"{'Product':<12}"
        f"{'Type':<12}"
        f"{'Qty':<8}"
        f"{'Before':<10}"
        f"{'After':<10}"
        f"{'Timestamp'}"
    )

    print("-" * 100)

    for transaction in transactions:
        print(
            f"{transaction.transaction_id:<16}"
            f"{transaction.product_id:<12}"
            f"{transaction.transaction_type:<12}"
            f"{transaction.quantity:<8}"
            f"{transaction.previous_quantity:<10}"
            f"{transaction.new_quantity:<10}"
            f"{transaction.timestamp}"
        )


def add_category(inventory):
    print("\n--- Add Category ---")

    category_id = input(
        "Category ID: "
    )

    name = input(
        "Category Name: "
    )

    category = inventory.add_category(
        category_id,
        name
    )

    print(
        f"Category '{category.name}' added successfully."
    )


def add_product(inventory):
    print("\n--- Add Product ---")

    product_id = input(
        "Product ID: "
    )

    name = input(
        "Product Name: "
    )

    category_id = input(
        "Category ID: "
    )

    try:
        price = float(
            input("Price: ")
        )

        quantity = int(
            input("Initial Quantity: ")
        )

    except ValueError:
        raise ValueError(
            "Price and quantity must contain valid numbers."
        )

    product = inventory.add_product(
        product_id,
        name,
        category_id,
        price,
        quantity
    )

    print(
        f"Product '{product.name}' added successfully."
    )


def update_product(inventory):
    print("\n--- Update Product ---")

    product_id = input(
        "Product ID to update: "
    )

    product = inventory.get_product(
        product_id
    )

    if not product:
        raise ValueError(
            f"Product ID '{product_id}' does not exist."
        )

    print(
        "Press Enter to keep the existing value."
    )

    print(
        "Use Stock In / Stock Out to change inventory quantity."
    )

    name = input(
        f"Name [{product.name}]: "
    ).strip()

    category_id = input(
        f"Category ID [{product.category_id}]: "
    ).strip()

    price_input = input(
        f"Price [{product.price}]: "
    ).strip()

    price = None

    if price_input:
        try:
            price = float(price_input)
        except ValueError:
            raise ValueError(
                "Price must be a valid number."
            )

    inventory.update_product(
        product_id,
        name=name or None,
        category_id=category_id or None,
        price=price
    )

    print(
        "Product updated successfully."
    )


def remove_product(inventory):
    print("\n--- Remove Product ---")

    product_id = input(
        "Product ID to remove: "
    )

    product = inventory.remove_product(
        product_id
    )

    print(
        f"Product '{product.name}' removed successfully."
    )


def search_products(inventory):
    print("\n--- Search Products ---")

    keyword = input(
        "Enter ID, name or category: "
    )

    results = inventory.search_products(
        keyword
    )

    display_products(
        inventory,
        results
    )


def show_summary(inventory):
    summary = inventory.get_summary()

    print("\n--- Inventory Summary ---")

    print(
        "Total Categories:",
        summary["total_categories"]
    )

    print(
        "Total Products:",
        summary["total_products"]
    )

    print(
        "Total Units:",
        summary["total_units"]
    )

    print(
        "Total Inventory Value:",
        f"{summary['total_inventory_value']:.2f}"
    )

    print(
        "Low Stock Threshold:",
        summary["low_stock_threshold"]
    )

    print(
        "Low Stock Products:",
        summary["low_stock_products"]
    )

    print(
        "Out of Stock Products:",
        summary["out_of_stock_products"]
    )

    print(
        "Stock Transactions:",
        summary["total_transactions"]
    )


def stock_in(inventory):
    print("\n--- Stock In ---")

    product_id = input(
        "Product ID: "
    )

    try:
        quantity = int(
            input("Quantity to add: ")
        )
    except ValueError:
        raise ValueError(
            "Stock quantity must be a whole number."
        )

    transaction = inventory.stock_in(
        product_id,
        quantity
    )

    print("\nStock added successfully.")
    print(
        "Product ID:",
        transaction.product_id
    )
    print(
        "Previous Quantity:",
        transaction.previous_quantity
    )
    print(
        "Added Quantity:",
        transaction.quantity
    )
    print(
        "New Quantity:",
        transaction.new_quantity
    )
    print(
        "Transaction ID:",
        transaction.transaction_id
    )


def stock_out(inventory):
    print("\n--- Stock Out ---")

    product_id = input(
        "Product ID: "
    )

    try:
        quantity = int(
            input("Quantity to remove: ")
        )
    except ValueError:
        raise ValueError(
            "Stock quantity must be a whole number."
        )

    transaction = inventory.stock_out(
        product_id,
        quantity
    )

    print("\nStock removed successfully.")
    print(
        "Product ID:",
        transaction.product_id
    )
    print(
        "Previous Quantity:",
        transaction.previous_quantity
    )
    print(
        "Removed Quantity:",
        transaction.quantity
    )
    print(
        "New Quantity:",
        transaction.new_quantity
    )
    print(
        "Transaction ID:",
        transaction.transaction_id
    )


def show_transaction_history(inventory):
    print("\n--- Stock Transaction History ---")

    product_id = input(
        "Product ID (press Enter for all): "
    ).strip()

    if product_id:
        if not inventory.get_product(product_id):
            raise ValueError(
                f"Product ID '{product_id}' does not exist."
            )

        transactions = (
            inventory.get_transaction_history(
                product_id
            )
        )

    else:
        transactions = (
            inventory.get_transaction_history()
        )

    display_transactions(
        transactions
    )


def change_low_stock_threshold(inventory):
    print("\n--- Low-Stock Threshold ---")

    print(
        "Current Threshold:",
        inventory.low_stock_threshold
    )

    try:
        threshold = int(
            input("New Threshold: ")
        )
    except ValueError:
        raise ValueError(
            "Low-stock threshold must be a whole number."
        )

    inventory.set_low_stock_threshold(
        threshold
    )

    print(
        f"Low-stock threshold changed to {threshold}."
    )


def filter_products(inventory):
    print("\n--- Filter Products ---")

    print("1. Filter by Category")
    print("2. Show Low-Stock Products")
    print("3. Show Out-of-Stock Products")

    choice = input(
        "\nSelect filter: "
    ).strip()

    if choice == "1":
        category_id = input(
            "Category ID: "
        )

        products = inventory.filter_by_category(
            category_id
        )

        display_products(
            inventory,
            products
        )

    elif choice == "2":
        products = (
            inventory.get_low_stock_products()
        )

        display_products(
            inventory,
            products
        )

    elif choice == "3":
        products = (
            inventory.get_out_of_stock_products()
        )

        display_products(
            inventory,
            products
        )

    else:
        print(
            "\nInvalid filter option."
        )


def export_inventory(inventory):
    print("\n--- Export Inventory ---")

    output_file = inventory.export_csv()

    print(
        "Inventory exported successfully."
    )

    print(
        "File:",
        output_file
    )


def show_menu():
    print("\n" + "=" * 48)
    print("       OBJECT-ORIENTED INVENTORY SYSTEM")
    print("=" * 48)

    print("1.  Add Category")
    print("2.  Add Product")
    print("3.  Update Product")
    print("4.  Remove Product")
    print("5.  Search Products")
    print("6.  View All Products")
    print("7.  Inventory Summary")
    print("8.  Stock In")
    print("9.  Stock Out")
    print("10. Transaction History")
    print("11. Set Low-Stock Threshold")
    print("12. Filter Products")
    print("13. Export Inventory to CSV")
    print("0.  Exit")


def main():
    try:
        inventory = Inventory()

    except RuntimeError as error:
        print(
            "Startup Error:",
            error
        )
        return

    while True:
        show_menu()

        choice = input(
            "\nSelect an option: "
        ).strip()

        try:
            if choice == "1":
                add_category(inventory)

            elif choice == "2":
                add_product(inventory)

            elif choice == "3":
                update_product(inventory)

            elif choice == "4":
                remove_product(inventory)

            elif choice == "5":
                search_products(inventory)

            elif choice == "6":
                display_products(
                    inventory,
                    inventory.products
                )

            elif choice == "7":
                show_summary(inventory)

            elif choice == "8":
                stock_in(inventory)

            elif choice == "9":
                stock_out(inventory)

            elif choice == "10":
                show_transaction_history(
                    inventory
                )

            elif choice == "11":
                change_low_stock_threshold(
                    inventory
                )

            elif choice == "12":
                filter_products(
                    inventory
                )

            elif choice == "13":
                export_inventory(
                    inventory
                )

            elif choice == "0":
                print(
                    "\nInventory system closed successfully."
                )
                break

            else:
                print(
                    "\nInvalid option. Please select 0 to 13."
                )

        except (
            ValueError,
            RuntimeError
        ) as error:
            print(
                f"\nError: {error}"
            )


if __name__ == "__main__":
    main()
