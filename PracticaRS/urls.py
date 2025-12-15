"""
URL configuration for PracticaRS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import index, cargar_datos, loadRS, buscar_peliculas_por_genero, mostrar_usuarios_mas_estrictos, recomendar_peliculas_usuario_RSitems

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('cargar_datos/', cargar_datos),
    path('loadRS/', loadRS),
    path('buscar_peliculas_por_genero/', buscar_peliculas_por_genero),
    path('mostrar_usuarios_mas_estrictos/', mostrar_usuarios_mas_estrictos),
    path('recomendar_peliculas_usuario_RSitems/', recomendar_peliculas_usuario_RSitems),
]
