import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def preprocess_logs(input_path, output_path):
    """
    Charge, nettoie, transforme et normalise les logs réseau adaptés au format Wireshark.
    Args:
        input_path (str): Chemin du fichier log brut (CSV).
        output_path (str): Chemin du fichier prétraité (CSV).
    """
    df = pd.read_csv(input_path)

    # Renommage des colonnes pour correspondre au pipeline
    df = df.rename(columns={
        'frame.time': 'ts',
        'ip.src': 'ip_src',
        'ip.dst': 'ip_dst',
        'ip.proto': 'proto',
        'tcp.srcport': 'src_port',
        'tcp.dstport': 'dst_port'
    })

    # Création des colonnes manquantes avec des valeurs par défaut
    df['duration'] = 0
    df['orig_bytes'] = 0
    df['resp_bytes'] = 0

    # Conversion du timestamp en numérique (timestamp UNIX)
    # Si la colonne 'ts' est déjà au format numérique, cette étape est ignorée
    try:
        df['ts'] = pd.to_datetime(df['ts'], errors='coerce').astype('int64') // 10**9
    except Exception:
        pass

    # Encodage du protocole si besoin
    if df['proto'].dtype == object:
        le = LabelEncoder()
        df['proto'] = le.fit_transform(df['proto'])

    # Sélection des colonnes utiles pour la suite du pipeline
    columns = ['ts', 'ip_src', 'ip_dst', 'proto', 'duration', 'orig_bytes', 'resp_bytes']
    df = df[columns]

    # Normalisation des colonnes numériques (hors IP)
    scaler = MinMaxScaler()
    df[['ts', 'duration', 'orig_bytes', 'resp_bytes']] = scaler.fit_transform(df[['ts', 'duration', 'orig_bytes', 'resp_bytes']])

    df.to_csv(output_path, index=False)