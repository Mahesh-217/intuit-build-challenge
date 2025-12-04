import csv
from pathlib import Path
from typing import List
from sales_model import SalesRecord


def read_sales_data(csv_path: str) -> List[SalesRecord]:
    """Read sales data from CSV file."""
    path = Path(csv_path)
    
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    records = []
    
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                record = SalesRecord.from_row(row)
                records.append(record)
            except (ValueError, KeyError):
                continue  # Skip malformed rows
    
    return records