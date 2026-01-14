from utils.file_handler import *
from utils.data_processor import *
from utils.api_handler import *
from utils.data_processor import generate_sales_report


def main():
    try:
        print("="*40)
        print("SALES ANALYTICS SYSTEM")
        print("="*40)

        raw = read_sales_data('data/sales_data.txt')
        print(f"✓ Read {len(raw)} records")

        parsed = parse_transactions(raw)
        valid, invalid, summary = validate_and_filter(parsed)

        print(f"✓ Valid: {len(valid)} | Invalid: {invalid}")

        print("✓ Running analysis...")
        calculate_total_revenue(valid)

        products = fetch_all_products()
        mapping = create_product_mapping(products)

        enriched = enrich_sales_data(valid, mapping)
        print(f"✓ Enriched {len(enriched)} records")

        generate_sales_report(valid, enriched)
        print("✓ Report saved to output/sales_report.txt")

        print("✓ Process complete")

    except Exception as e:
        print("❌ Error:", e)


if __name__ == "__main__":
    main()
