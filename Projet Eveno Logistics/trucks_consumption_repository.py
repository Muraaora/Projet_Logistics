# repositories/trucks_consumption_repository.py

from typing import Dict, Tuple
from mysql.connector import MySQLConnection

from config import ENERGY_PRICES
from models.energy import EnergyCost, TruckEnergyProfile


def _build_energy_cost_objects() -> Dict[str, EnergyCost]:
    """
    Construit les objets EnergyCost à partir des prix dans config.ENERGY_PRICES.
    """
    # unités imposées par la table trucks_consumption
    units = {
        "Diesel":   "L",
        "Gasoline": "L",
        "LPG":      "kg",
        "Electric": "kWh",
        "Hydrogen": "kg",
    }

    energy_costs: Dict[str, EnergyCost] = {}
    for energy_name, price in ENERGY_PRICES.items():
        unit = units.get(energy_name, "u")
        energy_costs[energy_name] = EnergyCost(
            energy_name=energy_name,
            unit=unit,
            price_per_unit=price,
        )
    return energy_costs


def load_truck_energy_profiles(
    conn: MySQLConnection,
) -> Dict[Tuple[str, str], TruckEnergyProfile]:
    """
    Lit la table trucks_consumption dans la base 'logistics' et retourne un dict :
        (ptac, energy_name) -> TruckEnergyProfile
    """
    energy_costs = _build_energy_cost_objects()

    query = """
        SELECT
            PTAC,
            `DIESEL (L)`,
            `GASOLINE (L)`,
            `LPG (kg)`,
            `ELECTRIC (kWh)`,
            `HYDROGEN (kg)`
        FROM trucks_consumption
    """

    cursor = conn.cursor()
    cursor.execute(query)

    profiles: Dict[Tuple[str, str], TruckEnergyProfile] = {}

    for row in cursor.fetchall():
        ptac = row[0]
        diesel, gasoline, lpg, electric, hydrogen = row[1:]

        if diesel is not None:
            profiles[(ptac, "Diesel")] = TruckEnergyProfile(
                ptac=ptac,
                energy_name="Diesel",
                consumption_per_100km=diesel,
                energy_cost=energy_costs["Diesel"],
            )

        if gasoline is not None:
            profiles[(ptac, "Gasoline")] = TruckEnergyProfile(
                ptac=ptac,
                energy_name="Gasoline",
                consumption_per_100km=gasoline,
                energy_cost=energy_costs["Gasoline"],
            )

        if lpg is not None:
            profiles[(ptac, "LPG")] = TruckEnergyProfile(
                ptac=ptac,
                energy_name="LPG",
                consumption_per_100km=lpg,
                energy_cost=energy_costs["LPG"],
            )

        if electric is not None:
            profiles[(ptac, "Electric")] = TruckEnergyProfile(
                ptac=ptac,
                energy_name="Electric",
                consumption_per_100km=electric,
                energy_cost=energy_costs["Electric"],
            )

        if hydrogen is not None:
            profiles[(ptac, "Hydrogen")] = TruckEnergyProfile(
                ptac=ptac,
                energy_name="Hydrogen",
                consumption_per_100km=hydrogen,
                energy_cost=energy_costs["Hydrogen"],
            )

    cursor.close()
    return profiles
