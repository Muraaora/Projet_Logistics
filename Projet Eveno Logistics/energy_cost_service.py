# services/energy_cost_service.py

from typing import Dict, Tuple, Optional
from models.energy import TruckEnergyProfile


class EnergyCostService:
    """
    Service qui encapsule la logique de coût d'énergie pour les camions.
    """
    def __init__(self, profiles: Dict[Tuple[str, str], TruckEnergyProfile]) -> None:
        # profiles[(ptac, energy_name)] -> TruckEnergyProfile
        self._profiles = profiles

    def get_profile(self, ptac: str, energy_name: str) -> Optional[TruckEnergyProfile]:
        """
        Retourne le profil énergétique pour un PTAC + énergie.
        """
        key = (ptac, energy_name)
        return self._profiles.get(key)

    def cost_for_trip(self, ptac: str, energy_name: str, distance_km: float) -> float:
        """
        Calcule le coût énergie pour un trajet donné pour un camion (PTAC + énergie).
        Lève une erreur si le profil n'existe pas.
        """
        profile = self.get_profile(ptac, energy_name)
        if profile is None:
            raise ValueError(
                f"Aucun profil énergétique trouvé pour PTAC={ptac}, énergie={energy_name}"
            )
        return profile.cost_for_distance(distance_km)

    def list_available_profiles(self):
        """
        Retourne une liste simple des profils disponibles (utile pour debug/affichage).
        """
        return [
            (ptac, energy, p.consumption_per_100km, p.energy_cost.unit)
            for (ptac, energy), p in self._profiles.items()
        ]
