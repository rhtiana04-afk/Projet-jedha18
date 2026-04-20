import os
import random
import string
import pandas as pd

from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine

fake = Faker("fr_FR")
random.seed()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

TABLE_CONTACTS = "contacts"
TABLE_SINISTRES = "sinistres"

required_vars = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_NAME": DB_NAME,
}

missing_vars = [key for key, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Variables manquantes : {', '.join(missing_vars)}")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def charger_sinistres():
    query = f"""
        SELECT sinistre_id, client_id, date_ouverture
        FROM {TABLE_SINISTRES}
    """
    df_sinistres = pd.read_sql(query, engine)

    if df_sinistres.empty:
        raise ValueError("La table sinistres est vide.")

    return df_sinistres


def recuperer_prochain_contact_id():
    query = f"SELECT MAX(contact_id) AS max_id FROM {TABLE_CONTACTS}"
    df_max = pd.read_sql(query, engine)

    max_id = df_max.loc[0, "max_id"]

    if pd.isna(max_id):
        return 1

    return int(max_id) + 1


def generer_contacts_clients(df_sinistres, n_contacts=5):
    contacts_data = []

    prochain_contact_id = recuperer_prochain_contact_id()

    canaux = ["telephone", "mail", "visite"]
    poids_canaux = [60, 30, 10]

    motifs = [
        "declaration_sinistre",
        "relance_dossier",
        "demande_avancement",
        "contestation_indemnisation",
        "piece_manquante",
        "expertise",
        "reclamation_delai",
        "incomprehension_garantie"
    ]
    poids_motifs = [18, 20, 24, 8, 14, 6, 6, 4]

    for _ in range(n_contacts):
        sinistre = df_sinistres.sample(1).iloc[0]

        sinistre_id = sinistre["sinistre_id"]
        client_id = sinistre["client_id"]
        date_ouverture = pd.to_datetime(sinistre["date_ouverture"])

        date_contact = min(
            date_ouverture + timedelta(days=random.randint(0, 360)),
            datetime.today()
        )

        canal = random.choices(canaux, weights=poids_canaux, k=1)[0]
        motif = random.choices(motifs, weights=poids_motifs, k=1)[0]

        temps_attente_sec = random.randint(0, 900)
        nb_transferts = random.randint(0, 3)
        duree_traitement_min = random.randint(1, 30)

        resolution_premier_contact = random.choices(
            ["oui", "non"],
            weights=[0.6, 0.4],
            k=1
        )[0]

        prob_escalade = 0.1
        if nb_transferts > 1:
            prob_escalade += 0.3
        if resolution_premier_contact == "non":
            prob_escalade += 0.4

        escalade = "oui" if random.random() < prob_escalade else "non"

        satisfaction = 5

        if temps_attente_sec > 600:
            satisfaction -= 2
        elif temps_attente_sec > 300:
            satisfaction -= 1

        if nb_transferts >= 2:
            satisfaction -= 1

        if resolution_premier_contact == "non":
            satisfaction -= 1

        if escalade == "oui":
            satisfaction -= 1

        if motif in [
            "reclamation_delai",
            "contestation_indemnisation",
            "incomprehension_garantie"
        ]:
            satisfaction -= 1

        satisfaction = max(1, min(5, satisfaction))

        contacts_data.append({
            "contact_id": prochain_contact_id,
            "sinistre_id": sinistre_id,
            "client_id": client_id,
            "date_contact": date_contact.strftime("%Y-%m-%d %H:%M:%S"),
            "canal": canal,
            "motif_contact": motif,
            "temps_attente_sec": temps_attente_sec,
            "nb_transferts": nb_transferts,
            "duree_traitement_min": duree_traitement_min,
            "resolution_premier_contact": resolution_premier_contact,
            "escalade": escalade,
            "satisfaction_score": satisfaction,
            "nb_contacts_precedents": random.randint(0, 5)
        })
        prochain_contact_id += 1
    return pd.DataFrame(contacts_data)


def inserer_contacts(df_contacts):
    if df_contacts.empty:
        print("Aucun contact à insérer.")
        return

    df_contacts.to_sql(TABLE_CONTACTS, engine, if_exists="append", index=False)
    print(f"{len(df_contacts)} contacts ajoutés dans '{TABLE_CONTACTS}'.")


def main():
    df_sinistres = charger_sinistres()
    df_contacts = generer_contacts_clients(df_sinistres, n_contacts=5)
    inserer_contacts(df_contacts)


if __name__ == "__main__":
    main()