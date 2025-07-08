import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_password = os.getenv('BDD_PSWD')
engine = create_engine(
    f"mysql+mysqlconnector://bawi2179_idumi:{db_password}@127.0.0.1:3307/bawi2179_data_game"
)

df = pd.read_csv(r"C:\Users\User\Documents\Data-Game\data-game\csv\company_parent_modified.csv")
df = df.rename(columns={'status': 'status_id'})

from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text("DELETE FROM company"))

# 1. Insérer d'abord les lignes sans parent
df_no_parent = df[df['parent'].isnull()]
df_no_parent.to_sql('company', engine, if_exists='append', index=False)

# 2. Insérer les lignes avec parent dont le parent existe déjà dans la table
ids_in_db = set(df_no_parent['id'])
df_with_parent = df[df['parent'].notnull()]

# Boucle pour insérer par "vagues" les lignes dont le parent est déjà inséré
while not df_with_parent.empty:
    mask = df_with_parent['parent'].isin(ids_in_db)
    to_insert = df_with_parent[mask]
    if to_insert.empty:
        print("Certaines lignes ont un parent inexistant dans le CSV. Import arrêté.")
        break
    to_insert.to_sql('company', engine, if_exists='append', index=False)
    ids_in_db.update(to_insert['id'])
    df_with_parent = df_with_parent[~mask]

print("✅ Import terminé avec succès.")