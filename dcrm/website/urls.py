from django.urls import path
from . import views  # Importa el archivo views.py de la misma carpeta

urlpatterns = [  # type: ignore
    path("", views.home, name="home"),  # Aquí SÍ va el path # type: ignore
    path("login/", views.login_user, name="login"),  # type: ignore
    path("logout/", views.logout_user, name="logout"),  # type: ignore
    path("registrar/", views.register_user, name="register"),
    path("record/<str:pk>", views.customer_record, name="customer_record"),  # type: ignore
    path("delete-record/<str:pk>", views.delete_record, name="delete_record"),  # type: ignore
    path("update-record/<str:pk>", views.update_record, name="update_record"),  # type: ignore
    # Ruta para ver el listado general de pedidos (con paginación segura)
    path("pedidos/", views.list_orders, name="list_orders"),
    # Ruta para acceder al formulario y procesar la creación de un nuevo pedido
    path("crear-pedido/", views.create_order, name="create_order"),
    # Ruta para procesar y mostrar el formulario de creación de pedidos
    path("pedidos/crear/", views.create_order, name="create_order"),
    # Módulo tienda: catálogo y pedidos por usuario autenticado
    path("tienda/", views.store_home, name="store_home"),
    path("tienda/pedir/<int:product_id>/", views.create_store_order, name="create_store_order"),
]
