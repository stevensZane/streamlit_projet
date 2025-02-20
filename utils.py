from bs4 import BeautifulSoup as bs
import pandas as pd
from requests import get
import warnings

# fonction pour scrapper les terrains
def scrap_coinafrique_villas(nombre_pages):
    data = {
        "type annonce": [],
        "nombre pieces": [],
        "prix": [],
        "adresse": [],
        "image lien": []
    }

    for i in range(nombre_pages):
        url = f'https://sn.coinafrique.com/categorie/villas?page={nombre_pages}'
        
        try:
            res = get(url)
            soup = bs(res.text, 'html.parser')
            containers = soup.find_all('div', class_ = "col s6 m4 l3")
        except Exception as e:
            print(f"Pas de containers trouvés sur la page {i}: {e}")
            continue
        
        for container in containers:
            img_link = container.find('img', class_ = "ad__card-img")['src']
            
            # on prend le lien de chaque container pour recuprer les informations
            # après on préfixe le lien de chaque container 'https://sn.coinafrique.com' pour iterer selon les pages
            try:
                inner_link = container.find('a', class_ = "card-image ad__card-image waves-block waves-light")["href"]
                if inner_link:
                    url_enfant = 'https://sn.coinafrique.com' + inner_link
                    
            except Exception as e:
                continue
            
            # on rentre dans url_enfant, pour extraire les donnees (s'il y'en a)
            if url_enfant:
                try:
                    res1 = get(url_enfant)
                    soup1 = bs(res1.text, 'html.parser')
                    container_1 = soup1.find('div', class_ = "card round slide proffer z-depth-0 remove-background-white")
                    
                    if container_1:
                        # Recuperation des informations
                        type_annonce = container_1.find('h1', class_ = 'title title-ad hide-on-large-and-down').text.split()[0]
                        nombre_pieces = int(container_1.find('span', class_ = 'qt').text)
                        prix = int(container_1.find('p', class_ = 'ad__card-price').text.replace('CFA', '').replace(' ', '').strip())
                        
                        adresse = container_1.find_all('span', class_ = 'valign-wrapper')[1].text
                    
                except Exception as e:
                    continue
                
                
                # on met tous les infos dans un dictionnaire
                data["type annonce"].append(type_annonce)
                data["nombre pieces"].append(nombre_pieces)
                data["prix"].append(prix)
                data["adresse"].append(adresse)
                data["image lien"].append(img_link)

    df = pd.DataFrame(data)
    
    return df

# fonction pour scrapper les villas
def scrap_coinafrique_terrains(nombre_pages):
    data1 = {
        "superficie": [],
        "prix": [],
        "adresse": [],
        "image lien": []
    }

    for j in range(nombre_pages):
        url2 = f'https://sn.coinafrique.com/categorie/terrains?page={nombre_pages}'
        
        try:
            res2 = get(url2)
            soup2 = bs(res2.text, 'html.parser')
            containers_ = soup2.find_all('div', class_ = "col s6 m4 l3")
        except Exception as e:
            print(f"Pas de containers trouvés sur la page: {e}")
            continue
        
        for container in containers_:
            img_link_ = container.find('img', class_ = "ad__card-img")['src']
            
            # on prend le lien de chaque container pour recuprer les informations
            # après on préfixe le lien de chaque container 'https://sn.coinafrique.com' pour iterer selon les pages
            try:
                inner_link_= container.find('a', class_ = "card-image ad__card-image waves-block waves-light")["href"]
                if inner_link_:
                    url_enfant_ = 'https://sn.coinafrique.com' + inner_link_
                    
            except Exception as e:
                continue
            
            # on rentre dans url_enfant, pour extraire les donnees (s'il y'en a)
            if url_enfant_:
                try:
                    res3 = get(url_enfant_)
                    soup3 = bs(res3.text, 'html.parser')
                    container_2 = soup3.find('div', class_ = "card round slide proffer z-depth-0 remove-background-white")
                    
                    if container_2:
                        superficie = int(container_2.find('span', class_ = 'qt').text.strip().replace("m2", ""))
                        prix = int(container_2.find('p', class_ = 'ad__card-price').text.replace('CFA', ' ').replace(' ', '').strip().strip())
                        adresse = container_2.find_all('span', class_ = 'valign-wrapper')[1].text

                    
                except Exception as e:
                    continue
                
                
                # on met tous les infos dans un dictionnaire
                data1["superficie"].append(superficie)
                data1["prix"].append(prix)
                data1["adresse"].append(adresse)
                data1["image lien"].append(img_link_)

    df1 = pd.DataFrame(data1)
    
    return df1

# variable pour les formulaires
google_forms = '<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScIINigJlApa3cAGiSv4cmZMRUvjxyms6HmKoIdOQcrEeuSvA/viewform?embedded=true" width="700" height="650" frameborder="0" marginheight="0" marginwidth="0">Chargement…</iframe>'
kobo_forms = '<iframe src=https://ee.kobotoolbox.org/i/j9qkSiwi width="700" height="600"></iframe>'

# autres variables
mot_inspirant = """Explorez, collectez, analysez.
Le web à portée de main, vos données en action.
Scraping, visualisation, décision – en un clic !"""

streamdata_logo = "./images/StreamData-logo.webp"