"""
Advanced Sales Data Analyzer using Functional Programming Paradigms
Demonstrates stream operations, lambda expressions, and data aggregation
"""

import pandas as pd
from functools import reduce
from typing import Dict, List, Tuple, Any
import operator
from sales_reader import read_sales_data
from sales_model import SalesRecord


class SalesAnalyzer:
    """Functional programming approach to sales data analysis"""
    
    def __init__(self, csv_file: str):
        records = read_sales_data(csv_file)
        if records:
            data_dict = {
                'product_id': [r.product_id for r in records],
                'product_name': [r.product_name for r in records],
                'category': [r.category for r in records],
                'price': [r.price for r in records],
                'quantity': [r.quantity for r in records],
                'sales_date': [r.sales_date for r in records],
                'region': [r.region for r in records],
                'total_revenue': [r.total_value for r in records]
            }
            self.data = pd.DataFrame(data_dict)
            self.data['sales_date'] = pd.to_datetime(self.data['sales_date'])
        else:
            self.data = pd.DataFrame(columns=['product_id', 'product_name', 'category', 
                                            'price', 'quantity', 'sales_date', 'region', 
                                            'total_revenue'])
    
    def top_products_by_revenue(self, n: int = 5) -> List[Tuple[str, float]]:
        """Stream-based aggregation of top products by revenue"""
        if len(self.data) == 0:
            return []
        return (self.data.groupby('product_name')['total_revenue']
                .sum()
                .pipe(lambda x: x.sort_values(ascending=False))
                .head(n)
                .pipe(lambda x: list(zip(x.index, x.values))))
    
    def revenue_by_category(self) -> Dict[str, float]:
        """Functional aggregation using reduce and lambda"""
        if len(self.data) == 0:
            return {}
        category_revenues = self.data.groupby('category')['total_revenue'].sum()
        return dict(zip(category_revenues.index, category_revenues.values))
    
    def daily_sales_performance(self) -> List[Tuple[str, int, float]]:
        """Date-based performance analysis with functional operations"""
        if len(self.data) == 0:
            return []
        return (self.data.groupby(self.data['sales_date'].dt.date)
                .agg({'product_id': 'count', 'total_revenue': 'sum'})
                .pipe(lambda df: [(str(idx), row['product_id'], row['total_revenue']) 
                                for idx, row in df.iterrows()]))
    
    def regional_analysis(self) -> Dict[str, Dict[str, Any]]:
        """Nested functional operations for regional insights"""
        if len(self.data) == 0:
            return {}
        return (self.data.groupby('region')
                .apply(lambda group: {
                    'total_sales': group['total_revenue'].sum(),
                    'avg_order_value': group['total_revenue'].mean(),
                    'product_count': len(group),
                    'top_category': group.groupby('category')['total_revenue']
                                   .sum().idxmax()
                }, include_groups=False)
                .to_dict())
    
    def price_distribution_analysis(self) -> Dict[str, List[Tuple[str, int]]]:
        """Stream operations with custom lambda functions"""
        if len(self.data) == 0:
            return {'Budget': [], 'Mid-range': [], 'Premium': []}
        
        price_ranges = [
            ('Budget', lambda x: x < 100),
            ('Mid-range', lambda x: 100 <= x < 500),
            ('Premium', lambda x: x >= 500)
        ]
        
        return {
            range_name: list(
                self.data[self.data['price'].apply(condition)]
                .groupby('category')
                .size()
                .pipe(lambda x: zip(x.index, x.values))
            )
            for range_name, condition in price_ranges
        }
    
    def monthly_trend_analysis(self) -> List[Tuple[str, float, int]]:
        """Time-based aggregation using functional approach"""
        if len(self.data) == 0:
            return []
        return (self.data.groupby(self.data['sales_date'].dt.strftime('%Y-%m'))
                .agg({'total_revenue': 'sum', 'quantity': 'sum'})
                .pipe(lambda df: [(idx, row['total_revenue'], row['quantity']) 
                                for idx, row in df.iterrows()]))
    
    def weekly_sales_pattern(self) -> Dict[str, float]:
        """Weekly pattern analysis using lambda expressions"""
        if len(self.data) == 0:
            return {}
        return (self.data.groupby(self.data['sales_date'].dt.day_name())['total_revenue']
                .sum()
                .pipe(lambda x: dict(zip(x.index, x.values))))
    
    def date_range_analysis(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Complex date filtering with lambda expressions"""
        if len(self.data) == 0:
            return {'filtered_sales': 0, 'avg_daily_revenue': 0.0, 'peak_day': None}
        
        filtered_data = self.data
        if start_date:
            filtered_data = filtered_data[filtered_data['sales_date'] >= start_date]
        if end_date:
            filtered_data = filtered_data[filtered_data['sales_date'] <= end_date]
        
        if len(filtered_data) == 0:
            return {'filtered_sales': 0, 'avg_daily_revenue': 0.0, 'peak_day': None}
        
        daily_revenue = filtered_data.groupby(filtered_data['sales_date'].dt.date)['total_revenue'].sum()
        
        return {
            'filtered_sales': len(filtered_data),
            'avg_daily_revenue': daily_revenue.mean(),
            'peak_day': str(daily_revenue.idxmax()),
            'peak_revenue': daily_revenue.max()
        }
    
    def cross_category_insights(self) -> List[Tuple[str, str, float]]:
        """Multi-dimensional analysis using functional programming"""
        if len(self.data) == 0:
            return []
        return (self.data.groupby(['category', 'region'])['total_revenue']
                .sum()
                .reset_index()
                .pipe(lambda df: [(row['category'], row['region'], row['total_revenue']) 
                                for _, row in df.iterrows()]))


def main():
    """Execute comprehensive sales analysis"""
    analyzer = SalesAnalyzer('sales_data.csv')
    
    print("=== ADVANCED SALES DATA ANALYSIS ===\n")
    
    # Analysis 1: Top Products by Revenue
    print("1. TOP 5 PRODUCTS BY REVENUE:")
    top_products = analyzer.top_products_by_revenue()
    for product, revenue in top_products:
        print(f"   {product}: ${revenue:,.2f}")
    
    # Analysis 2: Revenue by Category
    print("\n2. REVENUE BY CATEGORY:")
    category_revenue = analyzer.revenue_by_category()
    for category, revenue in sorted(category_revenue.items(), key=lambda x: x[1], reverse=True):
        print(f"   {category}: ${revenue:,.2f}")
    
    # Analysis 3: Daily Sales Performance
    print("\n3. DAILY SALES PERFORMANCE:")
    daily_performance = analyzer.daily_sales_performance()
    for date, sales_count, revenue in sorted(daily_performance, key=lambda x: x[2], reverse=True)[:10]:
        print(f"   {date}: {sales_count} sales, ${revenue:,.2f} revenue")
    
    # Analysis 4: Regional Analysis
    print("\n4. REGIONAL ANALYSIS:")
    regional_data = analyzer.regional_analysis()
    for region, metrics in regional_data.items():
        print(f"   {region}:")
        print(f"     Total Sales: ${metrics['total_sales']:,.2f}")
        print(f"     Avg Order Value: ${metrics['avg_order_value']:.2f}")
        print(f"     Top Category: {metrics['top_category']}")
    
    # Analysis 5: Price Distribution
    print("\n5. PRICE DISTRIBUTION BY CATEGORY:")
    price_dist = analyzer.price_distribution_analysis()
    for price_range, categories in price_dist.items():
        print(f"   {price_range}:")
        for category, count in categories:
            print(f"     {category}: {count} products")
    
    # Analysis 6: Monthly Trends
    print("\n6. MONTHLY SALES TRENDS:")
    trends = analyzer.monthly_trend_analysis()
    for month, revenue, quantity in trends:
        print(f"   {month}: ${revenue:,.2f} revenue, {quantity} units sold")
    
    # Analysis 7: Weekly Sales Pattern
    print("\n7. WEEKLY SALES PATTERN:")
    weekly_pattern = analyzer.weekly_sales_pattern()
    for day, revenue in sorted(weekly_pattern.items(), key=lambda x: x[1], reverse=True):
        print(f"   {day}: ${revenue:,.2f}")
    
    # Analysis 8: Date Range Analysis
    print("\n8. JANUARY 2024 ANALYSIS:")
    jan_analysis = analyzer.date_range_analysis('2024-01-01', '2024-01-31')
    print(f"   Sales in period: {jan_analysis['filtered_sales']}")
    print(f"   Avg daily revenue: ${jan_analysis['avg_daily_revenue']:.2f}")
    print(f"   Peak day: {jan_analysis['peak_day']} (${jan_analysis['peak_revenue']:.2f})")


if __name__ == "__main__":
    main()