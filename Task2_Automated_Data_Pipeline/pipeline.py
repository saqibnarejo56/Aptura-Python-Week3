import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Union


class DataPipeline:
    REQUIRED_FIELDS = [
        "record_id",
        "customer_name",
        "email",
        "city",
        "order_date",
        "quantity",
        "unit_price",
    ]

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    def __init__(
        self,
        input_file: Union[str, Path],
        output_dir: Union[str, Path] = "output",
    ):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)

        self.raw_records = []
        self.clean_records = []
        self.error_records = []

        self.seen_record_ids = set()

    # ---------------------------------------------------------
    # READ DATA
    # ---------------------------------------------------------

    def read_data(self):
        if not self.input_file.exists():
            raise FileNotFoundError(
                f"Input file not found: {self.input_file}"
            )

        extension = self.input_file.suffix.lower()

        if extension == ".csv":
            self.raw_records = self._read_csv()

        elif extension == ".json":
            self.raw_records = self._read_json()

        else:
            raise ValueError(
                "Unsupported file format. Only CSV and JSON are supported."
            )

        return self.raw_records

    def _read_csv(self):
        with self.input_file.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError(
                    "CSV file is empty or does not contain headers."
                )

            missing_fields = [
                field
                for field in self.REQUIRED_FIELDS
                if field not in reader.fieldnames
            ]

            if missing_fields:
                raise ValueError(
                    "CSV is missing required columns: "
                    + ", ".join(missing_fields)
                )

            return list(reader)

    def _read_json(self):
        with self.input_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "JSON input must contain a list of records."
            )

        for record_number, record in enumerate(data, start=1):
            if not isinstance(record, dict):
                raise ValueError(
                    f"JSON record {record_number} must be an object."
                )

        return data

    # ---------------------------------------------------------
    # CLEANING
    # ---------------------------------------------------------

    @staticmethod
    def clean_text(value):
        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def clean_name(value):
        return DataPipeline.clean_text(value).title()

    @staticmethod
    def clean_email(value):
        return DataPipeline.clean_text(value).lower()

    @staticmethod
    def clean_city(value):
        return DataPipeline.clean_text(value).title()

    @staticmethod
    def clean_date(value):
        value = DataPipeline.clean_text(value)

        accepted_formats = (
            "%Y-%m-%d",
            "%Y/%m/%d",
        )

        for date_format in accepted_formats:
            try:
                parsed_date = datetime.strptime(
                    value,
                    date_format,
                )

                return parsed_date.strftime("%Y-%m-%d")

            except ValueError:
                continue

        return value

    @staticmethod
    def clean_quantity(value):
        value = DataPipeline.clean_text(value)

        try:
            return int(value)

        except (ValueError, TypeError):
            return value

    @staticmethod
    def clean_price(value):
        value = DataPipeline.clean_text(value)

        try:
            return float(value)

        except (ValueError, TypeError):
            return value

    def clean_record(self, record):
        return {
            "record_id": self.clean_text(
                record.get("record_id")
            ),
            "customer_name": self.clean_name(
                record.get("customer_name")
            ),
            "email": self.clean_email(
                record.get("email")
            ),
            "city": self.clean_city(
                record.get("city")
            ),
            "order_date": self.clean_date(
                record.get("order_date")
            ),
            "quantity": self.clean_quantity(
                record.get("quantity")
            ),
            "unit_price": self.clean_price(
                record.get("unit_price")
            ),
        }

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def validate_record(self, record):
        errors = []

        # Required fields
        for field in self.REQUIRED_FIELDS:
            value = record.get(field)

            if value is None or value == "":
                errors.append(
                    f"{field} is required"
                )

        # Duplicate ID validation
        record_id = record.get("record_id", "")

        if record_id:
            if record_id in self.seen_record_ids:
                errors.append(
                    "duplicate record_id"
                )
            else:
                self.seen_record_ids.add(record_id)

        # Email validation
        email = record.get("email", "")

        if email:
            if not self.EMAIL_PATTERN.fullmatch(
                str(email)
            ):
                errors.append(
                    "invalid email format"
                )

        # Date validation
        order_date = record.get(
            "order_date",
            "",
        )

        if order_date:
            try:
                datetime.strptime(
                    str(order_date),
                    "%Y-%m-%d",
                )

            except ValueError:
                errors.append(
                    "invalid order_date"
                )

        # Quantity validation
        quantity = record.get("quantity")

        if quantity != "":
            if (
                not isinstance(quantity, int)
                or isinstance(quantity, bool)
                or quantity <= 0
            ):
                errors.append(
                    "quantity must be a positive whole number"
                )

        # Price validation
        unit_price = record.get(
            "unit_price"
        )

        if unit_price != "":
            if (
                not isinstance(
                    unit_price,
                    (int, float),
                )
                or isinstance(unit_price, bool)
                or unit_price <= 0
            ):
                errors.append(
                    "unit_price must be greater than 0"
                )

        return errors

    # ---------------------------------------------------------
    # PROCESS RECORDS
    # ---------------------------------------------------------

    def process_records(self):
        self.clean_records = []
        self.error_records = []
        self.seen_record_ids = set()

        for record_number, raw_record in enumerate(
            self.raw_records,
            start=1,
        ):
            cleaned_record = self.clean_record(
                raw_record
            )

            errors = self.validate_record(
                cleaned_record
            )

            if errors:
                self.error_records.append(
                    {
                        "record_number": record_number,
                        "record_id": cleaned_record.get(
                            "record_id",
                            "",
                        ),
                        "errors": "; ".join(
                            errors
                        ),
                        "raw_record": json.dumps(
                            raw_record,
                            ensure_ascii=False,
                        ),
                    }
                )

                continue

            quantity = cleaned_record[
                "quantity"
            ]

            unit_price = cleaned_record[
                "unit_price"
            ]

            # Transform numeric values
            cleaned_record[
                "unit_price"
            ] = round(
                unit_price,
                2,
            )

            # Derived field
            cleaned_record[
                "total_amount"
            ] = round(
                quantity * unit_price,
                2,
            )

            self.clean_records.append(
                cleaned_record
            )

        return (
            self.clean_records,
            self.error_records,
        )

    # ---------------------------------------------------------
    # SUMMARY STATISTICS
    # ---------------------------------------------------------

    def generate_summary(self):
        total_records = len(
            self.raw_records
        )

        valid_records = len(
            self.clean_records
        )

        invalid_records = len(
            self.error_records
        )

        amounts = [
            record["total_amount"]
            for record in self.clean_records
        ]

        city_counts = Counter(
            record["city"]
            for record in self.clean_records
        )

        total_sales = round(
            sum(amounts),
            2,
        )

        if valid_records:
            average_order_value = round(
                total_sales / valid_records,
                2,
            )
        else:
            average_order_value = 0

        if total_records:
            valid_rate = round(
                (
                    valid_records
                    / total_records
                )
                * 100,
                2,
            )
        else:
            valid_rate = 0

        if amounts:
            minimum_order_value = round(
                min(amounts),
                2,
            )

            maximum_order_value = round(
                max(amounts),
                2,
            )

        else:
            minimum_order_value = 0
            maximum_order_value = 0

        return {
            "total_records": total_records,
            "valid_records": valid_records,
            "invalid_records": invalid_records,
            "valid_rate_percent": valid_rate,
            "total_sales_amount": total_sales,
            "average_order_value": average_order_value,
            "minimum_order_value": minimum_order_value,
            "maximum_order_value": maximum_order_value,
            "records_by_city": dict(
                sorted(
                    city_counts.items()
                )
            ),
        }

    # ---------------------------------------------------------
    # EXPORT CLEAN DATASET
    # ---------------------------------------------------------

    def export_clean_data(
        self,
        filename="cleaned_data.csv",
    ):
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = (
            self.output_dir / filename
        )

        fieldnames = [
            "record_id",
            "customer_name",
            "email",
            "city",
            "order_date",
            "quantity",
            "unit_price",
            "total_amount",
        ]

        with output_file.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            writer.writerows(
                self.clean_records
            )

        return output_file

    # ---------------------------------------------------------
    # EXPORT ERROR LOG
    # ---------------------------------------------------------

    def export_error_log(
        self,
        filename="error_log.csv",
    ):
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = (
            self.output_dir / filename
        )

        fieldnames = [
            "record_number",
            "record_id",
            "errors",
            "raw_record",
        ]

        with output_file.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            writer.writerows(
                self.error_records
            )

        return output_file

    # ---------------------------------------------------------
    # EXPORT SUMMARY
    # ---------------------------------------------------------

    def export_summary(
        self,
        summary,
        filename="summary.json",
    ):
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = (
            self.output_dir / filename
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                summary,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output_file

    # ---------------------------------------------------------
    # COMPLETE PIPELINE
    # ---------------------------------------------------------

    def run(self):
        self.read_data()

        self.process_records()

        summary = self.generate_summary()

        clean_file = (
            self.export_clean_data()
        )

        error_file = (
            self.export_error_log()
        )

        summary_file = (
            self.export_summary(summary)
        )

        return {
            "summary": summary,
            "clean_file": clean_file,
            "error_file": error_file,
            "summary_file": summary_file,
        }
