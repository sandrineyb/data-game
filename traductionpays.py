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
    
    # Dictionnaire direct pour les codes les plus courants
    CODES_PAYS = {
        840: "États-Unis",
        250: "France",
        276: "Allemagne", 
        392: "Japon",
        826: "Royaume-Uni",
        724: "Espagne",
        380: "Italie",
        156: "Chine",
        643: "Russie",
        124: "Canada"
    }
    
    try:
        # Conversion en int si c'est un float
        code_num = int(float(code))
        
        # Vérifier dans notre dictionnaire direct d'abord
        if code_num in CODES_PAYS:
            return CODES_PAYS[code_num]
        
        # Essayer avec pycountry comme plan B
        code_str = str(code_num).zfill(3)
        try:
            pays = pycountry.countries.get(numeric=code_str)
            if pays:
                nom_en = pays.name
                return TRADUCTIONS_PAYS.get(nom_en, nom_en)
        except:
            pass
            
        # Si on arrive ici, essayer un lookup plus flexible
        try:
            pays = pycountry.countries.lookup(str(code_num))
            if pays:
                nom_en = pays.name
                return TRADUCTIONS_PAYS.get(nom_en, nom_en)
        except:
            return f"Pays {code_num}"
            
    except Exception as e:
        print(f"Erreur dans code_vers_nom_pays: {e}")
        return f"Code pays inconnu: {code}"

# Exemple d'utilisation
print(f"USA: {code_vers_nom_pays(840)}")
print(f"France: {code_vers_nom_pays(250)}")
print(f"Japon: {code_vers_nom_pays(392)}")
print(f"Allemagne: {code_vers_nom_pays(276)}")