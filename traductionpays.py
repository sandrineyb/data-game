import pycountry

# Dictionnaire de traduction pour les pays courants
TRADUCTIONS_PAYS = {
    "United States": "États-Unis",
    "France": "France",
    "Germany": "Allemagne", 
    "Japan": "Japon",
    "United Kingdom": "Royaume-Uni",
    "Spain": "Espagne",
    "Italy": "Italie",
    "China": "Chine",
    "Russia": "Russie",
    "Canada": "Canada",
    "Brazil": "Brésil",
    "Australia": "Australie",
    "India": "Inde",
    "Mexico": "Mexique",
    "Netherlands": "Pays-Bas",
    "Switzerland": "Suisse",
    "Sweden": "Suède",
    "Norway": "Norvège",
    "Finland": "Finlande",
    "Denmark": "Danemark",
    "Poland": "Pologne",
    "Austria": "Autriche",
    "Belgium": "Belgique",
    "Portugal": "Portugal",
    "Greece": "Grèce",
    "Ireland": "Irlande",
    "South Korea": "Corée du Sud",
    "Turkey": "Turquie"
    # Ajoute d'autres pays au fur et à mesure selon tes besoins
}

def code_vers_nom_pays(code, langue='fr'):
    if not code:
        return "Non communiqué"
    
    try:
        # Conversion en int si c'est un float
        if isinstance(code, float):
            code = int(code)
        
        # Conversion en string avec padding à 3 chiffres
        code_str = str(code).zfill(3)
        
        # Recherche par code numérique
        try:
            pays = pycountry.countries.get(numeric=code_str)
            nom_en = pays.name
            
            # Retourner la traduction ou le nom anglais
            if langue == 'fr':
                return TRADUCTIONS_PAYS.get(nom_en, nom_en)
            else:
                return nom_en
                
        except (KeyError, AttributeError, LookupError):
            return f"Pays {code}"
            
    except Exception as e:
        print(f"Erreur: {e}")
        return "Code pays inconnu"

# Exemple d'utilisation
print(f"USA: {code_vers_nom_pays(840)}")
print(f"France: {code_vers_nom_pays(250)}")
print(f"Japon: {code_vers_nom_pays(392)}")
print(f"Allemagne: {code_vers_nom_pays(276)}")