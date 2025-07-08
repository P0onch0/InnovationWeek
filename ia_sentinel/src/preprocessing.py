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
    # On force le format pour éviter les erreurs et warnings
    # Exemple de format : "Jul  8, 2025 10:04:04.514970542 CEST"
    # On ignore le fuseau horaire et les microsecondes pour simplifier
    def parse_time(val):
        try:
            # Retire le fuseau horaire (dernier mot)
            val = " ".join(val.split(" ")[:-1])
            # Retire les microsecondes si présentes
            if "." in val:
                val = val.split(".")[0]
            # Format sans microsecondes : "Jul  8, 2025 10:04:04"
            return pd.to_datetime(val, format="%b %d, %Y %H:%M:%S", errors="coerce").timestamp()
        except Exception:
            return 0

    df['ts'] = df['ts'].astype(str).apply(parse_time)
    df['ts'] = pd.to_numeric(df['ts'], errors='coerce').fillna(0)

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