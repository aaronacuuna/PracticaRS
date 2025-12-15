from django.shortcuts import render

import shelve
from models import Puntuacion
from main.recommendations import  transformPrefs, calculateSimilarItems

# Create your views here.

# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. Tambien carga el diccionario inverso
# Serializa los resultados en dataRS.dat
def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.idUsuario.idUsuario)
        itemid = int(ra.idPelicula.idPelicula)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()