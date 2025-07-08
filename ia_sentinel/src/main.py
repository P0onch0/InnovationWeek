import os
import sys
from preprocessing import preprocess_logs
from anomaly_detection import detect_anomalies
from export_results import export_final_results

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <nom_du_log.csv>")
        sys.exit(1)
    raw_log = sys.argv[1]
    preprocessed = os.path.join('data', 'processed', 'preprocessed.csv')
    anomalies = os.path.join('data', 'processed', 'anomalies.csv')
    final = os.path.join('data', 'processed', 'final_results.csv')

    preprocess_logs(raw_log, preprocessed)
    detect_anomalies(preprocessed, anomalies, method='isolation_forest')
    columns = ['ts', 'ip_src', 'ip_dst', 'proto', 'duration', 'orig_bytes', 'resp_bytes', 'anomalie']
    log_name = os.path.splitext(os.path.basename(raw_log))[0]
    export_final_results(anomalies, final, columns, log_name=log_name)

if __name__ == '__main__':
    main()