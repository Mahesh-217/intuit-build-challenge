"""
Data model for the sales CSV dataset.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class SalesRecord:
    """In-memory representation of a single sales row."""

    product_id: int
    product_name: str
    category: str
    price: float
    quantity: int
    sales_date: str
    region: str

    @property
    def total_value(self) -> float:
        """Total sales value for this record."""
        return self.price * self.quantity

    @staticmethod
    def _to_int(value: Any, default: int = 0) -> int:
        """Safe int conversion with fallback."""
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _to_float(value: Any, default: float = 0.0) -> float:
        """Safe float conversion with fallback."""
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "SalesRecord":
        """Build a SalesRecord from a CSV DictReader row."""
        return cls(
            product_id=cls._to_int(row.get("product_id")),
            product_name=str(row.get("product_name", "")),
            category=str(row.get("category", "")),
            price=cls._to_float(row.get("price")),
            quantity=cls._to_int(row.get("quantity")),
            sales_date=str(row.get("sales_date", "")),
            region=str(row.get("region", "")),
        )