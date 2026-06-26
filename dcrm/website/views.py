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
from decimal import Decimal
from django.db.models import Count, Sum

# SEGURIDAD: Importamos el decorador para obligar a que el usuario esté autenticado
from django.contrib.auth.decorators import login_required

# Importamos el paginador para manejar grandes volúmenes de pedidos de forma eficiente
from django.core.paginator import Paginator

# Importamos el modelo y el formulario que cree
from .models import Order, Product, ProductOrder
from .forms import OrderForm, OrderAdminForm


def get_user_role(user):
    """Devuelve el rol del usuario para la lógica de negocio del CRM."""
    if not getattr(user, "is_authenticated", False):
        return "usuario"

    profile = getattr(user, "profile", None)
    if profile is not None:
        role = getattr(profile, "role", None)
        if role:
            return role

    return "usuario"


def can_manage_records(role):
    """Define qué roles pueden crear o modificar registros de clientes y pedidos."""
    return role in {"admin", "vendedor"}


def is_admin(role):
    return role == "admin"


def create_sample_products():
    """Carga productos base (frutas) para la tienda si aún no existen."""
    if Product.objects.exists():
        return

    fruits = [
        {
            "name": "Manzana Roja",
            "description": "Fruta fresca por unidad",
            "price": Decimal("1.50"),
            "stock": 200,
        },
        {
            "name": "Banano",
            "description": "Banano maduro de alta calidad",
            "price": Decimal("0.80"),
            "stock": 250,
        },
        {
            "name": "Naranja",
            "description": "Naranja dulce para jugo",
            "price": Decimal("1.10"),
            "stock": 220,
        },
        {
            "name": "Fresa",
            "description": "Caja de fresas frescas",
            "price": Decimal("2.90"),
            "stock": 120,
        },
        {
            "name": "Piña",
            "description": "Piña tropical entera",
            "price": Decimal("3.20"),
            "stock": 80,
        },
    ]

    for product_data in fruits:
        Product.objects.create(**product_data)


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

    role = get_user_role(request.user)
    return render(request, "home.html", {"records": records, "user_role": role})  # type: ignore


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
        role = get_user_role(request.user)
        if not can_manage_records(role):
            messages.error(request, "No tienes permiso para eliminar registros.")
            return redirect("home")
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
        role = get_user_role(request.user)
        if not can_manage_records(role):
            messages.error(request, "No tienes permiso para actualizar registros.")
            return redirect("home")
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
        return render(
            request,
            "record.html",
            {"customer_record": customer_record, "user_role": get_user_role(request.user)},
        )
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
    return render(
        request,
        "orders.html",
        {"orders": page_obj, "user_role": get_user_role(request.user)},
    )


# =====================================================================
# VISTA 2: CREAR PEDIDO (CON VALIDACIÓN CSRF Y BACKEND)
# =====================================================================
@login_required(login_url="home")
def create_order(request):
    """
    Vista protegida que procesa el formulario de creación de pedidos.
    Cuenta con validación segura de peticiones POST y manejo de mensajes del sistema.
    """
    role = get_user_role(request.user)
    if not can_manage_records(role):
        messages.error(request, "Solo los administradores o vendedores pueden crear pedidos.")
        return redirect("list_orders")

    if request.method == "POST":
        # Pasamos los datos del POST al formulario para su validación
        form = OrderForm(request.POST)

        # Validamos que los datos sean correctos y que pasen los filtros de seguridad (ej. monto > 0)
        if form.is_valid():
            order = form.save(commit=False)
            order.assigned_seller = request.user
            order.save()
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

    return render(request, "add_order.html", {"form": form, "user_role": role})


@login_required(login_url="home")
def update_order(request, order_id):
    """Edición administrativa completa de pedidos CRM."""
    role = get_user_role(request.user)
    if not is_admin(role):
        messages.error(request, "Solo el administrador puede editar pedidos CRM.")
        return redirect("list_orders")

    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = OrderAdminForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido actualizado correctamente por administración.")
            return redirect("admin_orders_dashboard")
    else:
        form = OrderAdminForm(instance=order)

    return render(
        request,
        "add_order.html",
        {
            "form": form,
            "user_role": role,
            "is_edit_mode": True,
            "order_id": order.id,
        },
    )


