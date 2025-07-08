# Détection d'anomalies avec IA (Isolation Forest, K-Means, etc.)
def detect_anomalies(input_path, output_path, method='isolation_forest'):
    """
    Applique un algorithme non supervisé pour détecter les anomalies.
    Args:
        input_path (str): Chemin du fichier CSV prétraité.
        output_path (str): Chemin du fichier CSV annoté.
        method (str): 'isolation_forest' ou 'kmeans'.
    """
    import pandas as pd
    from sklearn.ensemble import IsolationForest
    from sklearn.cluster import KMeans
    df = pd.read_csv(input_path)
    # Utiliser uniquement les colonnes numériques pertinentes
    features = df[['proto', 'duration', 'orig_bytes', 'resp_bytes']]
    if method == 'isolation_forest':
        model = IsolationForest(contamination=0.2, random_state=42)
        df['anomalie'] = model.fit_predict(features)
        df['anomalie'] = df['anomalie'].map({1: 0, -1: 1})
    elif method == 'kmeans':
        kmeans = KMeans(n_clusters=2, random_state=42)
        df['cluster'] = kmeans.fit_predict(features)
        counts = df['cluster'].value_counts()
        anomaly_label = counts.idxmin()
        df['anomalie'] = (df['cluster'] == anomaly_label).astype(int)
        df = df.drop(columns=['cluster'])
    else:
        raise ValueError('Méthode non supportée')
    df.to_csv(output_path, index=False)

