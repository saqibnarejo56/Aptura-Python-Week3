from datetime import datetime


def current_timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


class Category:
    def __init__(
        self,
        category_id,
        name,
        created_at=None,
        updated_at=None
    ):
        self.category_id = category_id
        self.name = name
        self.created_at = created_at or current_timestamp()
        self.updated_at = updated_at or self.created_at

    def touch(self):
        self.updated_at = current_timestamp()

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class Product:
    def __init__(
        self,
        product_id,
        name,
        category_id,
        price,
        quantity,
        created_at=None,
        updated_at=None
    ):
        self.product_id = product_id
        self.name = name
        self.category_id = category_id
        self.price = price
        self.quantity = quantity
        self.created_at = created_at or current_timestamp()
        self.updated_at = updated_at or self.created_at

    def touch(self):
        self.updated_at = current_timestamp()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category_id": self.category_id,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class StockTransaction:
    def __init__(
        self,
        transaction_id,
        product_id,
        transaction_type,
        quantity,
        previous_quantity,
        new_quantity,
        timestamp=None
    ):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.previous_quantity = previous_quantity
        self.new_quantity = new_quantity
        self.timestamp = timestamp or current_timestamp()

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "product_id": self.product_id,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "previous_quantity": self.previous_quantity,
            "new_quantity": self.new_quantity,
            "timestamp": self.timestamp
        }
