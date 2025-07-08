# AI-Sentinel

Solution de détection d'anomalies réseau basée sur l'IA, à partir de logs Wireshark/Zeek, avec visualisation Grafana.

## Structure du projet
- `src/` : Scripts Python (prétraitement, IA, export)
- `data/raw/` : Logs bruts (Wireshark)
- `data/processed/` : Données prétraitées et résultats
- `notebooks/` : Exploration et tests
- `grafana/` : Dashboard Grafana

## Étapes principales
1. Capture et export des logs réseau (Wireshark)
2. Prétraitement et nettoyage des données
3. Détection d'anomalies (IA)
4. Export des résultats
5. Visualisation Grafana

## Utilisation du pipeline IA-Sentinel

1. Placez votre fichier de logs réseau (ex: log_test.csv) dans `data/raw/`.
2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```
3. Exécutez le script principal :
   ```bash
   python src/main.py
   ```
4. Les résultats sont générés dans `data/processed/` :
   - `preprocessed.csv` : données nettoyées et normalisées
   - `anomalies.csv` : données annotées (normal/anomalie)
   - `final_results.csv` : fichier final pour Grafana

## Visualisation avec Grafana

- Configurez une source de données CSV (ou utilisez un plugin CSV) dans Grafana.
- Importez le fichier `final_results.csv` depuis `data/processed/`.
- Créez des panels pour :
  - Nombre d’anomalies détectées
  - IP source/destination suspectes
  - Protocole le plus touché
  - Évolution temporelle des anomalies

## Exemple de panels Grafana

1. **Nombre d’anomalies détectées**
   - Type : Stat ou Bar Chart
   - Requête : `SELECT COUNT(*) FROM final_results WHERE anomalie=1`
2. **IP source/destination suspectes**
   - Type : Table
   - Requête : `SELECT ip_src, ip_dst FROM final_results WHERE anomalie=1`
3. **Protocole le plus touché**
   - Type : Pie Chart ou Bar Chart
   - Requête : `SELECT proto, COUNT(*) FROM final_results WHERE anomalie=1 GROUP BY proto`
4. **Évolution temporelle des anomalies**
   - Type : Time Series
   - Requête : `SELECT ts, COUNT(*) FROM final_results WHERE anomalie=1 GROUP BY ts`

## Procédure pour Grafana

1. Installer le plugin CSV (ex : marcusolsson-csv-datasource) via le marketplace Grafana.
2. Ajouter une nouvelle source de données CSV et pointer vers `data/processed/final_results.csv`.
3. Créer un nouveau dashboard et ajouter les panels ci-dessus.
4. Exporter la configuration du dashboard (menu "Partager" > "Exporter") et sauvegarder le fichier dans `grafana/dashboard.json`.

## Plan pour le support de présentation

1. **Introduction**
   - Objectif du projet AI-Sentinel
2. **Pipeline technique**
   - Prétraitement des logs (nettoyage, normalisation)
   - Détection d’anomalies (Isolation Forest)
   - Export des résultats
3. **Visualisation Grafana**
   - Présentation des panels
   - Démonstration live ou captures d’écran
4. **Conclusion**
   - Bilan, limites, perspectives

---

Le projet est prêt à être utilisé et présenté !

Pour toute question, consultez les scripts dans `src/` ou le notebook d’exploration.