@login_required(login_url="home")
def delete_order(request, order_id):
    """Eliminación administrativa de pedidos CRM."""
    role = get_user_role(request.user)
    if not is_admin(role):
        messages.error(request, "Solo el administrador puede eliminar pedidos CRM.")
        return redirect("list_orders")

    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Pedido CRM eliminado correctamente.")
    return redirect("admin_orders_dashboard")


@login_required(login_url="home")
def admin_orders_dashboard(request):
    """Panel administrador con resumen global de pedidos CRM y tienda."""
    role = get_user_role(request.user)
    if not is_admin(role):
        messages.error(request, "Este panel es solo para administradores.")
        return redirect("home")

    crm_orders_qs = Order.objects.select_related("customer", "assigned_seller").order_by(
        "-created_at"
    )
    store_orders_qs = ProductOrder.objects.select_related("user", "product").order_by(
        "-created_at"
    )

    crm_total_sales = crm_orders_qs.aggregate(total=Sum("total_amount"))["total"] or 0
    store_total_sales = (
        store_orders_qs.aggregate(total=Sum("total_amount"))["total"] or 0
    )

    crm_by_status = crm_orders_qs.values("status").annotate(total=Count("id")).order_by(
        "status"
    )
    store_by_status = (
        store_orders_qs.values("status").annotate(total=Count("id")).order_by("status")
    )

    crm_paginator = Paginator(crm_orders_qs, 10)
    crm_page_number = request.GET.get("crm_page")
    crm_orders = crm_paginator.get_page(crm_page_number)

    store_paginator = Paginator(store_orders_qs, 10)
    store_page_number = request.GET.get("store_page")
    store_orders = store_paginator.get_page(store_page_number)

    return render(
        request,
        "admin_orders_dashboard.html",
        {
            "user_role": role,
            "crm_orders": crm_orders,
            "store_orders": store_orders,
            "crm_total_sales": crm_total_sales,
            "store_total_sales": store_total_sales,
            "crm_by_status": crm_by_status,
            "store_by_status": store_by_status,
        },
    )


@login_required(login_url="home")
def store_home(request):
    """Muestra el catálogo de tienda y los pedidos del usuario autenticado."""
    create_sample_products()
    role = get_user_role(request.user)
    products = Product.objects.filter(is_active=True).order_by("name")
    if is_admin(role):
        my_orders = ProductOrder.objects.select_related("user", "product").order_by(
            "-created_at"
        )[:20]
    else:
        my_orders = ProductOrder.objects.filter(user=request.user).select_related(
            "product"
        ).order_by("-created_at")[:8]

    return render(
        request,
        "store.html",
        {
            "products": products,
            "my_orders": my_orders,
            "user_role": role,
        },
    )


@login_required(login_url="home")
def create_store_order(request, product_id):
    """Crea un pedido de tienda para el usuario autenticado."""
    if request.method != "POST":
        return redirect("store_home")

    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity_raw = request.POST.get("quantity", "1").strip()

    if not quantity_raw.isdigit():
        messages.error(request, "La cantidad debe ser un número válido.")
        return redirect("store_home")

    quantity = int(quantity_raw)
    if quantity < 1:
        messages.error(request, "La cantidad mínima para pedir es 1.")
        return redirect("store_home")

    if quantity > product.stock:
        messages.error(
            request,
            f"No hay stock suficiente para {product.name}. Stock disponible: {product.stock}.",
        )
        return redirect("store_home")

    total_amount = product.price * quantity
    ProductOrder.objects.create(
        user=request.user,
        product=product,
        quantity=quantity,
        unit_price=product.price,
        total_amount=total_amount,
    )
    product.stock -= quantity
    product.save(update_fields=["stock"])

    messages.success(
        request,
        f"Pedido creado: {quantity} x {product.name}. Total: ${total_amount}.",
    )
    return redirect("store_home")
