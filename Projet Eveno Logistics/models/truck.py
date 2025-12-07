# models/truck.py

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Truck:
    id: int                 # PK_TRUCK
    reference: int          # REFERENCE
    immat: str              # IMMAT
    date_mec: Optional[date]
    vin: Optional[str]
    power_ch: Optional[int]
    energy: Optional[str]
    ptac: Optional[str]
    refrigerated: bool
    color: Optional[str]
