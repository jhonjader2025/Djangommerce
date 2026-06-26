from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE: Agregar 'include'

urlpatterns = [
    path('', include('website.urls')), # Rutas funcionales de la app principal
    path('admin/', admin.site.urls),
]