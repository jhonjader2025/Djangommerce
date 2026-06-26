from django.urls import path
from . import views  # Importa el archivo views.py de la misma carpeta

urlpatterns = [  # type: ignore
    path('', views.home, name='home'), # Aquí SÍ va el path # type: ignore
    path('login/', views.login_user, name='login'), # type: ignore
    path('logout/', views.logout_user, name='logout'), # type: ignore
    path('registrar/',views.register_user, name='register'),
    path('record/<str:pk>', views.customer_record, name='customer_record'), # type: ignore
    path('delete-record/<str:pk>', views.delete_record, name='delete_record'), # type: ignore
    path('update-record/<str:pk>', views.update_record, name='update_record'), # type: ignore

]