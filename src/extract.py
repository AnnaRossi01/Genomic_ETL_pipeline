import requests
import json 
import sys
import pandas as pd 
import time 
import os 

# definition of the gene panel, server and headers 
oncology_panel = ['BRCA1', 'TP53', 'EGFR', 'PTEN']
server = "https://rest.ensembl.org"
headers = {"Accept": "application/json"}

all_transcripts_data = []

print(" --- 1: EXTRACT (using API REST) ---")

for gene in oncology_panel: 
    print(f"DOwnload data for {gene}")

    endpoint = f"/lookup/symbol/homo_sapiens/{gene}?expand=1"

    print(f"Esecuzione della GET request per {gene}...")
    response = requests.get(server + endpoint, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error for {gene} --> Code: {response.status_code}")
        cache_path = f'data/raw/{gene}_raw_data.json'
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as raw_file:
                data = json.load(raw_file)
            print(f"Using cached data for {gene}")
        else:
            continue

    transcripts = data.get('Transcript', [])
    for t in transcripts:
        exons = t.get('Exon', [])
        exon_count = len(exons)
        is_coding = 1 if t.get('Translation') else 0

        all_transcripts_data.append({
            "gene_id": data.get('id'),
            "gene_symbol": gene,
            "transcript_id": t.get('id'),
            "start": t.get('start'),
            "end": t.get('end'),
            "biotype": t.get('biotype'),
            "exon_count": exon_count,
            "is_protein_coding": is_coding
        })

    time.sleep(1)


print(" ---2:TRANSFORM ---")
df = pd.DataFrame(all_transcripts_data)

# Calcoliamo la lunghezza dei trascritti vettorialmente
df['length'] = df['end'] - df['start']

print(f"Pipeline completed. Processed {len(df)} transcripts of {df['gene_symbol'].nunique()} genes.")

# Mostriamo un'anteprima dei dati
print("\ndataset view:")
print(df[['gene_symbol', 'transcript_id', 'biotype', 'length']].head(10))

# Creiamo la cartella se non esiste e salviamo il file (Load temporaneo in CSV)
os.makedirs('data/processed', exist_ok=True)
df.to_csv('data/processed/oncology_panel_transcripts.csv', index=False)
print("\nData saved in: data/processed/oncology_panel_transcripts.csv")