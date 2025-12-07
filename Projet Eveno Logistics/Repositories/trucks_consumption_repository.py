import os
import sys
from typing import Dict, Tuple
from mysql.connector import MySQLConnection

CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from config import ENERGY_PRICES
from models.energy import EnergyCost, TruckEnergyProfile   # <-- models en minuscule
