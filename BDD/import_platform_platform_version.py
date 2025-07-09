import mysql.connector
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()
# Récupération des informations de connexion à la base de données
db_password = os.getenv('BDD_PSWD')

# Connexion à ta base de données chez o2switch
conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3307,
    user='bawi2179_idumi',
    password=db_password,
    database='bawi2179_data_game',
    allow_local_infile=True
)

cursor = conn.cursor()

# Chemin vers ton fichier CSV local
csv_path = r"C:\Users\User\Documents\Data-Game\data-game\csv\platform_platform_version.csv"

query = f"""
LOAD DATA LOCAL INFILE '{csv_path.replace("\\", "/")}'
INTO TABLE platform_platform_version
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\\n'
IGNORE 1 LINES
(platform_id, version_id);
"""

try:
    cursor.execute(query)
    conn.commit()
    print(f"✅ Import terminé avec succès.")
except Exception as e:
    print("❌ Erreur lors de l'import :", e)

cursor.close()
conn.close()