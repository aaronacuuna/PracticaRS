from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Genero(models.Model):
    nombre = models.TextField(unique=True, verbose_name='Categoría')
    
    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    idPelicula = models.TextField(primary_key=True)
    titulo = models.TextField(verbose_name='Título')
    director = models.TextField(verbose_name='Director')
    imdb = models.IntegerField(verbose_name='URL en IMDB')
    generos = models.ManyToManyField(Genero, null=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ('titulo', )

class Puntuacion(models.Model):
    PUNTUACIONES = ((10, 'Muy mala'), (15, 'Mala'), (20, 'Regular'), (25, 'Buena'),
                    (30, 'Muy Buena'), (35, 'Excelente'), (40, 'Obra maestra'), (45, 'Clásico'),
                    (50, 'Perfecta'))
    idUsuario = models.TextField(verbose_name='ID Usuario')
    idPelicula = models.ForeignKey(Pelicula,on_delete=models.CASCADE)
    puntuacion = models.IntegerField(verbose_name='Puntuación', validators=[MinValueValidator(10), MaxValueValidator(50)], choices=PUNTUACIONES)
