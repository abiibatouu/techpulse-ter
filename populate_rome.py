import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(host=os.getenv('DB_HOST'), port=int(os.getenv('DB_PORT')), database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))
cur = conn.cursor()

print('=== 1. ALTER TABLE - ajouter colonnes ===')
cur.execute('ALTER TABLE offres ADD COLUMN IF NOT EXISTS code_rome VARCHAR(10), ADD COLUMN IF NOT EXISTS libelle_rome TEXT;')
conn.commit()
print('✓ Colonnes ajoutées')
print()

print('=== 2. UPDATE - remplir depuis raw_json ===')
cur.execute('UPDATE offres SET code_rome = raw_json->>\'romeCode\', libelle_rome = raw_json->>\'romeLibelle\' WHERE code_rome IS NULL;')
conn.commit()
rows_updated = cur.rowcount
print(f'✓ {rows_updated} offres mises à jour')
print()

print('=== 3. SELECT - vérifier distribution ===')
cur.execute('SELECT libelle_rome, COUNT(*) n FROM offres GROUP BY libelle_rome ORDER BY n DESC;')
rows = cur.fetchall()
for i, (libelle, count) in enumerate(rows, 1):
    libelle_str = libelle if libelle else "NULL"
    print(f'{i}. {libelle_str:50} ({count:4}x)')

cur.close()
conn.close()
