# 🚀 Détection des contacts à risque d’insatisfaction 

## 🎯 Objectif

Dans un service client assurance, l’insatisfaction ne se manifeste pas toujours de manière explicite dès le départ. 
Elle peut aussi se construire progressivement, à travers des irritants tels que :

- des délais de traitement trop longs  
- des relances répétées  
- des transferts multiples  
- un manque de clarté dans le suivi  

👉 L’objectif de ce projet est de **détecter ces situations à risque le plus tôt possible**, afin de :
- prioriser les actions des équipes  
- améliorer l’expérience client  
- réduire les coûts opérationnels  

---

## ⚙️ Fonctionnement

Le projet repose sur un pipeline data complet :

Génération de contacts → Scoring ML → Stockage (Supabase) → Dashboard Power BI

### 🔹 Génération de données
- simulation de clients, sinistres et contacts  
- scénarios réalistes (attente, motifs, transferts…)  

### 🔹 Flux de contacts
- script `flux_contacts.py`  
- génération continue de nouveaux contacts  
- insertion dans Supabase  

### 🔹 Machine Learning
- modèle entraîné dans `machine_learning.ipynb`  
- prédiction d’un **score de satisfaction (1 à 5)**  
- pipeline complet (preprocessing + modèle)  

### 🔹 API (FastAPI)
- endpoint `/predict`  
- prédiction du score à partir des caractéristiques d’un contact  
- déployée via Docker sur Hugging Face  

### 🔹 Visualisation
- dashboard Power BI  
- page dédiée aux alertes  
- supervision des contacts à risque  


## 🛠️ Stack technique

- Python (Faker, Pandas, NumPy)
- Scikit-learn
- FastAPI
- Docker
- Supabase (PostgreSQL)
- Power BI

## Conclusion

Ce projet illustre comment l’exploitation des données permet d’anticiper les situations à risque et d’améliorer la gestion de la relation client.

## Auteurs 

Elizabeth POZOS
Hery RAKOTONDRATRIMO
Mirabelle DUPLEIX