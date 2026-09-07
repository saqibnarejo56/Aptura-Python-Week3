import csv
import json
from pathlib import Path
from uuid import uuid4

from models import Category, Product, StockTransaction


class Inventory:
    def __init__(self, data_file=None):
        if data_file is None:
            self.data_file = (
                Path(__file__).parent
                / "data"
                / "inventory.json"
            )
        else:
            self.data_file = Path(data_file)

        self.categories = []
        self.products = []
        self.transactions = []

        self.low_stock_threshold = 5

        self.load_data()

    def load_data(self):
        if not self.data_file.exists():
            self.save_data()
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError(
                    "Inventory data must be a JSON object."
                )

            categories = data.get("categories", [])
            products = data.get("products", [])
            transactions = data.get("transactions", [])
            settings = data.get("settings", {})

            if not isinstance(categories, list):
                raise ValueError(
                    "Categories must be stored as a list."
                )

            if not isinstance(products, list):
                raise ValueError(
                    "Products must be stored as a list."
                )

            if not isinstance(transactions, list):
                raise ValueError(
                    "Transactions must be stored as a list."
                )

            self.categories = [
                Category(
                    category_id=item["category_id"],
                    name=item["name"],
                    created_at=item.get("created_at"),
                    updated_at=item.get("updated_at")
                )
                for item in categories
            ]

            self.products = [
                Product(
                    product_id=item["product_id"],
                    name=item["name"],
                    category_id=item["category_id"],
                    price=float(item["price"]),
                    quantity=int(item["quantity"]),
                    created_at=item.get("created_at"),
                    updated_at=item.get("updated_at")
                )
                for item in products
            ]

            self.transactions = [
                StockTransaction(
                    transaction_id=item["transaction_id"],
                    product_id=item["product_id"],
                    transaction_type=item["transaction_type"],
                    quantity=int(item["quantity"]),
                    previous_quantity=int(
                        item["previous_quantity"]
                    ),
                    new_quantity=int(item["new_quantity"]),
                    timestamp=item.get("timestamp")
                )
                for item in transactions
            ]

            threshold = settings.get(
                "low_stock_threshold",
                5
            )

            if (
                isinstance(threshold, bool)
                or not isinstance(threshold, int)
                or threshold < 0
            ):
                threshold = 5

            self.low_stock_threshold = threshold

        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError
        ) as error:
            raise RuntimeError(
                f"Unable to load inventory data: {error}"
            ) from error

    def save_data(self):
        data = {
            "categories": [
                category.to_dict()
                for category in self.categories
            ],
            "products": [
                product.to_dict()
                for product in self.products
            ],
            "transactions": [
                transaction.to_dict()
                for transaction in self.transactions
            ],
            "settings": {
                "low_stock_threshold":
                    self.low_stock_threshold
            }
        }

        try:
            self.data_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with self.data_file.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    indent=4
                )

        except OSError as error:
            raise RuntimeError(
                f"Unable to save inventory data: {error}"
            ) from error

    def get_category(self, category_id):
        category_id = category_id.strip().upper()

        for category in self.categories:
            if category.category_id == category_id:
                return category

        return None

    def get_product(self, product_id):
        product_id = product_id.strip().upper()

        for product in self.products:
            if product.product_id == product_id:
                return product

        return None

    def add_category(self, category_id, name):
        category_id = category_id.strip().upper()
        name = name.strip()

        if not category_id:
            raise ValueError(
                "Category ID cannot be empty."
            )

        if not name:
            raise ValueError(
                "Category name cannot be empty."
            )

        if self.get_category(category_id):
            raise ValueError(
                f"Category ID '{category_id}' already exists."
            )

        for category in self.categories:
            if category.name.lower() == name.lower():
                raise ValueError(
                    f"Category '{name}' already exists."
                )

        category = Category(
            category_id,
            name
        )

        self.categories.append(category)
        self.save_data()

        return category

    def add_product(
        self,
        product_id,
        name,
        category_id,
        price,
        quantity
    ):
        product_id = product_id.strip().upper()
        name = name.strip()
        category_id = category_id.strip().upper()

        if not product_id:
            raise ValueError(
                "Product ID cannot be empty."
            )

        if not name:
            raise ValueError(
                "Product name cannot be empty."
            )

        if self.get_product(product_id):
            raise ValueError(
                f"Product ID '{product_id}' already exists."
            )

        if not self.get_category(category_id):
            raise ValueError(
                f"Category ID '{category_id}' does not exist."
            )

        self._validate_price(price)
        self._validate_quantity(quantity)

        product = Product(
            product_id,
            name,
            category_id,
            float(price),
            quantity
        )

        self.products.append(product)
        self.save_data()

        return product

    def update_product(
        self,
        product_id,
        name=None,
        category_id=None,
        price=None,
        quantity=None
    ):
        product = self.get_product(product_id)

        if not product:
            raise ValueError(
                f"Product ID '{product_id}' does not exist."
            )

        if name is not None:
            name = name.strip()

            if not name:
                raise ValueError(
                    "Product name cannot be empty."
                )

            product.name = name

        if category_id is not None:
            category_id = category_id.strip().upper()

            if not self.get_category(category_id):
                raise ValueError(
                    f"Category ID '{category_id}' does not exist."
                )

            product.category_id = category_id

        if price is not None:
            self._validate_price(price)
            product.price = float(price)

        if quantity is not None:
            self._validate_quantity(quantity)
            product.quantity = quantity

        product.touch()
        self.save_data()

        return product

    def remove_product(self, product_id):
        product = self.get_product(product_id)

        if not product:
            raise ValueError(
                f"Product ID '{product_id}' does not exist."
            )

        self.products.remove(product)
        self.save_data()

        return product

    def search_products(self, keyword):
        keyword = keyword.strip().lower()

        if not keyword:
            raise ValueError(
                "Search keyword cannot be empty."
            )

        results = []

        for product in self.products:
            category = self.get_category(
                product.category_id
            )

            category_name = (
                category.name
                if category
                else ""
            )

            if (
                keyword in product.product_id.lower()
                or keyword in product.name.lower()
                or keyword
                in product.category_id.lower()
                or keyword
                in category_name.lower()
            ):
                results.append(product)

        return results

    def stock_in(self, product_id, quantity):
        self._validate_stock_quantity(quantity)

        product = self.get_product(product_id)

        if not product:
            raise ValueError(
                f"Product ID '{product_id}' does not exist."
            )

        previous_quantity = product.quantity
        product.quantity += quantity
        product.touch()

        transaction = self._create_transaction(
            product=product,
            transaction_type="STOCK_IN",
            quantity=quantity,
            previous_quantity=previous_quantity
        )

        self.save_data()

        return transaction

    def stock_out(self, product_id, quantity):
        self._validate_stock_quantity(quantity)

        product = self.get_product(product_id)

        if not product:
            raise ValueError(
                f"Product ID '{product_id}' does not exist."
            )

        if quantity > product.quantity:
            raise ValueError(
                "Insufficient stock for this operation."
            )

        previous_quantity = product.quantity
        product.quantity -= quantity
        product.touch()

        transaction = self._create_transaction(
            product=product,
            transaction_type="STOCK_OUT",
            quantity=quantity,
            previous_quantity=previous_quantity
        )

        self.save_data()

        return transaction

    def _create_transaction(
        self,
        product,
        transaction_type,
        quantity,
        previous_quantity
    ):
        transaction = StockTransaction(
            transaction_id=uuid4().hex[:12].upper(),
            product_id=product.product_id,
            transaction_type=transaction_type,
            quantity=quantity,
            previous_quantity=previous_quantity,
            new_quantity=product.quantity
        )

        self.transactions.append(transaction)

        return transaction

    def get_transaction_history(
        self,
        product_id=None
    ):
        if product_id is None:
            return list(self.transactions)

        product_id = product_id.strip().upper()

        return [
            transaction
            for transaction in self.transactions
            if transaction.product_id == product_id
        ]

    def set_low_stock_threshold(self, threshold):
        if (
            isinstance(threshold, bool)
            or not isinstance(threshold, int)
        ):
            raise ValueError(
                "Low-stock threshold must be a whole number."
            )

        if threshold < 0:
            raise ValueError(
                "Low-stock threshold cannot be negative."
            )

        self.low_stock_threshold = threshold
        self.save_data()

    def filter_by_category(self, category_id):
        category_id = category_id.strip().upper()

        if not self.get_category(category_id):
            raise ValueError(
                f"Category ID '{category_id}' does not exist."
            )

        return [
            product
            for product in self.products
            if product.category_id == category_id
        ]

    def get_low_stock_products(self):
        return [
            product
            for product in self.products
            if (
                0 < product.quantity
                <= self.low_stock_threshold
            )
        ]

    def get_out_of_stock_products(self):
        return [
            product
            for product in self.products
            if product.quantity == 0
        ]

    def export_csv(self, output_file=None):
        if output_file is None:
            output_file = (
                Path(__file__).parent
                / "exports"
                / "inventory_export.csv"
            )
        else:
            output_file = Path(output_file)

        try:
            output_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with output_file.open(
                "w",
                newline="",
                encoding="utf-8"
            ) as file:
                writer = csv.writer(file)

                writer.writerow([
                    "Product ID",
                    "Name",
                    "Category ID",
                    "Category Name",
                    "Price",
                    "Quantity",
                    "Created At",
                    "Updated At"
                ])

                for product in self.products:
                    category = self.get_category(
                        product.category_id
                    )

                    writer.writerow([
                        product.product_id,
                        product.name,
                        product.category_id,
                        (
                            category.name
                            if category
                            else ""
                        ),
                        product.price,
                        product.quantity,
                        product.created_at,
                        product.updated_at
                    ])

        except OSError as error:
            raise RuntimeError(
                f"Unable to export CSV: {error}"
            ) from error

        return output_file

    def get_summary(self):
        total_products = len(self.products)

        total_units = sum(
            product.quantity
            for product in self.products
        )

        total_value = sum(
            product.price * product.quantity
            for product in self.products
        )

        return {
            "total_categories": len(self.categories),
            "total_products": total_products,
            "total_units": total_units,
            "total_inventory_value": round(
                total_value,
                2
            ),
            "low_stock_products": len(
                self.get_low_stock_products()
            ),
            "out_of_stock_products": len(
                self.get_out_of_stock_products()
            ),
            "low_stock_threshold":
                self.low_stock_threshold,
            "total_transactions":
                len(self.transactions)
        }

    @staticmethod
    def _validate_price(price):
        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
        ):
            raise ValueError(
                "Price must be a number."
            )

        if price <= 0:
            raise ValueError(
                "Price must be greater than 0."
            )

    @staticmethod
    def _validate_quantity(quantity):
        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
        ):
            raise ValueError(
                "Quantity must be a whole number."
            )

        if quantity < 0:
            raise ValueError(
                "Quantity cannot be negative."
            )

    @staticmethod
    def _validate_stock_quantity(quantity):
        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
        ):
            raise ValueError(
                "Stock quantity must be a whole number."
            )

        if quantity <= 0:
            raise ValueError(
                "Stock quantity must be greater than 0."
            )
