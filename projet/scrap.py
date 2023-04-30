import requests
from bs4 import BeautifulSoup
import random
import re

# A FAIRE DEMAIN : GENERER DANS UN FICHIER UNE ENTREE + PLAT + DESSERT APPELER MENU |
# SCRAPPER UNE DEUXIEME PAGE ET RANGER DANS L'ORDRE DES MEILLEURS NOTES 

def entree():
    url2 = "https://www.marmiton.org/recettes/index/categorie/entree/"
    r_entree = requests.get(url2)

    if r_entree.ok:
        soup_entree = BeautifulSoup(r_entree.text, "html.parser")
        all_entree = soup_entree.findAll("div",{"class": "recipe-card"})
    
    list_entree = []
    list_rate_entree = []
    list_opinion_entree = []

    for entree in all_entree:
        name_of_entree = entree.find("h4", {"class": "recipe-card__title"}).text.strip()
        rate_entree = entree.find("span", {"class": "recipe-card__rating__value"}).text.strip()
        opinion_entree = entree.find('span', class_='mrtn-font-discret', text=re.compile(r'sur \d+ avis'))
        if opinion_entree:
            num_reviews = int(opinion_entree.text.split()[1])
            print(" sur " + str(num_reviews) + " avis")
        else:
            print("Nombre d'avis non trouvé")
        # Pour n'afficher que les meilleurs recettes 
        # if float(rate_entree) > 4.7:
        #     list_entree.append(name_of_entree + " - Notes : " + rate_entree + " - sur " + str(num_reviews) + " avis")
        list_entree.append(name_of_entree + " - Notes : " + rate_entree + " - sur " + str(num_reviews) + " avis")
    random_entree = random.choice(list_entree)
    with open ("entree.txt", "w") as f:
        f.writelines("%s\n" % element for element in list_entree)
    return random_entree

entree()


def plat(): 
    url = 'https://www.marmiton.org/recettes/index/categorie/plat-principal/'
    r_plat = requests.get(url)
    if r_plat.ok:
        soup = BeautifulSoup(r_plat.text, "lxml")
        all_plat = soup.findAll("div",{"class": "recipe-card"})
    
    list_plat = []
    list_rate_plat = []
    
    for plat in all_plat:
        name_of_plat = plat.find("h4",{"class": "recipe-card__title"}).text.strip()
        rate_of_plat = plat.find("span", {"class": "recipe-card__rating__value"}).text.strip()
        opinion_plat = plat.find('span', class_='mrtn-font-discret', text=re.compile(r'sur \d+ avis'))
        if opinion_plat:
            num_reviews_plat = int(opinion_plat.text.split()[1])
            print(" sur " + str(num_reviews_plat) + " avis")
        else:
            print("Nombre d'avis non trouvé")
        list_plat.append(name_of_plat + " - Notes : " + rate_of_plat + " - sur " + str(num_reviews_plat) + " avis")
        # print(list_plat)
        # list_rate_plat.append(rate_of_plat)
    # for element in list_plat:
    #     print(element)
    random_plat = random.choice(list_plat)
    with open ("plat.txt", "w") as f:
        f.writelines("%s\n" % element for element in list_plat)
    return random_plat
  
    # print(name_of_recipe + " - Note : " + rate_of_plat)

plat()

def dessert(): 
    url3  = "https://www.marmiton.org/recettes/index/categorie/dessert/"
    r_dessert = requests.get(url3)

    if r_dessert.ok:
        soup_dessert = BeautifulSoup(r_dessert.text, "html.parser")
        all_dessert = soup_dessert.find_all("div",{"class": "recipe-card"})
    
    list_dessert = []
    list_rate_dessert = []

    for dessert in all_dessert:
        name_of_dessert = dessert.find("h4", {"class": "recipe-card__title"}).text.strip()
        rate_dessert = dessert.find("span", {"class": "recipe-card__rating__value"}).text.strip()
        opinion_dessert = dessert.find('span', class_='mrtn-font-discret', text=re.compile(r'sur \d+ avis'))
        if opinion_dessert:
            num_reviews_dessert = int(opinion_dessert.text.split()[1])
            print(" - sur " + str(num_reviews_dessert) + " avis")
        else:
            print("Nombre d'avis non trouvé")
        list_dessert.append(name_of_dessert + " - Notes : " + rate_dessert + " - sur " + str(num_reviews_dessert) + " avis")
        # print(list_dessert)    
        # print(name_of_dessert + "- Note : " + rate_dessert)
    # for element in list_dessert:
    #     print(element)
    random_dessert = random.choice(list_dessert)
    with open ("dessert.txt", "w") as f:
        f.writelines("%s\n" % element for element in list_dessert)
    return random_dessert

dessert()

def menu(): 
    entree()
    plat()
    dessert()
    with open("menu.txt","w") as f:
        f.writelines("%s" % entree() + "\n" + plat() + "\n" + dessert() + "\n") 

menu()




