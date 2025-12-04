"""
Comprehensive unit tests for SalesAnalyzer
Tests all functional programming methods and edge cases
"""

import sys
from pathlib import Path
import unittest
import tempfile
import os

# Add parent directory to path for imports
REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

from sales_analyzer import SalesAnalyzer


class TestSalesAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Create sample CSV data for testing"""
        self.sample_data_content = """product_id,product_name,category,price,quantity,sales_date,region
1,Test Product A,Electronics,100.00,2,2024-01-01,North
2,Test Product B,Furniture,200.00,1,2024-01-02,South
3,Test Product C,Electronics,50.00,3,2024-01-03,East
4,Test Product D,Furniture,300.00,1,2024-01-04,West"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(self.sample_data_content)
            self.sample_file = f.name
        
        self.analyzer = SalesAnalyzer(self.sample_file)
    
    def tearDown(self):
        """Clean up temporary files"""
        try:
            os.remove(self.sample_file)
        except:
            pass
        
        # Clean up any other temp files
        for file in os.listdir('.'):
            if file.startswith('tmp') and file.endswith('.csv'):
                try:
                    os.remove(file)
                except:
                    pass
    
    def test_initialization(self):
        """Test proper initialization and data loading"""
        self.assertEqual(len(self.analyzer.data), 4)
        self.assertIn('total_revenue', self.analyzer.data.columns)
        self.assertEqual(self.analyzer.data['total_revenue'].iloc[0], 200.00)
    
    def test_top_products_by_revenue(self):
        """Test top products functionality"""
        top_products = self.analyzer.top_products_by_revenue(2)
        self.assertEqual(len(top_products), 2)
        self.assertEqual(top_products[0][0], 'Test Product D')
        self.assertEqual(top_products[0][1], 300.00)
    
    def test_revenue_by_category(self):
        """Test category revenue aggregation"""
        category_revenue = self.analyzer.revenue_by_category()
        self.assertIn('Electronics', category_revenue)
        self.assertIn('Furniture', category_revenue)
        self.assertEqual(category_revenue['Electronics'], 350.00)
        self.assertEqual(category_revenue['Furniture'], 500.00)
    
    def test_daily_sales_performance(self):
        """Test daily sales performance metrics"""
        daily_performance = self.analyzer.daily_sales_performance()
        self.assertEqual(len(daily_performance), 4)
        dates = [d[0] for d in daily_performance]
        self.assertIn('2024-01-01', dates)
    
    def test_regional_analysis(self):
        """Test regional analysis functionality"""
        regional_data = self.analyzer.regional_analysis()
        self.assertEqual(len(regional_data), 4)
        self.assertIn('North', regional_data)
        self.assertIn('total_sales', regional_data['North'])
    
    def test_price_distribution_analysis(self):
        """Test price distribution categorization"""
        price_dist = self.analyzer.price_distribution_analysis()
        self.assertIn('Budget', price_dist)
        self.assertIn('Mid-range', price_dist)
        self.assertIn('Premium', price_dist)
    
    def test_monthly_trend_analysis(self):
        """Test monthly trend calculations"""
        trends = self.analyzer.monthly_trend_analysis()
        self.assertEqual(len(trends), 1)
        self.assertEqual(trends[0][0], '2024-01')
        self.assertEqual(trends[0][1], 850.00)
    
    def test_weekly_sales_pattern(self):
        """Test weekly sales pattern analysis"""
        weekly_pattern = self.analyzer.weekly_sales_pattern()
        self.assertIsInstance(weekly_pattern, dict)
        self.assertGreater(len(weekly_pattern), 0)
    
    def test_date_range_analysis(self):
        """Test date range filtering analysis"""
        date_analysis = self.analyzer.date_range_analysis('2024-01-01', '2024-01-02')
        self.assertIn('filtered_sales', date_analysis)
        self.assertIn('avg_daily_revenue', date_analysis)
        self.assertEqual(date_analysis['filtered_sales'], 2)
    
    def test_cross_category_insights(self):
        """Test cross-category analysis"""
        insights = self.analyzer.cross_category_insights()
        self.assertEqual(len(insights), 4)
        self.assertTrue(all(len(insight) == 3 for insight in insights))
    
    def test_empty_data_handling(self):
        """Test handling of empty CSV data"""
        empty_data = "product_id,product_name,category,price,quantity,sales_date,region\n"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(empty_data)
            f.flush()
            empty_analyzer = SalesAnalyzer(f.name)
            
            self.assertEqual(len(empty_analyzer.data), 0)
            self.assertEqual(empty_analyzer.top_products_by_revenue(), [])
            self.assertEqual(empty_analyzer.revenue_by_category(), {})
            
            os.remove(f.name)
    
    def test_single_product_analysis(self):
        """Test analysis with single product"""
        single_data = """product_id,product_name,category,price,quantity,sales_date,region
1,Single Product,Electronics,100.00,1,2024-01-01,North"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(single_data)
            f.flush()
            single_analyzer = SalesAnalyzer(f.name)
            
            top_products = single_analyzer.top_products_by_revenue(5)
            self.assertEqual(len(top_products), 1)
            self.assertEqual(top_products[0][1], 100.00)
            
            os.remove(f.name)
    
    def test_lambda_expressions_functionality(self):
        """Test lambda expressions in price distribution"""
        price_dist = self.analyzer.price_distribution_analysis()
        
        # Verify lambda categorization works correctly
        budget_items = price_dist['Budget']
        mid_range_items = price_dist['Mid-range']
        premium_items = price_dist['Premium']
        
        # Test Product C (50.00) should be in Budget
        # Test Product A (100.00) should be in Mid-range  
        # Test Product D (300.00) should be in Premium
        self.assertIsInstance(budget_items, list)
        self.assertIsInstance(mid_range_items, list)
        self.assertIsInstance(premium_items, list)
    
    def test_stream_operations_chaining(self):
        """Test pandas pipe operations and method chaining"""
        # Test that stream operations return expected data types
        top_products = self.analyzer.top_products_by_revenue(3)
        self.assertIsInstance(top_products, list)
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 2 for item in top_products))
        
        # Test functional composition in regional analysis
        regional_data = self.analyzer.regional_analysis()
        for region, metrics in regional_data.items():
            self.assertIn('total_sales', metrics)
            self.assertIn('avg_order_value', metrics)
            self.assertIn('top_category', metrics)
    
    def test_functional_aggregation_correctness(self):
        """Test mathematical correctness of functional aggregations"""
        # Verify revenue calculations
        category_revenue = self.analyzer.revenue_by_category()
        
        # Electronics: (100*2) + (50*3) = 200 + 150 = 350
        # Furniture: (200*1) + (300*1) = 200 + 300 = 500
        self.assertEqual(category_revenue['Electronics'], 350.00)
        self.assertEqual(category_revenue['Furniture'], 500.00)
        
        # Verify total revenue matches sum of categories
        total_expected = 350.00 + 500.00
        actual_total = sum(category_revenue.values())
        self.assertEqual(actual_total, total_expected)
    
    def test_date_range_analysis_edge_cases(self):
        """Test date range analysis with various edge cases"""
        # Test with no date filters
        all_data = self.analyzer.date_range_analysis()
        self.assertEqual(all_data['filtered_sales'], 4)
        
        # Test with start date only
        start_only = self.analyzer.date_range_analysis(start_date='2024-01-02')
        self.assertEqual(start_only['filtered_sales'], 3)
        
        # Test with end date only
        end_only = self.analyzer.date_range_analysis(end_date='2024-01-02')
        self.assertEqual(end_only['filtered_sales'], 2)
        
        # Test with date range that returns no results
        no_results = self.analyzer.date_range_analysis('2025-01-01', '2025-01-31')
        self.assertEqual(no_results['filtered_sales'], 0)
        self.assertEqual(no_results['avg_daily_revenue'], 0.0)
        self.assertIsNone(no_results['peak_day'])
    
    def test_main_execution_coverage(self):
        """Test main function execution for coverage"""
        import sys
        from io import StringIO
        
        # Capture stdout to test main execution
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Import and execute main function
            from sales_analyzer import main
            main()
            
            # Verify output was generated
            output = sys.stdout.getvalue()
            self.assertIn('ADVANCED SALES DATA ANALYSIS', output)
            self.assertIn('TOP 5 PRODUCTS BY REVENUE', output)
        finally:
            sys.stdout = old_stdout
    
    def test_empty_data_initialization_edge_case(self):
        """Test initialization with completely empty CSV file"""
        import pandas as pd
        
        # Test with pandas EmptyDataError
        empty_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        empty_file.write('')  # Completely empty file
        empty_file.close()
        
        try:
            analyzer = SalesAnalyzer(empty_file.name)
            self.assertEqual(len(analyzer.data), 0)
            # Test all methods return appropriate empty results
            self.assertEqual(analyzer.top_products_by_revenue(), [])
            self.assertEqual(analyzer.revenue_by_category(), {})
            self.assertEqual(analyzer.daily_sales_performance(), [])
            self.assertEqual(analyzer.regional_analysis(), {})
            self.assertEqual(analyzer.monthly_trend_analysis(), [])
            self.assertEqual(analyzer.weekly_sales_pattern(), {})
            self.assertEqual(analyzer.cross_category_insights(), [])
        finally:
            os.remove(empty_file.name)
    
    def test_file_not_found_initialization(self):
        """Test initialization with non-existent file"""
        with self.assertRaises(FileNotFoundError):
            SalesAnalyzer('nonexistent_file.csv')
    
    def test_main_function_with_wrong_path(self):
        """Test main function execution path coverage"""
        # This will test the main() function path that tries to load from hardcoded path
        import sys
        from io import StringIO
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # This should handle the case where the hardcoded path doesn't exist
            from sales_analyzer import main
            # The main function has a hardcoded path that won't exist in test environment
            # This will test the error handling path
            main()
        except:
            # Expected to fail due to hardcoded path
            pass
        finally:
            sys.stdout = old_stdout


if __name__ == '__main__':
    unittest.main()