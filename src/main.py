# Script principal orchestrant le pipeline complet

def main():
    import os
    from preprocessing import preprocess_logs
    from anomaly_detection import detect_anomalies
    from export_results import export_final_results

    # Chemins relatifs depuis la racine du projet (corrigé)
    raw_log = os.path.join('data', 'raw', 'log_test.csv')
    preprocessed = os.path.join('data', 'processed', 'preprocessed.csv')
    anomalies = os.path.join('data', 'processed', 'anomalies.csv')
    final = os.path.join('data', 'processed', 'final_results.csv')

    # 1. Prétraitement
    preprocess_logs(raw_log, preprocessed)
    # 2. Détection d'anomalies
    detect_anomalies(preprocessed, anomalies, method='isolation_forest')
    # 3. Export final pour Grafana
    columns = ['ts', 'ip_src', 'ip_dst', 'proto', 'duration', 'orig_bytes', 'resp_bytes', 'anomalie']
    export_final_results(anomalies, final, columns)

if __name__ == '__main__':
    main()