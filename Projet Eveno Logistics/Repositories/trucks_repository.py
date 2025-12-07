# Repositories/trucks_repository.py

import os
import sys
from typing import List
from mysql.connector import MySQLConnection

# === pour que Python voie le dossier racine (et donc models/) ===
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)
# =================================================================

from models.truck import Truck   # <-- ici : models en minuscule


def load_trucks(conn: MySQLConnection) -> List[Truck]:
    """
    Récupère tous les camions depuis la table 'trucks'
    et les transforme en objets Truck.
    """
    query = """
        SELECT
            PK_TRUCK,
            REFERENCE,
            IMMAT,
            DATE_MEC,
            VIN,
            CH,
            ENERGIE,
            PTAC,
            REMORQUE_REFRIGEREE,
            COULEUR
        FROM trucks
    """

    cursor = conn.cursor()
    cursor.execute(query)

    trucks: List[Truck] = []

    for row in cursor.fetchall():
        (
            pk_truck,
            reference,
            immat,
            date_mec,
            vin,
            ch,
            energie,
            ptac,
            remorque_refrigeree,
            couleur,
        ) = row

        refrigerated = bool(remorque_refrigeree) if remorque_refrigeree is not None else False

        truck = Truck(
            id=pk_truck,
            reference=reference,
            immat=immat,
            date_mec=date_mec,
            vin=vin,
            power_ch=ch,
            energy=energie,
            ptac=ptac,
            refrigerated=refrigerated,
            color=couleur,
        )
        trucks.append(truck)

    cursor.close()
    return trucks
