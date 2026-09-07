import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from inventory import Inventory


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.data_file = (
            Path(self.temp_dir.name)
            / "inventory.json"
        )

        self.inventory = Inventory(
            data_file=self.data_file
        )

        self.inventory.add_category(
            "C001",
            "Electronics"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def add_default_product(
        self,
        product_id="P001",
        quantity=10
    ):
        return self.inventory.add_product(
            product_id,
            "Keyboard",
            "C001",
            2500,
            quantity
        )

    def test_add_category(self):
        category = self.inventory.add_category(
            "C002",
            "Stationery"
        )

        self.assertEqual(
            category.category_id,
            "C002"
        )

        self.assertEqual(
            len(self.inventory.categories),
            2
        )

    def test_duplicate_category_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.add_category(
                "C001",
                "Another Category"
            )

    def test_add_product(self):
        product = self.add_default_product()

        self.assertEqual(
            product.product_id,
            "P001"
        )

        self.assertEqual(
            product.quantity,
            10
        )

    def test_duplicate_product_rejected(self):
        self.add_default_product()

        with self.assertRaises(ValueError):
            self.inventory.add_product(
                "P001",
                "Mouse",
                "C001",
                1500,
                5
            )

    def test_invalid_category_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.add_product(
                "P001",
                "Keyboard",
                "C999",
                2500,
                10
            )

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.add_product(
                "P001",
                "Keyboard",
                "C001",
                -100,
                10
            )

    def test_negative_quantity_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.add_product(
                "P001",
                "Keyboard",
                "C001",
                2500,
                -1
            )

    def test_update_product(self):
        self.add_default_product()

        product = self.inventory.update_product(
            "P001",
            price=3000,
            quantity=8
        )

        self.assertEqual(
            product.price,
            3000.0
        )

        self.assertEqual(
            product.quantity,
            8
        )

    def test_remove_product(self):
        self.add_default_product()

        removed = self.inventory.remove_product(
            "P001"
        )

        self.assertEqual(
            removed.product_id,
            "P001"
        )

        self.assertEqual(
            len(self.inventory.products),
            0
        )

    def test_search_product(self):
        self.add_default_product()

        results = self.inventory.search_products(
            "keyboard"
        )

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0].product_id,
            "P001"
        )

    def test_summary(self):
        self.add_default_product()

        self.inventory.add_product(
            "P002",
            "Mouse",
            "C001",
            1500,
            4
        )

        self.inventory.add_product(
            "P003",
            "Monitor",
            "C001",
            30000,
            0
        )

        summary = self.inventory.get_summary()

        self.assertEqual(
            summary["total_categories"],
            1
        )

        self.assertEqual(
            summary["total_products"],
            3
        )

        self.assertEqual(
            summary["total_units"],
            14
        )

        self.assertEqual(
            summary["total_inventory_value"],
            31000.0
        )

        self.assertEqual(
            summary["low_stock_products"],
            1
        )

        self.assertEqual(
            summary["out_of_stock_products"],
            1
        )

    def test_persistence(self):
        self.add_default_product()

        new_inventory = Inventory(
            data_file=self.data_file
        )

        self.assertEqual(
            len(new_inventory.products),
            1
        )

        self.assertEqual(
            new_inventory.products[0].name,
            "Keyboard"
        )

    def test_stock_in(self):
        product = self.add_default_product()

        transaction = self.inventory.stock_in(
            "P001",
            5
        )

        self.assertEqual(
            product.quantity,
            15
        )

        self.assertEqual(
            transaction.transaction_type,
            "STOCK_IN"
        )

        self.assertEqual(
            transaction.previous_quantity,
            10
        )

        self.assertEqual(
            transaction.new_quantity,
            15
        )

    def test_stock_out(self):
        product = self.add_default_product()

        transaction = self.inventory.stock_out(
            "P001",
            4
        )

        self.assertEqual(
            product.quantity,
            6
        )

        self.assertEqual(
            transaction.transaction_type,
            "STOCK_OUT"
        )

        self.assertEqual(
            transaction.previous_quantity,
            10
        )

        self.assertEqual(
            transaction.new_quantity,
            6
        )

    def test_insufficient_stock_rejected(self):
        product = self.add_default_product()

        with self.assertRaises(ValueError):
            self.inventory.stock_out(
                "P001",
                50
            )

        self.assertEqual(
            product.quantity,
            10
        )

    def test_invalid_stock_quantity_rejected(self):
        self.add_default_product()

        with self.assertRaises(ValueError):
            self.inventory.stock_in(
                "P001",
                0
            )

        with self.assertRaises(ValueError):
            self.inventory.stock_out(
                "P001",
                -1
            )

    def test_transaction_history(self):
        self.add_default_product()

        self.inventory.stock_in(
            "P001",
            5
        )

        self.inventory.stock_out(
            "P001",
            2
        )

        history = (
            self.inventory.get_transaction_history(
                "P001"
            )
        )

        self.assertEqual(
            len(history),
            2
        )

        self.assertEqual(
            history[0].transaction_type,
            "STOCK_IN"
        )

        self.assertEqual(
            history[1].transaction_type,
            "STOCK_OUT"
        )

    def test_transaction_persistence(self):
        self.add_default_product()

        self.inventory.stock_in(
            "P001",
            5
        )

        new_inventory = Inventory(
            data_file=self.data_file
        )

        self.assertEqual(
            len(new_inventory.transactions),
            1
        )

        self.assertEqual(
            new_inventory.transactions[0].new_quantity,
            15
        )

    def test_set_low_stock_threshold(self):
        self.inventory.set_low_stock_threshold(
            10
        )

        self.assertEqual(
            self.inventory.low_stock_threshold,
            10
        )

    def test_negative_threshold_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.set_low_stock_threshold(
                -1
            )

    def test_filter_by_category(self):
        self.add_default_product()

        self.inventory.add_category(
            "C002",
            "Stationery"
        )

        self.inventory.add_product(
            "P002",
            "Notebook",
            "C002",
            300,
            10
        )

        results = self.inventory.filter_by_category(
            "C002"
        )

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0].product_id,
            "P002"
        )

    def test_low_stock_filter(self):
        self.add_default_product(
            "P001",
            4
        )

        self.inventory.add_product(
            "P002",
            "Mouse",
            "C001",
            1500,
            10
        )

        results = (
            self.inventory.get_low_stock_products()
        )

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0].product_id,
            "P001"
        )

    def test_out_of_stock_filter(self):
        self.add_default_product(
            "P001",
            0
        )

        results = (
            self.inventory.get_out_of_stock_products()
        )

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0].product_id,
            "P001"
        )

    def test_csv_export(self):
        self.add_default_product()

        output_file = (
            Path(self.temp_dir.name)
            / "inventory_export.csv"
        )

        result = self.inventory.export_csv(
            output_file
        )

        self.assertTrue(
            result.exists()
        )

        content = result.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Product ID",
            content
        )

        self.assertIn(
            "Keyboard",
            content
        )

        self.assertIn(
            "Electronics",
            content
        )

    def test_product_timestamps_created(self):
        product = self.add_default_product()

        self.assertTrue(
            product.created_at
        )

        self.assertTrue(
            product.updated_at
        )


if __name__ == "__main__":
    unittest.main()
