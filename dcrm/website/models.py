# dcrm/website/models.py

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("usuario", "Usuario básico"),
        ("vendedor", "Vendedor"),
        ("admin", "Administrador"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="usuario")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Record(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    email = models.EmailField(max_length=100)

    phone_number = models.CharField(max_length=15)

    address = models.CharField(max_length=100)

    city = models.CharField(max_length=50)

    state = models.CharField(max_length=50)

    zip_code = models.CharField(max_length=10)

    # Método para representar el objeto como cadena
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"


class Order(models.Model):
    """
    Modelo que representa un Pedido dentro del sistema DCRM.
    Vincula a un cliente (Record) con la información de su compra.
    """

    # ESTADOS DEL PEDIDO: Definimos las opciones para el campo status
    STATUS_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("Pagado", "Pagado"),
        ("Enviado", "Enviado"),
        ("Cancelado", "Cancelado"),
    ]

    CHANNEL_CHOICES = [
        ("CRM", "CRM"),
        ("TIENDA", "Tienda"),
    ]

    # RELACIÓN: Cada pedido pertenece a un cliente (Record).
    # Como Record está en este mismo archivo, Django lo reconoce directamente.
    # Usamos models.PROTECT por seguridad: si intentan borrar un cliente con pedidos,
    # Django protegerá la base de datos y no dejará borrar al cliente para no perder el historial financiero.
    customer = models.ForeignKey(
        Record, on_delete=models.PROTECT, verbose_name="Cliente"
    )

    # Reasignación administrativa del pedido a un vendedor responsable
    assigned_seller = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_crm_orders",
        verbose_name="Vendedor Asignado",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_orders",
        verbose_name="Creado Por",
    )

    channel = models.CharField(
        max_length=10,
        choices=CHANNEL_CHOICES,
        default="CRM",
        verbose_name="Canal",
    )

    # CAMPOS DE DETALLE
    description = models.TextField(
        max_length=500, verbose_name="Descripción del Pedido/Productos"
    )

    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Monto Total"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pendiente",
        verbose_name="Estado del Pedido",
    )

    # FECHAS AUTOMÁTICAS CON SEGURIDAD DE REGISTRO
    # auto_now_add=True guarda la fecha exacta de creación sin permitir alteraciones externas
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación"
    )

    # auto_now=True actualiza la fecha automáticamente con cada interacción/modificación
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Última Actualización"
    )

    def __str__(self):
        # Retorna una representación legible para auditorías y administración
        return f"Pedido #{self.id} - {self.customer.first_name} {self.customer.last_name} ({self.status})"


class Product(models.Model):
    """Productos para el módulo de tienda (catálogo simple)."""

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(max_length=300, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class ProductOrder(models.Model):
    """Pedido de tienda realizado por un usuario autenticado."""

    STATUS_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("Pagado", "Pagado"),
        ("Entregado", "Entregado"),
        ("Cancelado", "Cancelado"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store_orders")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pendiente")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Pedido Tienda #{self.id} - {self.user.username} - "
            f"{self.product.name} x{self.quantity}"
        )
