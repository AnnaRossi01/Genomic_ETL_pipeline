import sqlite3
import pandas as pd

print("--- PHASE 3: LOAD (Relational Database Creation) ---")

# 1. Read the processed flat file (CSV)
csv_path = 'data/processed/oncology_panel_transcripts.csv'
df = pd.read_csv(csv_path)

# 2. DATA SPLITTING (Normalization): Separate data into two relational tables

# A. 'genes' table: Drop duplicates to ensure each gene appears only once
genes_df = df[['gene_id', 'gene_symbol']].drop_duplicates().copy()
genes_df['pathology_panel'] = 'Oncology' # Add context information

# B. 'transcripts' table: Keep 'gene_id' as the Foreign Key for table joins
transcripts_df = df[['transcript_id', 'gene_id', 'biotype', 'length', 'exon_count', 'is_protein_coding']].copy()

# 3. Connect to the SQLite database
db_path = 'data/processed/oncology_clinical.db'
conn = sqlite3.connect(db_path)
print(f"Successfully connected to database: {db_path}")

# 4. Write DataFrames to SQL tables
genes_df.to_sql('genes', conn, if_exists='replace', index=False)
transcripts_df.to_sql('transcripts', conn, if_exists='replace', index=False)

print("Tables 'genes' and 'transcripts' created and populated successfully.")

# 5. VERIFICATION: Test the relational structure using a SQL JOIN query
print("\n--- TEST QUERY: RELATIONAL JOIN ---")
query = """
    SELECT 
        g.gene_symbol, 
        g.pathology_panel,
        t.biotype, 
        COUNT(t.transcript_id) as total_transcripts,
        ROUND(AVG(t.length), 0) as avg_length,
        ROUND(AVG(t.exon_count), 1) as avg_exons
    FROM 
        genes g
    JOIN 
        transcripts t ON g.gene_id = t.gene_id
    GROUP BY 
        g.gene_symbol, t.biotype
    HAVING 
        total_transcripts > 5
    ORDER BY 
        g.gene_symbol, total_transcripts DESC;
        """

# Execute the query and load results into a DataFrame for display
result_df = pd.read_sql_query(query, conn)
print(result_df.to_string(index=False))

# 6. Best Practice: Always close the database connection
conn.close()
print("\nDatabase connection closed.")