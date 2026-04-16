# 🛡️ Projet final

Ce projet vise à simuler un environnement de service client pour une compagnie d'assurance, afin de permettre l'analyse de données et la prédiction de la satisfaction client via le Machine Learning.

## 🏗️ Structure du Projet
- `simulateur_final.py` : Le script principal qui génère les clients, les sinistres et les scores de satisfaction.
- `docker-compose.yml` : Configuration pour lancer la base de données PostgreSQL et l'interface Adminer.
- `requirements.txt` : Liste des bibliothèques Python nécessaires (Faker, Pandas, Psycopg2).

## 🚀 Installation et Lancement

### 1. Prérequis
Assurez-vous d'avoir Python 3 et Docker installés sur votre machine.

### 2. Lancer la base de données
Dans le terminal, à la racine du projet :
```bash
docker-compose up -d
