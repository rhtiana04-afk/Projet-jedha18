import pandas as pd
import numpy as np

df = pd.read_csv("insurance_dataset.csv")

print(f"Taille du fichier avant nettoyage : {df.shape}")

# Suppression Doublon et incohérence Gender
df = df.drop_duplicates(subset=['Customer_ID'], keep='last')
dictionnaire_genre = {'M': 'Male', 'm': 'Male', 'F': 'Female', 'f': 'Female'}
df['Gender'] = df['Gender'].replace(dictionnaire_genre)

# Missing value Gender
df['Gender'] = df['Gender'].fillna('Unknown')

# Missing value Premium
mediane_premium = df['Premium'].median()
df['Premium'] = df['Premium'].fillna(mediane_premium)

# Missing value Customer Satisfaction
mediane_satisfaction = df['Customer_Satisfaction'].median()
df['Customer_Satisfaction'] = df['Customer_Satisfaction'].fillna(mediane_satisfaction)

print(f"Taille du fichier après nettoyage : {df.shape}")

df.to_csv("insurance_dataset_clean.csv", index=False)