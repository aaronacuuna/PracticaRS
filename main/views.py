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
    peliculas = generos = usuarios = puntuaciones = None

    if request.method == "POST":
        try:
            num_peliculas, num_generos, num_usuarios, num_puntuaciones = populate_database()
            mensaje = "Se han cargado los datos correctamente"
            peliculas = num_peliculas
            generos = num_generos
            usuarios = num_usuarios
            puntuaciones = num_puntuaciones
        except Exception as e:
            mensaje = "Error al poblar la base de datos: {}".format(e)

        return render(request, 'cargar_datos.html', {'mensaje': mensaje, 'peliculas': peliculas, 'generos': generos, 'usuarios': usuarios, 'puntuaciones': puntuaciones})

    return render(request, 'cargar_datos.html')

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


def mostrar_usuarios_mas_estrictos(request):
    # Construir diccionario de preferencias desde la BD
    Prefs = {}
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.idUsuario.idUsuario)
        itemid = int(ra.idPelicula.idPelicula)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating

    # Calcular media de cada usuario
    medias = []
    for user, items in Prefs.items():
        if len(items) == 0:
            continue
        avg = sum(items.values()) / len(items)
        medias.append((avg, user))

    # Orden ascendente por media y tomar los 3 más estrictos (peores medias)
    medias.sort()
    estrictos = medias[:3]

    # Para cada usuario estricto, obtener los 3 usuarios más parecidos (distancia euclídea)
    resultado = []
    for (avg, user) in estrictos:
        similares = topMatches(Prefs, user, n=3, similarity=sim_distance)
        # topMatches devuelve (sim, other_user); convertir a lista de tuplas (user, sim)
        similares_formateados = [(other, sim) for (sim, other) in similares]
        resultado.append({'usuario': user, 'media': avg, 'similares': similares_formateados})

    return render(request, 'usuarios_estrictos.html', {'resultado': resultado, 'STATIC_URL': settings.STATIC_URL})

