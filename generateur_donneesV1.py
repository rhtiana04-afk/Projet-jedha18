import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("fr_FR")
np.random.seed(42)

# 1. CONFIGURATION GÉNÉRALE
n_clients = 5000
departments = {
    "Île-de-France": ["75", "77", "78", "91", "92", "93", "94", "95"],
    "Auvergne-Rhône-Alpes": ["01", "03", "07", "15", "26", "38", "42", "43", "63", "69", "73", "74"],
    "Provence-Alpes-Côte d'Azur": ["04", "05", "06", "13", "83", "84"],
    "Occitanie": ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"],
    "Hauts-de-France": ["02", "59", "60", "62", "80"],
    "Nouvelle-Aquitaine": ["16", "17", "19", "23", "24", "33", "40", "47", "64", "79", "86", "87"],
    "Grand Est": ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"],
    "Bretagne": ["22", "29", "35", "56"],
    "Pays de la Loire": ["44", "49", "53", "72", "85"],
    "Normandie": ["14", "27", "50", "61", "76"],
    "Bourgogne-Franche-Comté": ["21", "25", "39", "58", "70", "71", "89", "90"],
    "Centre-Val de Loire": ["18", "28", "36", "37", "41", "45"],
    "Corse": ["2A", "2B"]
}

region_probs = {
    "Île-de-France": 0.1884,
    "Auvergne-Rhône-Alpes": 0.1240,
    "Provence-Alpes-Côte d'Azur": 0.0789,
    "Occitanie": 0.0926,
    "Hauts-de-France": 0.0906,
    "Nouvelle-Aquitaine": 0.0930,
    "Grand Est": 0.0841,
    "Bretagne": 0.0521,
    "Pays de la Loire": 0.0591,
    "Normandie": 0.0506,
    "Bourgogne-Franche-Comté": 0.0424,
    "Centre-Val de Loire": 0.0391,
    "Corse": 0.0051
}

department_probs = {
    "Île-de-France": {
        "75": 0.176, "77": 0.115, "78": 0.122, "91": 0.108,
        "92": 0.135, "93": 0.136, "94": 0.115, "95": 0.093
    },
    "Auvergne-Rhône-Alpes": {
        "01": 0.083, "03": 0.041, "07": 0.041, "15": 0.018,
        "26": 0.067, "38": 0.157, "42": 0.094, "43": 0.028,
        "63": 0.082, "69": 0.232, "73": 0.053, "74": 0.104
    },
    "Provence-Alpes-Côte d'Azur": {
        "04": 0.026, "05": 0.022, "06": 0.228,
        "13": 0.418, "83": 0.225, "84": 0.081
    },
    "Occitanie": {
        "09": 0.025, "11": 0.064, "12": 0.050, "30": 0.103,
        "31": 0.271, "32": 0.032, "34": 0.192, "46": 0.030,
        "48": 0.013, "65": 0.040, "66": 0.086, "81": 0.067, "82": 0.027
    },
    "Hauts-de-France": {
        "02": 0.094, "59": 0.436, "60": 0.124, "62": 0.286, "80": 0.060
    },
    "Nouvelle-Aquitaine": {
        "16": 0.053, "17": 0.097, "19": 0.038, "23": 0.018,
        "24": 0.063, "33": 0.273, "40": 0.063, "47": 0.049,
        "64": 0.104, "79": 0.057, "86": 0.070, "87": 0.115
    },
    "Grand Est": {
        "08": 0.051, "10": 0.055, "51": 0.102, "52": 0.030,
        "54": 0.130, "55": 0.031, "57": 0.193, "67": 0.205,
        "68": 0.146, "88": 0.057
    },
    "Bretagne": {
        "22": 0.183, "29": 0.271, "35": 0.320, "56": 0.226
    },
    "Pays de la Loire": {
        "44": 0.371, "49": 0.210, "53": 0.078, "72": 0.167, "85": 0.174
    },
    "Normandie": {
        "14": 0.214, "27": 0.190, "50": 0.152, "61": 0.082, "76": 0.362
    },
    "Bourgogne-Franche-Comté": {
        "21": 0.191, "25": 0.194, "39": 0.093, "58": 0.074,
        "70": 0.084, "71": 0.197, "89": 0.122, "90": 0.045
    },
    "Centre-Val de Loire": {
        "18": 0.123, "28": 0.172, "36": 0.088,
        "37": 0.236, "41": 0.131, "45": 0.250
    },
    "Corse": {
        "2A": 0.49, "2B": 0.51
    }
}

