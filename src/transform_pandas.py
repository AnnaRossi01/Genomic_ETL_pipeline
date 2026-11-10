import json 
import pandas as pd 

with open('data/raw/BRCA1_raw_data.json', 'r') as raw_dict: 
    data = json.load(raw_dict)

gene_id = data.get('id')
gene_symbol = data.get('display_name')

transcripts_list = data.get('Transcript', [])
df_transcripts = pd.DataFrame(transcripts_list)

df_transcripts['gene_id'] = gene_id
df_transcripts['gene_symbol'] = gene_symbol

# Calcola la lunghezza vettorialmente
df_transcripts['length'] = df_transcripts['end'] - df_transcripts['start']

# --- RECUPERO DATI STRUTTURALI (Esoni e Proteine) ---
# Conta quanti elementi ci sono nella lista 'Exon' di ogni trascritto
df_transcripts['exon_count'] = df_transcripts['Exon'].apply(lambda x: len(x) if isinstance(x, list) else 0)

# Verifica se esiste la colonna Translation e assegna 1 se è presente, 0 altrimenti
if 'Translation' in df_transcripts.columns:
    df_transcripts['is_protein_coding'] = df_transcripts['Translation'].notna().astype(int)
else:
    df_transcripts['is_protein_coding'] = 0

# Rinomina la colonna
df_transcripts = df_transcripts.rename(columns={'id': 'transcript_id'})

# Riga 23 CORRETTA: Aggiunte 'exon_count' e 'is_protein_coding'
df_filtered = df_transcripts[['transcript_id', 'gene_id', 'gene_symbol', 'start', 'end', 'biotype', 'source', 'length', 'exon_count', 'is_protein_coding']]

df_filtered.to_csv("data/processed/BRCA1_transcripts.csv", index=False)