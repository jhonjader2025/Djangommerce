from django.shortcuts import (
    redirect,
    render,
)  # permite cambiar la plantilla  html con datos  y devolver respuesta

# Esta es la función que se ejecuta cuando entras a la página
# login para incio de sesion  segun el rol
# logout para cerrar sesion
from django.contrib.auth import authenticate, login, logout  # type: ignore # Importamos las funciones de autenticación, inicio de sesión y cierre de sesión de Django.
from django.contrib import messages  # type: ignore #
from .forms import UserRegisterForm, RecordForm  # type: ignore # Importamos el formulario de registro de usuarios personalizado que hemos creado en forms.py.
from .models import Record
from django.core.paginator import Paginator  # type: ignore # Importamos la clase Paginator de Django para manejar la paginación de los registros en la vista home.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# SEGURIDAD: Importamos el decorador para obligar a que el usuario esté autenticado
from django.contrib.auth.decorators import login_required

# Importamos el paginador para manejar grandes volúmenes de pedidos de forma eficiente
from django.core.paginator import Paginator

# Importamos el modelo y el formulario que cree
from .models import Order
from .forms import OrderForm


def create_sample_records():
    if Record.objects.exists():
        return

    sample_records = [
        {
            "first_name": "Juan",
            "last_name": "Pérez",
            "email": "juan.perez@example.com",
            "phone_number": "+5491123456789",
            "address": "Av. Siempre Viva 123",
            "city": "Buenos Aires",
            "state": "Buenos Aires",
            "zip_code": "1000",
        },
        {
            "first_name": "María",
            "last_name": "García",
            "email": "maria.garcia@example.com",
            "phone_number": "+5491167890123",
            "address": "Calle Falsa 456",
            "city": "Córdoba",
            "state": "Córdoba",
            "zip_code": "5000",
        },
        {
            "first_name": "Carlos",
            "last_name": "Ramírez",
            "email": "carlos.ramirez@example.com",
            "phone_number": "+5491145678901",
            "address": "Av. del Libertador 789",
            "city": "Rosario",
            "state": "Santa Fe",
            "zip_code": "2000",
        },
        {
            "first_name": "Lucía",
            "last_name": "Fernández",
            "email": "lucia.fernandez@example.com",
            "phone_number": "+5491187654321",
            "address": "Calle Larga 101",
            "city": "Mendoza",
            "state": "Mendoza",
            "zip_code": "5500",
        },
        {
            "first_name": "Martín",
            "last_name": "Sánchez",
            "email": "martin.sanchez@example.com",
            "phone_number": "+5491178901234",
            "address": "Bulevar Central 202",
            "city": "Salta",
            "state": "Salta",
            "zip_code": "4400",
        },
        {
            "first_name": "Ana",
            "last_name": "López",
            "email": "ana.lopez@example.com",
            "phone_number": "+5491132109876",
            "address": "Pasaje Real 303",
            "city": "La Plata",
            "state": "Buenos Aires",
            "zip_code": "1900",
        },
        {
            "first_name": "Diego",
            "last_name": "Martínez",
            "email": "diego.martinez@example.com",
            "phone_number": "+5491120987654",
            "address": "Calle Nueva 404",
            "city": "Neuquén",
            "state": "Neuquén",
            "zip_code": "8300",
        },
        {
            "first_name": "Sofía",
            "last_name": "Torres",
            "email": "sofia.torres@example.com",
            "phone_number": "+5491165432109",
            "address": "Av. del Sol 505",
            "city": "Resistencia",
            "state": "Chaco",
            "zip_code": "3500",
        },
        {
            "first_name": "Andrés",
            "last_name": "Muñoz",
            "email": "andres.munoz@example.com",
            "phone_number": "+5491154321098",
            "address": "Calle Verde 606",
            "city": "San Juan",
            "state": "San Juan",
            "zip_code": "5400",
        },
        {
            "first_name": "Camila",
            "last_name": "Vega",
            "email": "camila.vega@example.com",
            "phone_number": "+5491198765432",
            "address": "Av. del Río 707",
            "city": "Salta",
            "state": "Salta",
            "zip_code": "4400",
        },
    ]

    for record_data in sample_records:
        Record.objects.create(**record_data)


