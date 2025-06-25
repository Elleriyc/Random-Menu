from fastapi import FastAPI
from src.scrap import plat, dessert,entree
import random

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe API! Use /plat or /dessert to get a random recipe."}

@app.get("/entree")
def liste_entree():

    return entree()

@app.get("/plat")
def liste_plat():

    return plat()

@app.get("/dessert")
def liste_dessert():

    return dessert()

@app.get("/menu")
def generate_menu():
    entree_choisie = random.choice(entree())
    plat_choisi = random.choice(plat())
    dessert_choisi = random.choice(dessert())
    if not entree_choisie or not plat_choisi or not dessert_choisi:
        return {"error": "Unable to generate a complete menu. Please try again later."}
    return {
        "entree": entree_choisie,
        "plat": plat_choisi,
        "dessert": dessert_choisi
        }
    