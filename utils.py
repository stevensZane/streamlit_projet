from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np 
from requests import get

# fonction pour scraper les villas
def scrap_villas(n):
    data = {
        "type annonce": [],
        "nombre pieces": [],
        "prix": [],
        "adresse": [],
        "image lien": []
    }
    
    for i in range(n):
    
        url = 'https://sn.coinafrique.com/categorie/villas?page={n}'
        
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_ = "col s6 m4 l3")
        
        for container in containers:
            img_link = container.find('img', class_ = "ad__card-img")['src']
            inner_link = container.find('a', class_ = "card-image ad__card-image waves-block waves-light")["href"]
            url_enfant = 'https://sn.coinafrique.com' + inner_link
            
            res1 = get(url_enfant)
            soup1 = bs(res1.text, 'html.parser')
            container_1 = soup1.find('div', class_ = "card round slide proffer z-depth-0 remove-background-white")
            try:
                type_annonce = container_1.find('h1', class_ = 'title title-ad hide-on-large-and-down').text.split()[0].capitalize()
                nombre_pieces = int(container_1.find('span', class_ = 'qt').text)
                prix = int(container_1.find('p', class_ = 'price').text.replace('CFA', '').replace(' ', '').strip())
                adresse = container_1.find_all('span', class_ = 'valign-wrapper')[1].text
            except Exception as e:
                continue
            
            
            dico = {
                "type annonce": type_annonce,
                "nombre pieces": nombre_pieces,
                "prix": prix,
                "adresse": adresse,
                "image lien": img_link
            }
            
            for key, value in dico.items():
                data[key].append(value)
        
    df = pd.DataFrame(data)
    return df

# fonction pour scraper les terrains
def scrap_terrains(nbre_page):
    gdf = pd.DataFrame()
    for i in range(nbre_page):
        url = 'https://sn.coinafrique.com/categorie/terrains?page={i}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all("div",class_ = "col s6 m4 l3")
        pdf = []
        for container in containers:
            try:
                img_link = container.find("img", class_="ad__card-img")["src"]
                prix = int(container.find("p", class_="ad__card-price").text.replace(" ", "").replace("CFA", ""))
                adresse = container.find("p", class_="ad__card-location").text.replace("location_on","")
                href = container.find("a", class_="card-image ad__card-image waves-block waves-light")["href"]
                urll = 'https://sn.coinafrique.com' + str(href)
                resa = get(urll)
                soup = bs(resa.text, 'html.parser')
                containerr = soup.find("div", class_="ad__info")
                superficie = int(containerr.find("span", class_="qt").text.replace(" ", "").replace("m2", ""))
                dict_terrain_infos = {
                    "superficie": superficie,
                    "prix": prix,
                    "adresse": adresse,
                    "img_link": img_link,
                }
                pdf.append(dict_terrain_infos)
            except:
                pass
        DF = pd.DataFrame(pdf)
        gdf = pd.concat([gdf,DF],axis=0).reset_index(drop = True)
    # Standardiser la colonne "prix" et remplacer "prixsurdemande" par NaN
    gdf["prix"] = gdf["prix"].replace("Prixsurdemande", np.nan).astype(float)
    # Remplacer les NaN par la moyenne des prix et convertir en int
    gdf.fillna({"prix": gdf["prix"].mean()}, inplace = True)
    return gdf

# variable pour les formulaires
google_forms = '<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScIINigJlApa3cAGiSv4cmZMRUvjxyms6HmKoIdOQcrEeuSvA/viewform?embedded=true" width="700" height="650" frameborder="0" marginheight="0" marginwidth="0">Chargement…</iframe>'
kobo_forms = '<iframe src=https://ee.kobotoolbox.org/i/j9qkSiwi width="700" height="600"></iframe>'

# autres variables
mot_inspirant = """Explorez, collectez, analysez.
Le web à portée de main, vos données en action.
Scraping, visualisation, décision – en un clic !"""

streamdata_logo = "./images/StreamData-logo.webp"



    
    
