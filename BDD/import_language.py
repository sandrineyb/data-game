import mysql.connector

# Connexion à ta base de données chez o2switch
conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3307,
    user='bawi2179_idumi',
    password='zyLeM]F_lkz$',
    database='bawi2179_data_game',
    allow_local_infile=True
)

cursor = conn.cursor()

csv_path = r"C:\Users\User\Documents\Data-Game\data-game\csv\language.csv"

query = f"""
LOAD DATA LOCAL INFILE '{csv_path.replace("\\", "/")}'
INTO TABLE language
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\\n'
IGNORE 1 LINES
(id, name, native_name, locale);
"""

try:
    cursor.execute(query)
    conn.commit()
    print(f"✅ Import terminé avec succès.")
except Exception as e:
    print("❌ Erreur lors de l'import :", e)

cursor.close()
conn.close()