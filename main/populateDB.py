from main.models import Genero, Pelicula, Puntuacion

path = 'data'

def populate_database():
    genres = set()
    populate_genres(genres)
    raw_movies = []
    movies = populate_movies(raw_movies)

    users = []
    ratings = []
    populate_rating(users, movies, ratings)

    num_peliculas = Pelicula.objects.count()
    num_generos = Genero.objects.count()
    num_usuarios = Puntuacion.objects.values('idUsuario').distinct().count()
    num_puntuaciones = Puntuacion.objects.count()
    return (num_peliculas, num_generos, num_usuarios, num_puntuaciones)

def populate_genres(generos):
    Genero.objects.all().delete()

    lista=[]
    for genre in generos:
        lista.append(Genero(nombre=genre))
    Genero.objects.bulk_create(lista)

def populate_movies(movies):
    Pelicula.objects.all().delete()

    lista=[]
    for movie in movies:
        pelicula = Pelicula(
            idPelicula=movie['idPelicula'],
            titulo=movie['titulo'],
            director=movie['director'],
            imdb=movie['imdb']
        )
        pelicula.save()
        for genre_name in movie['generos']:
            genre = Genero.objects.get(nombre=genre_name)
            pelicula.generos.add(genre)
        lista.append(pelicula)
    Pelicula.objects.bulk_create(lista)
    return lista

def populate_rating(users, movies, ratings):
    Puntuacion.objects.all().delete()

    lista=[]
    for rating in ratings:
        puntuacion = Puntuacion(
            idUsuario=rating['idUsuario'],
            idPelicula=movies[rating['movie_index']],
            puntuacion=rating['puntuacion']
        )
        lista.append(puntuacion)
    Puntuacion.objects.bulk_create(lista)