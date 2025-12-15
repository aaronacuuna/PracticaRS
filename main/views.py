from django.shortcuts import render, redirect

import shelve


from models import Puntuacion, Pelicula
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendedItems
from main.forms import UsuarioBusquedaForm
from django.conf import settings 
from main.populateDB import populate_database


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
    
def index(request):
    return render(request, 'index.html')

def cargar_datos(request):
    mensaje = ""
    peli, gen, us, punt = populate_database()
    if (peli, gen, us, punt) is not None:
        mensaje = "Base de datos poblada correctamente."
    return render(request, 'cargar_datos.html', {'peliculas': peli, 'generos': gen, 'usuarios': us, 'puntuaciones': punt, 'mensaje': mensaje})
    
def recomendar_peliculas_usuario_RSitems(request):
    formulario = UsuarioBusquedaForm()
    items = None
    
    if request.method=='POST':
        formulario = UsuarioBusquedaForm(request.POST)
        
        if formulario.is_valid():
            idUsuario=formulario.cleaned_data['idUsuario']
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUsuario))
            recomendadas= rankings[:3]
            peliculas = []
            puntuaciones = []
            for re in recomendadas:
                peliculas.append(Pelicula.objects.get(pk=re[1]))
                puntuaciones.append(re[0])
            items= zip(peliculas,puntuaciones)
    
    return render(request, 'recomendar_peliculas_usuarios.html', {'formulario':formulario, 'items':items, 'STATIC_URL':settings.STATIC_URL})

