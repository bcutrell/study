from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Accounts:
    """Generated from collection: accounts"""
    id: Optional[str] = None
    cash: Optional[float] = None
    firm: Optional[str] = None


@dataclass
class Firms:
    """Generated from collection: firm"""
    id: Optional[str] = None
    name: Optional[str] = None


@dataclass
class FirmMetrics:
    """Generated from collection: firm_metrics"""
    id: Optional[str] = None
    metrics_csv: Optional[List] = None
    metrics_json: Optional[Dict] = None
    analysis_date: Optional[datetime] = None