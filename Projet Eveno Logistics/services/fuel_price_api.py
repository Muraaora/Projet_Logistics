# services/fuel_price_api.py

from urllib.request import urlopen
import json
from typing import Dict

# Lien donné par le prof (station de référence à Juvisy-sur-Orge)
DEFAULT_API_URL = (
    "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "prix-des-carburants-en-france-flux-instantane-v2/records"
    "?where=id%3A%2291170007%22&limit=1"
)


def fetch_raw_fuel_json(api_url: str = DEFAULT_API_URL) -> dict:
    """
    Appelle l'API gouvernementale et renvoie le JSON brut sous forme de dict.
    """
    with urlopen(api_url) as f:
        data = f.read()
    return json.loads(data)


def parse_fuel_prices_from_json(json_obj: dict) -> Dict[str, float]:
    """
    Extrait les prix des carburants principaux à partir du JSON.

    Mapping normalisé projet :
        DIESEL   <=> gazole_prix
        GASOLINE <=> sp98_prix ou sp95_prix
        LPG      <=> gplc_prix

    Retourne un dict :
        {
            "Diesel":   prix_en_euro_par_L,
            "Gasoline": prix_en_euro_par_L,
            "LPG":      prix_en_euro_par_kg
        }
    """
    results = json_obj.get("results", [])
    if not results:
        raise ValueError("Réponse API vide : aucun résultat 'results'")

    station = results[0]

    prices: Dict[str, float] = {}

    # --- DIESEL ---
    diesel_price = station.get("gazole_prix")
    if diesel_price is not None:
        prices["Diesel"] = float(diesel_price)

    # --- GASOLINE ---
    # On privilégie SP98, sinon SP95
    sp98 = station.get("sp98_prix")
    sp95 = station.get("sp95_prix")

    gasoline_price = None
    if sp98 is not None:
        gasoline_price = float(sp98)
    elif sp95 is not None:
        gasoline_price = float(sp95)

    if gasoline_price is not None:
        prices["Gasoline"] = gasoline_price

    # --- LPG ---
    lpg_price = station.get("gplc_prix")
    if lpg_price is not None:
        prices["LPG"] = float(lpg_price)

    return prices


def get_realtime_energy_prices() -> Dict[str, float]:
    """
    Fonction principale à utiliser dans le projet.
    Elle renvoie un dict prêt à être fusionné avec ENERGY_PRICES :
        {"Diesel": ..., "Gasoline": ..., "LPG": ...}
    """
    raw_json = fetch_raw_fuel_json()
    return parse_fuel_prices_from_json(raw_json)


if __name__ == "__main__":
    # Petit test manuel si tu lances ce fichier directement
    data = fetch_raw_fuel_json()
    prices = parse_fuel_prices_from_json(data)
    print("Prix carburants (API) :", prices)
