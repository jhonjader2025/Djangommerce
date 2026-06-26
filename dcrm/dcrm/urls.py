from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE: Agregar 'include'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('website.urls')), # Rutas funcionales de la app principal
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)