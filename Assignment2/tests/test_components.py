#!/usr/bin/env python3

import unittest
import tempfile
import os
from Assignment2.sales_model import SalesRecord
from Assignment2.sales_reader import read_sales_data

class TestComponents(unittest.TestCase):
    
    def test_sales_model_conversion_errors(self):
        """Test SalesRecord error handling in conversions"""
        # Test invalid int conversion
        self.assertEqual(SalesRecord._to_int("invalid"), 0)
        self.assertEqual(SalesRecord._to_int(None), 0)
        
        # Test invalid float conversion  
        self.assertEqual(SalesRecord._to_float("invalid"), 0.0)
        self.assertEqual(SalesRecord._to_float(None), 0.0)
        
        # Test valid conversions
        self.assertEqual(SalesRecord._to_int("123"), 123)
        self.assertEqual(SalesRecord._to_float("99.99"), 99.99)
    
    def test_sales_reader_file_not_found(self):
        """Test sales reader file not found error"""
        with self.assertRaises(FileNotFoundError):
            read_sales_data('nonexistent_file.csv')
    
    def test_sales_reader_malformed_data(self):
        """Test sales reader with malformed CSV data"""
        malformed_data = """product_id,product_name,category,price,quantity,sales_date,region
,,,invalid,invalid,,"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(malformed_data)
            f.flush()
            
            records = read_sales_data(f.name)
            # Should create record with default values due to error handling
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].price, 0.0)
            self.assertEqual(records[0].quantity, 0)
            
            os.remove(f.name)

if __name__ == "__main__":
    unittest.main()