import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import datetime

def preprocess_logs(input_path, output_path):
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

    # Conversion du timestamp en numérique (timestamp UNIX) et ajout d'une colonne date lisible
    def parse_time(val):
        try:
            # Retire le fuseau horaire (dernier mot)
            val_clean = " ".join(val.split(" ")[:-1])
            # Retire les microsecondes si présentes
            if "." in val_clean:
                val_clean = val_clean.split(".")[0]
            # Format sans microsecondes : "Jul  8, 2025 10:04:04"
            dt = pd.to_datetime(val_clean, format="%b %d, %Y %H:%M:%S", errors="coerce")
            return dt
        except Exception:
            return pd.NaT

    # Applique la conversion et crée deux colonnes : ts (timestamp numérique) et date_str (lisible)
    df['date_str'] = df['ts'].astype(str).apply(parse_time)
    df['ts'] = df['date_str'].apply(lambda x: x.timestamp() if pd.notnull(x) else 0)
    df['date_str'] = df['date_str'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Encodage du protocole si besoin
    if df['proto'].dtype == object:
        le = LabelEncoder()
        df['proto'] = le.fit_transform(df['proto'])

    # Sélection des colonnes utiles pour la suite du pipeline
    columns = ['ts', 'date_str', 'ip_src', 'ip_dst', 'proto', 'duration', 'orig_bytes', 'resp_bytes']
    df = df[columns]

    # Normalisation des colonnes numériques (hors IP et date_str)
    scaler = MinMaxScaler()
    df[['ts', 'duration', 'orig_bytes', 'resp_bytes']] = scaler.fit_transform(df[['ts', 'duration', 'orig_bytes', 'resp_bytes']])

    df.to_csv(output_path, index=False)