# Import
from dotenv import load_dotenv
import os
import sys
import requests
from requests import post
import json
import time
import pandas as pd

# Chargements des des variables d'environnement
load_dotenv()

client_id_igdb = os.getenv("IGDB_ID_CLIENT")
client_secret_igdb = os.getenv("IGDB_SECRET_CLIENT")

# Vérification de la présence des variables d'environnement
if not client_id_igdb or not client_secret_igdb:
    print("Les variables d'environnement IGDB_ID_CLIENT et IGDB_SECRET_CLIENT ne sont pas définies.")
    raise SystemExit(1)


# Récupération du token d'accès pour IGDB
url = f"https://id.twitch.tv/oauth2/token?client_id={client_id_igdb}&client_secret={client_secret_igdb}&grant_type=client_credentials"

print(url)
response = requests.post(url)
if response.status_code == 200:
    response_json = response.json()
    if 'expires_in' in response_json == 0:
        print(f"Le token a expiré, il faut le renouveler")
    access_token = response_json['access_token']
    print(f"Access Token: {access_token}")
else:
    print("Error fetching data from the API")
    print("Status code:", response.status_code)
    
    
# Défninition du header pour les requêtes IGDB
headers = {
    'Client-ID': client_id_igdb,
    'Authorization': f'Bearer {access_token}',
}


# Récupération des game engines
def get_all_game_engines():
    """Récupération de tous les moteurs de jeu (game engines) depuis l'API IGDB.

    Returns:
        dataframe: DataFrame contenant les informations sur les moteurs de jeu.
    """
    all_game_engines = []
    offset = 0
    limit = 500  # Maximum limit for IGDB API

    while True:
        response = post('https://api.igdb.com/v4/game_engines', headers=headers, data=f'fields companies,description,logo,name,slug; limit {limit}; offset {offset};')
        
        if response.status_code == 200:
            response_json = response.json()
            if not response_json:  # If no more data, break the loop
                break
            all_game_engines.extend(response_json)
            offset += limit
        else:
            print("Error fetching data from the API")
            print("Status code:", response.status_code)
            break

    return pd.DataFrame(all_game_engines)


# Récupérations des platforms
def get_all_platforms():
    all_platforms = []
    offset = 0
    limit = 500  # Maximum limit for IGDB API
    
    while True:
        response = post('https://api.igdb.com/v4/platforms', headers=headers, data=f'fields *; exclude websites,checksum,created_at,updated_at,url;limit {limit}; offset {offset};')
        
        if response.status_code == 200:
            response_json = response.json()
            if not response_json:
                break
            all_platforms.extend(response_json)
            offset += limit
        else:
            print("Error fetching data from the API")
            print("Status code:", response.status_code)
            break
    return pd.DataFrame(all_platforms)


# Fonction pour récupérer toutes les player perspectives
def get_all_player_perspectives():
    """
    Récupère toutes les perspectives de joueur depuis l'API IGDB avec pagination.
    
    Returns:
        pd.DataFrame: DataFrame contenant toutes les perspectives de joueur.
    """
    all_player_perspectives = []
    offset = 0
    limit = 500  # Maximum limit for IGDB API

    while True:
        response = post('https://api.igdb.com/v4/player_perspectives', headers=headers, data=f'fields *; exclude created_at,checksum,updated_at,url; limit {limit}; offset {offset};')
        
        if response.status_code == 200:
            response_json = response.json()
            if not response_json:  # If no more data, break the loop
                break
            all_player_perspectives.extend(response_json)
            offset += limit
        else:
            print("Error fetching data from the API")
            print("Status code:", response.status_code)
            break

    return pd.DataFrame(all_player_perspectives)