import os
import random
import pandas as pd
import requests

from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client


load_dotenv()
random.seed()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL ou SUPABASE_KEY manquante dans le fichier .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_CONTACTS = "contacts"
TABLE_SINISTRES = "sinistres"
TABLE_CLIENTS = "clients"


def charger_sinistres_min():
    response = (
        supabase.table(TABLE_SINISTRES)
        .select("sinistre_id, client_id, date_ouverture")
        .execute()
    )

    df_sinistres = pd.DataFrame(response.data)

    if df_sinistres.empty:
        raise ValueError("La table sinistres est vide.")

    return df_sinistres


def recuperer_prochain_contact_id():
    response = (
        supabase.table(TABLE_CONTACTS)
        .select("contact_id")
        .order("contact_id", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return 1

    return int(response.data[0]["contact_id"]) + 1


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
        "incomprehension_garantie",
    ]
    poids_motifs = [18, 20, 24, 8, 14, 6, 6, 4]

    for _ in range(n_contacts):
        sinistre = df_sinistres.sample(1).iloc[0]

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

        contacts_data.append({
            "contact_id": prochain_contact_id,
            "sinistre_id": int(sinistre["sinistre_id"]),
            "client_id": int(sinistre["client_id"]),
            "date_contact": datetime.today().replace(microsecond=0).isoformat(),
            "canal": canal,
            "motif_contact": motif,
            "temps_attente_sec": temps_attente_sec,
            "nb_transferts": nb_transferts,
            "duree_traitement_min": duree_traitement_min,
            "resolution_premier_contact": resolution_premier_contact,
            "escalade": escalade,
            "satisfaction_score": None,
            "nb_contacts_precedents": random.randint(0, 5),
        })
        prochain_contact_id += 1

    return pd.DataFrame(contacts_data)


def inserer_contacts(df_contacts):
    if df_contacts.empty:
        print("Aucun contact à insérer.")
        return

    payload = df_contacts.to_dict(orient="records")
    supabase.table(TABLE_CONTACTS).insert(payload).execute()
    print(f"{len(df_contacts)} contacts ajoutés dans '{TABLE_CONTACTS}'.")


def charger_sinistres_pour_contacts(df_contacts):
    sinistre_ids = df_contacts["sinistre_id"].dropna().astype(int).unique().tolist()

    response = (
        supabase.table(TABLE_SINISTRES)
        .select(
            "sinistre_id, client_id, date_ouverture, type_sinistre, "
            "statut_dossier, montant_estime, date_derniere_action"
        )
        .in_("sinistre_id", sinistre_ids)
        .execute()
    )

    return pd.DataFrame(response.data)


def charger_clients_pour_contacts(df_contacts):
    client_ids = df_contacts["client_id"].dropna().astype(int).unique().tolist()

    response = (
        supabase.table(TABLE_CLIENTS)
        .select(
            "client_id, date_naissance, date_inscription, "
            "segment_client, region, departement"
        )
        .in_("client_id", client_ids)
        .execute()
    )

    return pd.DataFrame(response.data)



def construire_dataframe_enrichi(df_contacts, df_sinistres, df_clients):
    return (
        df_contacts
        .merge(df_sinistres, on=["sinistre_id", "client_id"], how="left")
        .merge(df_clients, on="client_id", how="left")
    )

API_URL = "http://127.0.0.1:8000/predict/batch"


def envoyer_a_api(df_enrichi):
    payload = {
        "contacts": df_enrichi.to_dict(orient="records")
    }

    response = requests.post(API_URL, json=payload, timeout=30)
    response.raise_for_status()

    return response.json()


def main():
    df_sinistres_min = charger_sinistres_min()
    df_nouveaux_contacts = generer_contacts_clients(df_sinistres_min, n_contacts=5)

    inserer_contacts(df_nouveaux_contacts)

    df_sinistres_filtre = charger_sinistres_pour_contacts(df_nouveaux_contacts)
    df_clients_filtre = charger_clients_pour_contacts(df_nouveaux_contacts)

    df_enrichi = construire_dataframe_enrichi(
        df_nouveaux_contacts,
        df_sinistres_filtre,
        df_clients_filtre,
    )


    resultat_api = envoyer_a_api(df_enrichi)
    print("\nRéponse API :")
    print(resultat_api)


if __name__ == "__main__":
    main()


