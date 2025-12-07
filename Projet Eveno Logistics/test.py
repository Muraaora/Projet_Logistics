# test_trucks.py

from db import get_connection
from Repositories.trucks_repository import load_trucks


def main():
    conn = get_connection()
    trucks = load_trucks(conn)

    print(f"Nombre de camions dans la base : {len(trucks)}\n")

    for t in trucks[:10]:  # on affiche les 10 premiers
        print(
            f"ID={t.id} | REF={t.reference} | IMMAT={t.immat} | "
            f"PTAC={t.ptac} | ENERGIE={t.energy} | Frigo={t.refrigerated}"
        )

    conn.close()


if __name__ == "__main__":
    main()
