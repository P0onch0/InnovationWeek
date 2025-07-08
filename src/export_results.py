# Export des résultats annotés dans un fichier CSV

import pandas as pd

def export_final_results(input_path, output_path, columns):
    """
    Exporte les colonnes utiles pour Grafana dans un CSV final.
    Args:
        input_path (str): Chemin du fichier CSV annoté.
        output_path (str): Chemin du fichier CSV final.
        columns (list): Colonnes à conserver.
    """
    df = pd.read_csv(input_path)
    df_final = df[columns]
    df_final.to_csv(output_path, index=False)

