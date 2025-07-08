import os
import time
from preprocessing import preprocess_logs
from anomaly_detection import detect_anomalies
from export_results import export_final_results

RAW_DIR = os.path.join('data', 'raw')
PROCESSED_DIR = os.path.join('data', 'processed')
CHECK_INTERVAL = 5  # secondes

def get_processed_marker(filename):
    return os.path.join(PROCESSED_DIR, f"{filename}.done")

def process_log_file(filename):
    base = os.path.splitext(filename)[0]
    raw_log = os.path.join(RAW_DIR, filename)
    preprocessed = os.path.join(PROCESSED_DIR, f"preprocessed_{base}.csv")
    anomalies = os.path.join(PROCESSED_DIR, f"anomalies_{base}.csv")
    final = os.path.join(PROCESSED_DIR, 'final_results.csv')
    columns = ['ts', 'ip_src', 'ip_dst', 'proto', 'duration', 'orig_bytes', 'resp_bytes', 'anomalie']

    print(f"Traitement de {filename} ...")
    preprocess_logs(raw_log, preprocessed)
    detect_anomalies(preprocessed, anomalies, method='isolation_forest')
    export_final_results(anomalies, final, columns, log_name=base)
    # Marque le fichier comme traité
    with open(get_processed_marker(base), "w") as f:
        f.write("done")
    print(f"Fichiers générés et ajoutés à final_results.csv pour {filename}.")

def main():
    print("Surveillance du dossier data/raw/ ...")
    while True:
        for filename in os.listdir(RAW_DIR):
            if filename.endswith('.csv'):
                base = os.path.splitext(filename)[0]
                marker = get_processed_marker(base)
                if not os.path.exists(marker):
                    try:
                        process_log_file(filename)
                    except Exception as e:
                        print(f"Erreur lors du traitement de {filename} : {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()