def home(request):  # type: ignore
    # Control de login y listado de registros.
    # Nota: el login se procesa en la misma vista home y solo los usuarios autenticados ven los registros.
    if request.method == "POST":  # pyright: ignore[reportUnknownMemberType]
        username = request.POST.get("username", "")  # type: ignore
        password = request.POST.get("password", "")  # type: ignore
        user = authenticate(request, username=username, password=password)  # type: ignore
        if user is not None:  # valor o nulo
            login(request, user)  # pyright: ignore[reportUnknownArgumentType]
            messages.success(request, "Ingresado exitosamente")  # pyright: ignore[reportUnknownArgumentType]
            return redirect("home")
        else:
            messages.error(request, "Las credenciales son inválidas.")  # type: ignore
            return render(request, "home.html", {"records": None})  # type: ignore

    records = None
    if request.user.is_authenticated:  # pyright: ignore[reportUnknownMemberType]
        if not Record.objects.exists():
            create_sample_records()

        record_list = Record.objects.order_by("-created_at").all()  # type: ignore
        paginator = Paginator(record_list, 10)  # type: ignore
        page_number = request.GET.get("page")
        records = paginator.get_page(page_number)  # type: ignore

    return render(request, "home.html", {"records": records})  # type: ignore


# funcion para logiar
def login_user(request):  # type: ignore
    # Nota: esta vista no hace login directo porque home ya procesa el formulario de autenticación.
    return redirect("home")


# funcion para poder salir  cerrar sesion
def logout_user(request):  # type: ignore
    logout(request)  # cierre de la sesion del usuario
    # muestra un mensaje de exito al usuario
    messages.success(request, "cerraste la session correctamente")
    return redirect("home")  # direccionar al usuario a la pafina de inicio


# funcion para registrar un nuevo usuario
def register_user(request):  # type: ignore
    # si el metodo de la solicitud es POST, significa que se esta enviando el formulario de registro
    if request.method == "POST":  # pyright: ignore[reportUnknownMemberType]
        form = UserRegisterForm(request.POST)  # type: ignore
        if form.is_valid():  # type: ignore
            form.save()  # type: ignore
            username = form.cleaned_data["username"]  # type: ignore
            password = form.cleaned_data["password1"]  # type: ignore
            user = authenticate(request, username=username, password=password)  # type: ignore
            login(request, user)  # type: ignore
            messages.success(request, "registro exitoso")  # type: ignore
            return redirect(
                "home"
            )  # redirige al usuario a la página de inicio después de un registro exitoso
    else:
        form = UserRegisterForm()  # type: ignore
    return render(request, "register.html", {"form": form})  # type: ignore


# Funcion para mostrar el registro de un cliente especifico


def delete_record(request, pk):  # type: ignore
    if request.user.is_authenticated:  # pyright: ignore[reportUnknownMemberType]
        delete_it = Record.objects.get(id=pk)  # type: ignore # obtenemos el registro del cliente utilizando su clave primaria (pk)
        delete_it.delete()  # type: ignore# eliminamos el registro del cliente de la base de datos
        messages.success(request, "registro eliminado correctamente")  # type: ignore# mostramos un mensaje de éxito indicando que el registro fue eliminado correctamente
        return redirect(
            "home"
        )  # redirigimos al usuario a la página de inicio después de eliminar el registro
    else:
        messages.error(request, "debes iniciar sesion para eliminar el registro del cliente")  # type: ignore# si el usuario no está autenticado, mostramos un mensaje de error indicando que debe iniciar sesión para eliminar el registro del cliente
        return redirect(
            "home"
        )  # redirigimos al usuario a la página de inicio si no está autenticado


