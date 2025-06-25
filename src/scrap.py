import requests
from bs4 import BeautifulSoup


class Plat:
    def __init__(self, titre, lien, note, avis):
        self.titre = titre
        self.lien = lien
        self.note = note
        self.avis = avis

    def init_plat(self):
        return f"{self.titre} - {self.note} - {self.avis}"

class Entree:
    def __init__(self, titre, lien, note, avis):
        self.titre = titre
        self.lien = lien
        self.note = note
        self.avis = avis

    def init_entree(self):
        return f"{self.titre} - {self.note} - {self.avis}"

class Dessert:
    def __init__(self, titre, lien, note, avis):
        self.titre = titre
        self.lien = lien
        self.note = note
        self.avis = avis

    def init_dessert(self):
        return f"{self.titre} - {self.note} - {self.avis}"
    

def entree():
    """Scrape entrees from Marmiton website."""
    entrees_list = []
    entrees_dict = {}
    
    url2 = "https://www.marmiton.org/recettes/index/categorie/entree/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response_entree = requests.get(url2, headers=headers)
    
    if response_entree.ok:
        soup_entree = BeautifulSoup(response_entree.text, "html.parser")
        recettes = soup_entree.find_all("div", class_="mrtn-card-vertical-detailed")
        
        for recette_entree in recettes:
            titre_tag = recette_entree.select_one(".mrtn-card__title a")
            titre = titre_tag.get_text(strip=True) if titre_tag else "Titre non trouvé"
            lien = titre_tag['href'] if titre_tag and 'href' in titre_tag.attrs else "Lien non trouvé"

            note_tag = recette_entree.select_one(".mrtn-home-rating__rating")
            note = note_tag.get_text(strip=True) if note_tag else "Note non trouvée"

            avis_tag = recette_entree.select_one(".mrtn-home-rating__nbreviews")
            avis = avis_tag.get_text(strip=True) if avis_tag else "Avis non trouvés"

            entrees_dict = Entree(titre=titre, 
                                  lien=lien, 
                                  note=note, 
                                  avis=avis
                                )
            entrees_list.append(entrees_dict)
    
    return entrees_list
# print(entree())

def plat(): 
    plats_dict = {}
    plats_list = []
    url = 'https://www.marmiton.org/recettes/index/categorie/plat-principal/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response_plat = requests.get(url, headers=headers)

    if response_plat.ok:
        soup = BeautifulSoup(response_plat.text, "html.parser")
        recettes = soup.find_all("div", class_="mrtn-card-vertical-detailed")
        print("Nombre de recettes trouvées :", len(recettes))

        for recette in recettes:
            # Titre
            titre_tag = recette.select_one(".mrtn-card__title a")
            titre = titre_tag.get_text(strip=True) if titre_tag else "Titre non trouvé"

            # Lien
            lien = titre_tag['href'] if titre_tag and 'href' in titre_tag.attrs else "Lien non trouvé"

            # Note
            note_tag = recette.select_one(".mrtn-home-rating__rating")
            note = note_tag.get_text(strip=True) if note_tag else "Note non trouvée"

            # Nombre d'avis
            avis_tag = recette.select_one(".mrtn-home-rating__nbreviews")
            avis = avis_tag.get_text(strip=True) if avis_tag else "Avis non trouvés"

            plats_dict = Plat(titre=titre, 
                              lien=lien, 
                              note=note, 
                              avis=avis)
            plats_list.append(plats_dict)

    return plats_list


def dessert() -> list:
    """Scrape desserts depuis Marmiton website.""" 
    desserts = []
    url3  = "https://www.marmiton.org/recettes/index/categorie/dessert/"
    response_dessert = requests.get(url3)

    if response_dessert.ok:
        soup_dessert = BeautifulSoup(response_dessert.text, "html.parser")
        recettes = soup_dessert.find_all("div", class_="mrtn-card-vertical-detailed")
        for recette in recettes:
            titre_tag = recette.select_one(".mrtn-card__title a")
            titre = titre_tag.get_text(strip=True) if titre_tag else "Titre non trouvé"
            lien = titre_tag['href'] if titre_tag and 'href' in titre_tag.attrs else "Lien non trouvé"

            note_tag = recette.select_one(".mrtn-home-rating__rating")
            note = note_tag.get_text(strip=True) if note_tag else "Note non trouvée"

            avis_tag = recette.select_one(".mrtn-home-rating__nbreviews")
            avis = avis_tag.get_text(strip=True) if avis_tag else "Avis non trouvés"

            dessert_dict = Dessert(
                titre=titre,
                lien=lien,
                note=note,
                avis=avis
            )
            desserts.append(dessert_dict)
    return desserts



    # with open("menu.txt","w") as f:
    #     f.writelines("%s" % entree() + "\n" + plat() + "\n" + dessert() + "\n") 
    # return "Menu généré avec succès ! Consultez le fichier menu.txt pour voir les recettes."





