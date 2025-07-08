# Export des résultats annotés dans un fichier CSV
import pandas as pd
import os

def export_final_results(input_path, output_path, columns, log_name=None):
    df = pd.read_csv(input_path)
    if log_name:
        df['log_name'] = log_name
        columns = columns + ['log_name']
    # Ajout (append) si le fichier existe déjà, sinon création
    if os.path.exists(output_path):
        df.to_csv(output_path, mode='a', header=False, index=False, columns=columns)
    else:
        df.to_csv(output_path, mode='w', header=True, index=False, columns=columns)