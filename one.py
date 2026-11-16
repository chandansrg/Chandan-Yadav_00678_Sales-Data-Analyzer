
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

REQUIRED_COLUMNS = [
    "Date", "Product", "Region", "Quantity", "Amount"
]


def load_sales(file_name):
    """Read and clean sales data from CSV."""

    path = Path(file_name)

    if not path.exists():
        print("Error: CSV file not found!")
        return None

    try:
        df = pd.read_csv(path, on_bad_lines="skip")
    except Exception as error:
        print("Error reading CSV:", error)
        return None

    df.columns = df.columns.astype(str).str.strip()

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        print("Missing columns:", missing)
        return None

    df = df[REQUIRED_COLUMNS].copy()

    # Clean text columns
    for col in ["Date", "Product", "Region"]:
        df[col] = df[col].astype("string").str.strip()

    # Convert numeric columns
    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"], errors="coerce"
    )

    # Remove invalid and incomplete rows
    before = len(df)

    df = df.dropna(subset=REQUIRED_COLUMNS)

    df = df[
        (df["Date"] != "") &
        (df["Product"] != "") &
        (df["Region"] != "")
    ]

    # Remove duplicate records
    df = df.drop_duplicates().copy()

    skipped = before - len(df)

    if skipped > 0:
        print(f"Rows skipped: {skipped}")

    if df.empty:
        print("No valid sales records found.")
        return None

    return df


def sales_summary(df):

    total_revenue = df["Amount"].sum()
    transactions = len(df)
    units_sold = df["Quantity"].sum()

    print("\n========== SALES SUMMARY ==========")

    print(f"Total Revenue : {total_revenue:g}")
    print(f"Transactions  : {transactions}")
    print(f"Units Sold    : {units_sold:g}")

    product_sales = (
        df.groupby("Product")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    if not product_sales.empty:
        print("Top product   :", product_sales.index[0])

    print("===================================\n")


def group_sales(df):

    print("\n--- Sales by Product ---")

    product_sales = df.groupby("Product")["Amount"].sum()

    print(product_sales.to_string())

    print("\n--- Sales by Region ---")

    region_sales = (
        df.groupby("Region")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print(region_sales.to_string())

    # Region-wise bar chart
    region_sales.plot(
        kind="bar",
        title="Region-wise Sales",
        xlabel="Region",
        ylabel="Sales Amount",
        rot=0
    )

    plt.tight_layout()
    plt.show()


def top_products(df):

    top = (
        df.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    print("\n--- TOP 5 SELLING PRODUCTS ---")

    print(top.to_string())


def display_charts(df):

    # Product-wise revenue bar chart
    product_sales = (
        df.groupby("Product")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    product_sales.plot(
        kind="bar",
        title="Product-wise Revenue",
        xlabel="Product",
        ylabel="Revenue",
        rot=0
    )

    plt.tight_layout()
    plt.show()

    # Daily sales line chart
    data = df.copy()

    data["Date"] = pd.to_datetime(
        data["Date"], errors="coerce"
    )

    data = data.dropna(subset=["Date"])

    if not data.empty:

        daily_sales = (
            data.groupby("Date")["Amount"]
            .sum()
            .sort_index()
        )

        daily_sales.plot(
            kind="line",
            marker="o",
            title="Daily Sales Trend",
            xlabel="Date",
            ylabel="Revenue"
        )

        plt.tight_layout()
        plt.show()

    else:
        print("No valid dates for line chart.")


def main():

    print("================================")
    print("       SALES DATA ANALYZER")
    print("================================")

    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = input(
            "Enter CSV filename (Enter for sales.csv): "
        ).strip()

        if not file_name:
            file_name = "sales.csv"

    df = load_sales(file_name)

    if df is None:
        return

    while True:

        print("\n========== MENU ==========")
        print("1. Sales Summary")
        print("2. Group Sales by Product and Region")
        print("3. Top 5 Selling Products")
        print("4. Display Bar and Line Charts")
        print("5. Exit")
        print("==========================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            sales_summary(df)

        elif choice == "2":
            group_sales(df)

        elif choice == "3":
            top_products(df)

        elif choice == "4":
            display_charts(df)

        elif choice == "5":
            print("Thank you for using Sales Data Analyzer!")
            break

        else:
            print("Invalid choice! Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
