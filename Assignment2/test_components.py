#!/usr/bin/env python3

from sales_model import SalesRecord
from sales_reader import read_sales_data

def test_sales_model():
    """Test SalesRecord model"""
    record = SalesRecord.from_row({
        'product_id': '1',
        'product_name': 'Test Product',
        'category': 'Electronics',
        'price': '99.99',
        'quantity': '2',
        'sales_date': '2024-01-01',
        'region': 'North'
    })
    print(f"✓ SalesRecord: {record.product_name}, Total: ${record.total_value}")

def test_sales_reader():
    """Test sales reader"""
    records = read_sales_data('sales_data.csv')
    print(f"✓ Reader loaded {len(records)} records")
    if records:
        print(f"  First record: {records[0].product_name}")

if __name__ == "__main__":
    test_sales_model()
    test_sales_reader()
    print("✓ All component tests passed")