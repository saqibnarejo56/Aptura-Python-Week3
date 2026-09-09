import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline import DataPipeline


class TestDataPipeline(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.base_path = Path(
            self.temp_dir.name
        )

        self.output_dir = (
            self.base_path / "output"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_csv(
        self,
        rows,
        filename="test.csv"
    ):
        file_path = (
            self.base_path / filename
        )

        fieldnames = [
            "record_id",
            "customer_name",
            "email",
            "city",
            "order_date",
            "quantity",
            "unit_price",
        ]

        with file_path.open(
            "w",
            encoding="utf-8",
            newline=""
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(rows)

        return file_path

    def create_json(
        self,
        rows,
        filename="test.json"
    ):
        file_path = (
            self.base_path / filename
        )

        with file_path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                rows,
                file
            )

        return file_path

    def sample_valid_record(self):
        return {
            "record_id": "1001",
            "customer_name": "Saqib Narejo",
            "email": "saqib@gmail.com",
            "city": "Karachi",
            "order_date": "2026-09-01",
            "quantity": "2",
            "unit_price": "2500",
        }

    # -----------------------------------------------------
    # READING
    # -----------------------------------------------------

    def test_read_csv(self):
        file_path = self.create_csv(
            [self.sample_valid_record()]
        )

        pipeline = DataPipeline(
            file_path,
            self.output_dir
        )

        records = pipeline.read_data()

        self.assertEqual(
            len(records),
            1
        )

        self.assertEqual(
            records[0]["record_id"],
            "1001"
        )

    def test_read_json(self):
        file_path = self.create_json(
            [self.sample_valid_record()]
        )

        pipeline = DataPipeline(
            file_path,
            self.output_dir
        )

        records = pipeline.read_data()

        self.assertEqual(
            len(records),
            1
        )

        self.assertEqual(
            records[0]["customer_name"],
            "Saqib Narejo"
        )

    def test_missing_input_file_rejected(self):
        pipeline = DataPipeline(
            self.base_path / "missing.csv",
            self.output_dir
        )

        with self.assertRaises(
            FileNotFoundError
        ):
            pipeline.read_data()

    def test_unsupported_file_format_rejected(self):
        file_path = (
            self.base_path / "data.txt"
        )

        file_path.write_text(
            "test",
            encoding="utf-8"
        )

        pipeline = DataPipeline(
            file_path,
            self.output_dir
        )

        with self.assertRaises(
            ValueError
        ):
            pipeline.read_data()

    def test_json_must_be_list(self):
        file_path = self.create_json(
            {
                "record_id": "1001"
            }
        )

        pipeline = DataPipeline(
            file_path,
            self.output_dir
        )

        with self.assertRaises(
            ValueError
        ):
            pipeline.read_data()

    # -----------------------------------------------------
    # CLEANING
    # -----------------------------------------------------

    def test_clean_name(self):
        result = DataPipeline.clean_name(
            "  saqib narejo  "
        )

        self.assertEqual(
            result,
            "Saqib Narejo"
        )

    def test_clean_email(self):
        result = DataPipeline.clean_email(
            "  SAQIB@GMAIL.COM "
        )

        self.assertEqual(
            result,
            "saqib@gmail.com"
        )

    def test_clean_city(self):
        result = DataPipeline.clean_city(
            "  KARACHI "
        )

        self.assertEqual(
            result,
            "Karachi"
        )

    def test_clean_date(self):
        result = DataPipeline.clean_date(
            "2026/09/04"
        )

        self.assertEqual(
            result,
            "2026-09-04"
        )

    def test_clean_numeric_values(self):
        quantity = (
            DataPipeline.clean_quantity(
                " 3 "
            )
        )

        price = (
            DataPipeline.clean_price(
                " 1750.50 "
            )
        )

        self.assertEqual(
            quantity,
            3
        )

        self.assertEqual(
            price,
            1750.50
        )

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    def test_invalid_email_rejected(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        record = pipeline.clean_record(
            self.sample_valid_record()
        )

        record["email"] = (
            "invalid-email.com"
        )

        errors = (
            pipeline.validate_record(
                record
            )
        )

        self.assertIn(
            "invalid email format",
            errors
        )

    def test_zero_quantity_rejected(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        record = pipeline.clean_record(
            self.sample_valid_record()
        )

        record["quantity"] = 0

        errors = (
            pipeline.validate_record(
                record
            )
        )

        self.assertIn(
            "quantity must be a positive whole number",
            errors
        )

    def test_negative_price_rejected(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        record = pipeline.clean_record(
            self.sample_valid_record()
        )

        record["unit_price"] = -100

        errors = (
            pipeline.validate_record(
                record
            )
        )

        self.assertIn(
            "unit_price must be greater than 0",
            errors
        )

    def test_missing_name_rejected(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        record = pipeline.clean_record(
            self.sample_valid_record()
        )

        record[
            "customer_name"
        ] = ""

        errors = (
            pipeline.validate_record(
                record
            )
        )

        self.assertIn(
            "customer_name is required",
            errors
        )

    def test_duplicate_record_id_rejected(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        record = pipeline.clean_record(
            self.sample_valid_record()
        )

        first_errors = (
            pipeline.validate_record(
                record
            )
        )

        second_errors = (
            pipeline.validate_record(
                record
            )
        )

        self.assertEqual(
            first_errors,
            []
        )

        self.assertIn(
            "duplicate record_id",
            second_errors
        )

    # -----------------------------------------------------
    # PROCESSING
    # -----------------------------------------------------

    def test_process_valid_record(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        pipeline.raw_records = [
            self.sample_valid_record()
        ]

        clean, errors = (
            pipeline.process_records()
        )

        self.assertEqual(
            len(clean),
            1
        )

        self.assertEqual(
            len(errors),
            0
        )

    def test_total_amount_transformation(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        pipeline.raw_records = [
            self.sample_valid_record()
        ]

        clean, _ = (
            pipeline.process_records()
        )

        self.assertEqual(
            clean[0][
                "total_amount"
            ],
            5000.0
        )

    def test_invalid_record_goes_to_error_log(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        record = (
            self.sample_valid_record()
        )

        record["email"] = (
            "bad-email"
        )

        pipeline.raw_records = [
            record
        ]

        clean, errors = (
            pipeline.process_records()
        )

        self.assertEqual(
            len(clean),
            0
        )

        self.assertEqual(
            len(errors),
            1
        )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    def test_summary_statistics(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        pipeline.raw_records = [
            self.sample_valid_record()
        ]

        pipeline.process_records()

        summary = (
            pipeline.generate_summary()
        )

        self.assertEqual(
            summary["total_records"],
            1
        )

        self.assertEqual(
            summary["valid_records"],
            1
        )

        self.assertEqual(
            summary["invalid_records"],
            0
        )

        self.assertEqual(
            summary[
                "total_sales_amount"
            ],
            5000.0
        )

    # -----------------------------------------------------
    # EXPORTS
    # -----------------------------------------------------

    def test_clean_csv_export(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        pipeline.raw_records = [
            self.sample_valid_record()
        ]

        pipeline.process_records()

        output_file = (
            pipeline.export_clean_data()
        )

        self.assertTrue(
            output_file.exists()
        )

    def test_error_log_export(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        record = (
            self.sample_valid_record()
        )

        record["quantity"] = "0"

        pipeline.raw_records = [
            record
        ]

        pipeline.process_records()

        output_file = (
            pipeline.export_error_log()
        )

        self.assertTrue(
            output_file.exists()
        )

    def test_summary_json_export(self):
        pipeline = DataPipeline(
            "dummy.csv",
            self.output_dir
        )

        pipeline.raw_records = [
            self.sample_valid_record()
        ]

        pipeline.process_records()

        summary = (
            pipeline.generate_summary()
        )

        output_file = (
            pipeline.export_summary(
                summary
            )
        )

        self.assertTrue(
            output_file.exists()
        )

    # -----------------------------------------------------
    # FULL PIPELINE
    # -----------------------------------------------------

    def test_complete_csv_pipeline(self):
        file_path = self.create_csv(
            [self.sample_valid_record()]
        )

        pipeline = DataPipeline(
            file_path,
            self.output_dir
        )

        result = pipeline.run()

        self.assertEqual(
            result["summary"][
                "valid_records"
            ],
            1
        )

        self.assertTrue(
            result[
                "clean_file"
            ].exists()
        )

        self.assertTrue(
            result[
                "error_file"
            ].exists()
        )

        self.assertTrue(
            result[
                "summary_file"
            ].exists()
        )

    def test_complete_json_pipeline(self):
        file_path = self.create_json(
            [self.sample_valid_record()]
        )

        pipeline = DataPipeline(
            file_path,
            self.output_dir
        )

        result = pipeline.run()

        self.assertEqual(
            result["summary"][
                "valid_records"
            ],
            1
        )

        self.assertTrue(
            result[
                "clean_file"
            ].exists()
        )


if __name__ == "__main__":
    unittest.main()