def update_record(request, pk):  # type: ignore
    if request.user.is_authenticated:  # pyright: ignore[reportUnknownMemberType]
        current_record = Record.objects.get(id=pk)  # type: ignore # obtenemos el registro del cliente utilizando su clave primaria (pk)
        form = RecordForm(request.POST or None, instance=current_record)  # type: ignore # creamos una instancia del formulario de registro de clientes, pasando los datos enviados en la solicitud POST (si los hay) y el registro actual como instancia para que el formulario sepa que estamos actualizando un registro existente
        if form.is_valid():  # type: ignore # verificamos si el formulario es válido, es decir, si los datos cumplen con las reglas de validación definidas en el formulario
            form.save()  # type: ignore # si el formulario es válido, guardamos los cambios en la base de datos, lo que actualizará el registro del cliente con los nuevos datos proporcionados en el formulario
            messages.success(request, "registro actualizado correctamente")  # type: ignore # mostramos un mensaje de éxito indicando que el registro fue actualizado correctamente
            return redirect(
                "home"
            )  # redirigimos al usuario a la página de inicio después de actualizar el registro
        return render(request, "update_record.html", {"form": form})  # type: ignore# si el formulario no es válido o si la solicitud no es POST, renderizamos la plantilla 'update_record.html' y pasamos el formulario como contexto para mostrarlo en la página
    else:
        messages.error(request, "debes iniciar sesion para actualizar el registro del cliente")  # type: ignore# si el usuario no está autenticado, mostramos un mensaje de error indicando que debe iniciar sesión para actualizar el registro del cliente
        return redirect(
            "home"
        )  # redirigimos al usuario a la página de inicio si no está autenticado


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record": customer_record})
    else:
        messages.error(request, "Debes iniciar sesión para ver el registro del cliente")
        return redirect("home")


# =====================================================================
# VISTA 1: LISTAR PEDIDOS (CON SEGURIDAD DE SESIÓN Y PAGINACIÓN)
# =====================================================================
@login_required(
    login_url="home"
)  # Si la sesión expira o no está logueado, redirige a la raíz (login)
def list_orders(request):
    """
    Vista protegida que recupera todos los pedidos registrados en MySQL
    y los muestra de forma paginada para optimizar el rendimiento del servidor.
    """
    # Recuperamos todos los pedidos de la base de datos, ordenados del más reciente al más antiguo
    orders_list = Order.objects.all().order_by("-created_at")

    # PAGINACIÓN: Mostramos 10 pedidos por página para no sobrecargar el navegador
    paginator = Paginator(orders_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Enviamos los datos protegidos al template
    return render(request, "orders.html", {"orders": page_obj})


# =====================================================================
# VISTA 2: CREAR PEDIDO (CON VALIDACIÓN CSRF Y BACKEND)
# =====================================================================
@login_required(login_url="home")
def create_order(request):
    """
    Vista protegida que procesa el formulario de creación de pedidos.
    Cuenta con validación segura de peticiones POST y manejo de mensajes del sistema.
    """
    if request.method == "POST":
        # Pasamos los datos del POST al formulario para su validación
        form = OrderForm(request.POST)

        # Validamos que los datos sean correctos y que pasen los filtros de seguridad (ej. monto > 0)
        if form.is_valid():
            form.save()  # Guarda de forma segura en MySQL
            messages.success(request, "¡Pedido registrado exitosamente en el sistema!")
            return redirect("list_orders")  # Redirige al listado general de pedidos
        else:
            # Si el formulario no es válido (ej. inyección de datos erróneos), avisa al usuario
            messages.error(
                request,
                "Hubo un error al registrar el pedido. Revisa los datos ingresados.",
            )
    else:
        # Si la petición es GET, simplemente mostramos el formulario vacío
        form = OrderForm()

    return render(request, "add_order.html", {"form": form})
