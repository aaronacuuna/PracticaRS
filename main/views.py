from django.shortcuts import render, redirect

import shelve


from main.models import Puntuacion, Pelicula, Genero
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendedItems
from main.forms import UsuarioBusquedaForm, GeneroBusquedaForm
from django.conf import settings 
from main.populateDB import populate_database
from django.http.response import HttpResponseRedirect


# Create your views here.

def loadDict():
    Prefs={}  
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

def loadRS(request):
    loadDict()
    return HttpResponseRedirect('/index.html')

def buscar_peliculas_por_genero(request):
    formulario = GeneroBusquedaForm()
    peliculas = None
    
    if request.method == 'POST':
        formulario = GeneroBusquedaForm(request.POST)
        if formulario.is_valid():
            genero = Genero.objects.get(id=formulario.cleaned_data['genero'].id)
            peliculas = genero.pelicula_set.all()
   
    return render(request, 'peliculasporgenero.html', {'peliculas': peliculas, 'formulario': formulario})
    
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