regions = list(departments.keys())

# 2. GÉNÉRATION DES CLIENTS
clients_data = []
for i in range(1, n_clients + 1):
    region = np.random.choice(
        list(region_probs.keys()),
        p=list(region_probs.values())
    )
    dept = np.random.choice(
        list(department_probs[region].keys()),
        p=list(department_probs[region].values())
    )
    
    # Date naissance (18-80 ans)
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=80)
    # Inscription (Après ses 18 ans et avant aujourd'hui)
    signup_date = fake.date_between(start_date=birthdate + timedelta(days=18*365), end_date='today')

    clients_data.append({
        "client_id": i,
        "date_naissance": birthdate.strftime("%Y-%m-%d"),
        "date_inscription": signup_date.strftime("%Y-%m-%d"),
        "segment_client": np.random.choice(["Premium", "Pro", "Standard"], p=[0.2, 0.35, 0.45]),
        "region": region,
        "departement": dept
    })

clients_df = pd.DataFrame(clients_data)

# 3. GÉNÉRATION DES SINISTRES (Cohérence Totale)
def generer_sinistres(df_clients, n_sinistres=2000):
    sinistres_data = []
    today = datetime.today()

    for i in range(1, n_sinistres + 1):
        client = df_clients.sample(1).iloc[0]
        c_id = client['client_id']
        c_inscription = datetime.strptime(client['date_inscription'], "%Y-%m-%d")

        date_ouvert = fake.date_between(start_date=c_inscription, end_date='today')
        date_action = fake.date_between(start_date=date_ouvert, end_date='today')
        year = date_ouvert.year
        sinistre_id = int(f"{year}{str(i).zfill(5)}")

        # Ancienneté des dossiers
        today = datetime.today().date()
        anciennete = (today - date_ouvert).days

        if anciennete > 360:
            statut = "clos"
        else:
            statut = random.choice(["ouvert", "en cours"])

        sinistres_data.append({
            "sinistre_id": sinistre_id,
            "client_id": c_id,
            "date_ouverture": date_ouvert.strftime("%Y-%m-%d"),
            "type_sinistre": random.choice(["auto", "habitation"]),
            "statut_dossier": statut,
            "montant_estime": round(random.uniform(100.0, 15000.0), 2),
            "date_derniere_action": date_action.strftime("%Y-%m-%d")
        })

    return pd.DataFrame(sinistres_data)

sinistres_df = generer_sinistres(clients_df)

# 4. GÉNÉRATION DES CONTACTS CLIENTS (FACT TABLE)

def generer_contacts_clients(df_sinistres, n_contacts=10000):
    contacts_data = []

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
    
    for i in range(1, n_contacts + 1):
        sinistre = df_sinistres.sample(1).iloc[0]

        sinistre_id = sinistre["sinistre_id"]
        client_id = sinistre["client_id"]
        date_ouverture = datetime.strptime(sinistre["date_ouverture"], "%Y-%m-%d")

        jours_apres_ouverture = random.randint(0, 730)
        date_contact = date_ouverture + timedelta(days=jours_apres_ouverture)
        
        # tirage pondéré
        canal = random.choices(canaux, weights=poids_canaux, k=1)[0]
        motif = random.choices(motifs, weights=poids_motifs, k=1)[0]

        temps_attente_sec = random.randint(0, 900)
        nb_transferts = random.randint(0, 3)
        duree_traitement_min = random.randint(1, 30)
        
        resolution_premier_contact = random.choices(["oui", "non"], weights=[0.6, 0.4])[0]
        
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
        
        if motif in ["reclamation_delai", "contestation_indemnisation", "incomprehension_garantie"]:
            satisfaction -= 1
        
        satisfaction = max(1, min(5, satisfaction))

        contacts_data.append({
            "contact_id": i,
            "sinistre_id": sinistre_id,
            "client_id": client_id,
            "date_contact": date_contact.strftime("%Y-%m-%d"),
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

    return pd.DataFrame(contacts_data)

contacts_df = generer_contacts_clients(sinistres_df)

print("Exportation des données en cours...")
clients_df.to_csv("clients.csv", index=False)
sinistres_df.to_csv("sinistres.csv", index=False)
contacts_df.to_csv("contacts.csv", index=False)

print("✅ Fichiers CSV générés avec succès ! Vous pouvez commencer l'EDA et le Machine Learning.")

print("✅ Fichiers CSV générés avec succès ! Vous pouvez commencer l'EDA et le Machine Learning.")

