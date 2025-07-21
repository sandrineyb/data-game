import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors
import unicodedata
import re

# ======== Nettoyage de texte ========
def normalize_text(text):
    if not isinstance(text, str):
        return ''
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r"[’']", "", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

# ======== Chargement du dataset ========
# Remplace par le bon chemin vers ton CSV
game_all = pd.read_csv(r"./csv/game_all.csv")  # ou data/jeux.csv selon ton projet

# Nettoyage des colonnes multilabel si besoin
list_columns = ['genres', 'players_perspectives', 'release_period', 'type']
list_columns = [col for col in list_columns if col in game_all.columns]


for col in list_columns:
    # Remplace les NaN par des listes vides et convertit les chaînes en listes
    game_all[col] = game_all[col].apply(
        lambda x: x if isinstance(x, list)
        else [] if pd.isna(x)
        else [i.strip() for i in str(x).split(',')]
    )

# ======== Encodage des features ========
encoded_features = []
for col in list_columns:
    mlb = MultiLabelBinarizer()
    encoded = mlb.fit_transform(game_all[col])
    encoded_df = pd.DataFrame(encoded, columns=[f"{col}_{cls}" for cls in mlb.classes_])
    encoded_features.append(encoded_df)

# Fusion
features_matrix = pd.concat(encoded_features, axis=1)

# Index nettoyé
game_all['clean_name'] = game_all['game_name'].map(normalize_text)
features_matrix.index = game_all['clean_name']

# Dictionnaire clean → original
name_lookup = dict(zip(game_all['clean_name'], game_all['game_name']))

# ======== Modèle KNN ========
knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
knn_model.fit(features_matrix)

# ======== Fonction de recommandation ========
def recommend_games(game_name, n=5):
    clean = normalize_text(game_name)

    if clean not in features_matrix.index:
        return []

    game_vector = features_matrix.loc[clean].values.reshape(1, -1)
    distances, indices = knn_model.kneighbors(game_vector, n_neighbors=n+1)
    recommended_clean_names = features_matrix.index[indices.flatten()[1:]]
    recommended_original_names = [name_lookup[clean_name] for clean_name in recommended_clean_names]

    return recommended_original_names
