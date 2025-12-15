from main.models import Genero, Pelicula, Puntuacion

path = 'data'

def populate_database():
    genres = set()
    raw_movies = []
    with open(f'{path}/movies2.txt', 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            print(parts)
            movie_id = parts[0]
            title = parts[1]
            director = parts[2]
            imdb = int(parts[3])
            genre_list = []
            if len(parts) == 5:
                genre_list = parts[4].split(',')
            for genre in genre_list:
                genres.add(genre)
            raw_movies.append({
                'idPelicula': movie_id,
                'titulo': title,
                'director': director,
                'imdb': imdb,
                'generos': genre_list
            })
    
    populate_genres(genres)

    movies = populate_movies(raw_movies)

    users = set()
    ratings = []

    with open(f'{path}/ratings.txt', 'r') as f:
        for line in f:
            parts = line.strip().split()
            print(parts)
            user_id = int(parts[0])
            movie_index = parts[1]
            puntuacion = int(parts[2])
            users.add(user_id)
            ratings.append({
                'idUsuario': user_id,
                'movie_index': movie_index,
                'puntuacion': puntuacion
            })

    populate_rating(movies, ratings)

    num_peliculas = Pelicula.objects.count()
    num_generos = Genero.objects.count()
    num_usuarios = len(users)
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
    movies_dict = dict()
    categories_dict = dict()
    for movie in movies:
        pelicula = Pelicula(
            idPelicula=movie['idPelicula'],
            titulo=movie['titulo'],
            director=movie['director'],
            imdb=int(movie['imdb'])
        )
        lista.append(pelicula)

        lista_aux = []
        for genre in movie['generos']:
            lista_aux.append(Genero.objects.get(nombre=genre))
        categories_dict[movie['idPelicula']] = lista_aux
    Pelicula.objects.bulk_create(lista)

    for movie in Pelicula.objects.all():
        movie.generos.set(categories_dict[movie.idPelicula])
        movies_dict[movie.idPelicula] = movie
    return movies_dict

# def populate_movies(movies):
#     Pelicula.objects.all().delete()

#     lista = []
#     dict_generos = {}
    
#     all_genres = {g.nombre: g for g in Genero.objects.all()}
    
#     id_peliculas = set()
#     for movie in movies:
#         if movie['idPelicula'] in id_peliculas:
#             continue
#         id_peliculas.add(movie['idPelicula'])
        
#         pelicula = Pelicula(
#             idPelicula=movie['idPelicula'],
#             titulo=movie['titulo'],
#             director=movie['director'],
#             imdb=movie['imdb']
#         )
#         lista.append(pelicula)
#         dict_generos[movie['idPelicula']] = movie['generos']
        
#     Pelicula.objects.bulk_create(lista)
    
#     movies_dict = {}
#     for pelicula in Pelicula.objects.all():
#         movies_dict[pelicula.idPelicula] = pelicula
        
#         genre_names = dict_generos.get(pelicula.idPelicula, [])
#         genres_objs = [all_genres[name] for name in genre_names if name in all_genres]
#         pelicula.generos.set(genres_objs)
        
#     return movies_dict

def populate_rating(movies, ratings):
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