import json
import sys
from pathlib import Path

from pipeline import DataPipeline


def display_summary(summary):
    print()
    print("=" * 55)
    print("          AUTOMATED DATA PIPELINE SUMMARY")
    print("=" * 55)

    print(
        f"Total Records        : "
        f"{summary['total_records']}"
    )

    print(
        f"Valid Records        : "
        f"{summary['valid_records']}"
    )

    print(
        f"Invalid Records      : "
        f"{summary['invalid_records']}"
    )

    print(
        f"Valid Rate           : "
        f"{summary['valid_rate_percent']:.2f}%"
    )

    print(
        f"Total Sales Amount   : "
        f"{summary['total_sales_amount']:.2f}"
    )

    print(
        f"Average Order Value  : "
        f"{summary['average_order_value']:.2f}"
    )

    print(
        f"Minimum Order Value  : "
        f"{summary['minimum_order_value']:.2f}"
    )

    print(
        f"Maximum Order Value  : "
        f"{summary['maximum_order_value']:.2f}"
    )

    print()
    print("Records by City:")

    city_data = summary[
        "records_by_city"
    ]

    if city_data:
        for city, count in city_data.items():
            print(
                f"  {city:<15} : {count}"
            )

    else:
        print(
            "  No valid records."
        )

    print("=" * 55)


def main():
    project_root = Path(
        __file__
    ).resolve().parent

    # User can optionally provide CSV/JSON path:
    # python main.py data/raw_data.json
    if len(sys.argv) > 1:
        input_file = Path(
            sys.argv[1]
        )

        if not input_file.is_absolute():
            input_file = (
                project_root
                / input_file
            )

    else:
        input_file = (
            project_root
            / "data"
            / "raw_data.csv"
        )

    output_dir = (
        project_root
        / "output"
    )

    print()
    print("=" * 55)
    print("             AUTOMATED DATA PIPELINE")
    print("=" * 55)

    print(
        f"Input File : {input_file}"
    )

    try:
        pipeline = DataPipeline(
            input_file=input_file,
            output_dir=output_dir,
        )

        result = pipeline.run()

        display_summary(
            result["summary"]
        )

        print()
        print("Generated Files:")

        print(
            f"Clean Dataset : "
            f"{result['clean_file']}"
        )

        print(
            f"Error Log     : "
            f"{result['error_file']}"
        )

        print(
            f"Summary       : "
            f"{result['summary_file']}"
        )

        print()
        print(
            "Pipeline completed successfully."
        )

    except FileNotFoundError as error:
        print(
            f"\nPipeline failed: {error}"
        )

    except json.JSONDecodeError as error:
        print(
            "\nPipeline failed: "
            f"Invalid JSON data - {error}"
        )

    except ValueError as error:
        print(
            f"\nPipeline failed: {error}"
        )

    except OSError as error:
        print(
            f"\nPipeline failed: {error}"
        )


if __name__ == "__main__":
    main()
