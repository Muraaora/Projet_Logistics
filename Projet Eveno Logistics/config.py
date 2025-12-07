# config.py

from typing import Dict

# Config de connexion MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",        # à adapter
    "password": "",    # à adapter
    "database": "logistics",
}

# Valeurs par défaut (si l'API ne répond pas)
# Diesel / Gasoline -> €/L, LPG & Hydrogen -> €/kg, Electric -> €/kWh
DEFAULT_ENERGY_PRICES: Dict[str, float] = {
    "Diesel":   1.70,
    "Gasoline": 1.80,
    "LPG":      1.10,
    "Electric": 0.20,   # pas dans l'API
    "Hydrogen": 6.00,   # pas dans l'API
}

try:
    # Import tardif pour éviter les cycles d'import
    from services.fuel_price_api import get_realtime_energy_prices

    realtime_prices = get_realtime_energy_prices()
    ENERGY_PRICES = {**DEFAULT_ENERGY_PRICES, **realtime_prices}

    print("[INFO] Prix carburant mis à jour via API :", realtime_prices)

except Exception as e:
    # Si l'API plante, on garde les valeurs par défaut
    print("[WARN] Impossible de récupérer les prix carburant via l'API :", e)
    ENERGY_PRICES = DEFAULT_ENERGY_PRICES
