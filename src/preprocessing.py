# Prétraitement des données réseau
# Chargement, nettoyage, transformation, normalisation

import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def preprocess_logs(input_path, output_path):
    """
    Charge, nettoie, transforme et normalise les logs réseau.
    Args:
        input_path (str): Chemin du fichier log brut (CSV).
        output_path (str): Chemin du fichier prétraité (CSV).
    """
    df = pd.read_csv(input_path)
    # Sélection des colonnes adaptées au log_test.csv
    columns = ['ts', 'ip_src', 'ip_dst', 'proto', 'duration', 'orig_bytes', 'resp_bytes']
    df = df[columns]
    # Nettoyage : valeurs manquantes
    df = df.dropna()
    # Transformation : protocoles en valeurs numériques
    le = LabelEncoder()
    df['proto'] = le.fit_transform(df['proto'])
    # Normalisation des colonnes numériques
    scaler = MinMaxScaler()
    df[['duration', 'orig_bytes', 'resp_bytes']] = scaler.fit_transform(df[['duration', 'orig_bytes', 'resp_bytes']])
    df.to_csv(output_path, index=False)

