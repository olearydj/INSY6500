"""
Test 2b Data Generation - Main Orchestrator
Students run this to generate their unique dataset.
Grader uses --grader flag for verification statistics.
"""

import argparse
import sys
import numpy as np
from generate import (
    get_banner_id,
    create_products,
    generate_sales,
    add_data_quality_issues,
    save_data,
    print_verification_info
)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate Test 2b data')
    parser.add_argument('--grader', action='store_true',
                        help='Enable grader mode with verbose statistics (requires analyze.py)')
    args = parser.parse_args()

    # Get and validate Banner ID
    banner_id, verification_hash = get_banner_id()

    # Set seed for reproducibility with student's Banner ID
    np.random.seed(banner_id)

    # Generate data
    products = create_products()
    sales = generate_sales(products)

    # Add data quality issues
    sales = add_data_quality_issues(sales)

    # Run analysis if grader mode
    if args.grader:
        try:
            from analyze import analyze_generated_data
            analyze_generated_data(sales, products)
        except ImportError:
            print("\n⚠️  ERROR: Grader mode requires analyze.py (not included in student distribution)")
            sys.exit(1)

    # Save data
    save_data(products, sales)

    print("\n" + "=" * 70)
    print("FILES SAVED")
    print("=" * 70)
    print("✓ data/products.csv")
    print("✓ data/sales.csv")
    print("\nYour unique dataset is ready for Test 2b!")
    print("=" * 70)

    print_verification_info(banner_id, verification_hash)

if __name__ == "__main__":
    main()
