# models/energy.py

from dataclasses import dataclass


@dataclass
class EnergyCost:
    """
    Coût unitaire d'une énergie donnée.
    """
    energy_name: str        # 'Diesel', 'Gasoline', 'LPG', 'Electric', 'Hydrogen'
    unit: str               # 'L', 'kg', 'kWh'
    price_per_unit: float   # €/L, €/kg, €/kWh


@dataclass
class TruckEnergyProfile:
    """
    Profil énergétique d'un camion (PTAC + type d'énergie).
    Les consommations sont exprimées sur 100 km.
    """
    ptac: str                      # ex: '12t', '19t', ...
    energy_name: str               # 'Diesel', ...
    consumption_per_100km: float   # L/100km, kg/100km, kWh/100km
    energy_cost: EnergyCost        # coût unitaire associé

    def cost_for_distance(self, distance_km: float) -> float:
        """
        Calcule le coût de l'énergie pour un trajet de 'distance_km' km.
        """
        quantity = self.consumption_per_100km * distance_km / 100.0
        return quantity * self.energy_cost.price_per_unit
