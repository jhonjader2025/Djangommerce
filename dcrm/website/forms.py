# dcrm/website/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import Order, Product, UserProfile


from .models import Record


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="", widget=forms.EmailInput(attrs={"placeholder": "Correo electronico"})
    )
    first_name = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Nombre"})
    )
    last_name = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Apellido"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Nombre de usuario"
        self.fields["username"].label = ""
        self.fields["username"].help_text = (
            '<span class="form-text text-muted">Requerido. 150 caracteres o menos. '
            "Letras, digitos y @/./+/-/_ solamente.</span>"
        )

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Contrasena"
        self.fields["password1"].label = ""
        self.fields["password1"].help_text = (
            '<ul class="form-text text-muted">'
            "<li>Tu contrasena no puede ser demasiado similar a tu otra informacion personal.</li>"
            "<li>Tu contrasena debe contener al menos 8 caracteres.</li>"
            "<li>Tu contrasena no puede ser una contrasena comun.</li>"
            "<li>Tu contrasena no puede ser completamente numerica.</li>"
            "</ul>"
        )

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirmar contrasena"
        self.fields["password2"].label = ""
        self.fields["password2"].help_text = (
            '<span class="form-text text-muted">Requerido. Debe coincidir con la contrasena anterior.</span>'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = "usuario"
            profile.save()
        return user


class AdminUserCreateForm(UserRegisterForm):
    ROLE_CHOICES = [
        ("usuario", "Usuario básico"),
        ("vendedor", "Vendedor"),
        ("admin", "Administrador"),
    ]

    role = forms.ChoiceField(
        label="",
        choices=ROLE_CHOICES,
        initial="usuario",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta(UserRegisterForm.Meta):
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].widget.attrs["class"] = "form-control"
        self.fields["role"].label = ""
        self.fields["role"].help_text = (
            '<span class="form-text text-muted">Selecciona el rol del nuevo usuario.</span>'
        )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data.get("role", "usuario")
            profile.save()
        return user


class RecordForm(forms.ModelForm):
    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Nombre", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Apellido", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
    )
    # Corregido para usar phone_number, que coincide con el campo del modelo Record.
    phone_number = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Telefono", "class": "form-control"}
        ),
    )
    address = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Direccion", "class": "form-control"}
        ),
    )
    city = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Ciudad", "class": "form-control"}
        ),
    )
    state = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Estado", "class": "form-control"}
        ),
    )
    zip_code = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Codigo Postal", "class": "form-control"}
        ),
    )

    class Meta:
        model = Record
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "city",
            "state",
            "zip_code",
        ]


class OrderForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Pedidos (Order).
    Maneja la vinculación con el cliente y los detalles de la compra.
    """

    class Meta:
        model = Order
        # Especificamos los campos que se le mostrarán al usuario en el frontend.
        # 'customer' generará automáticamente un dropdown seguro con los clientes existentes (Records).
        fields = ["customer", "description", "total_amount", "status"]

        # personalizamos los campos con Bootstrap para que se vea genial y profesional
        widgets = {
            "customer": forms.Select(
                attrs={"class": "form-control", "placeholder": "Seleccione el cliente"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Detalla los productos o el concepto del pedido...",
                }
            ),
            "total_amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0.00", "step": "0.01"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    # =====================================================================
    # CAPA DE SEGURIDAD: Validamos los datos en el backend antes de guardar
    # =====================================================================
    def clean_total_amount(self):
        """
        Validación de seguridad: Evita que registren pedidos con montos
        negativos o vacíos en el sistema.
        """
        total = self.cleaned_data.get("total_amount")
        if total is not None and total <= 0:
            raise forms.ValidationError(
                "Por seguridad, el monto total del pedido debe ser mayor a 0."
            )
        return total


class OrderAdminForm(OrderForm):
    """Formulario para administración total de pedidos (incluye reasignación)."""

    assigned_seller = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Vendedor Asignado",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta(OrderForm.Meta):
        fields = [
            "customer",
            "assigned_seller",
            "description",
            "total_amount",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_seller"].queryset = User.objects.filter(
            profile__role__in=["vendedor", "admin"]
        ).order_by("username")


class ProductAdminForm(forms.ModelForm):
    """Formulario para que admin cargue productos de ropa con imagen local."""

    class Meta:
        model = Product
        fields = ["name", "description", "image_url", "price", "stock", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del producto"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descripción corta de la prenda...",
                }
            ),
                "image_url": forms.ClearableFileInput(
                    attrs={"class": "form-control", "accept": "image/*"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}
            ),
            "stock": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("El precio debe ser mayor a cero.")
        return price
