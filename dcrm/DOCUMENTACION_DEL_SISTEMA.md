# Documentación del sistema DCRM

## 1. Estructura general

- `dcrm/manage.py`: punto de entrada de Django.
- `dcrm/dcrm/settings.py`: configuración principal de Django, base de datos, aplicaciones instaladas, archivos estáticos.
- `dcrm/dcrm/urls.py`: enruta la raíz a la app `website`.
- `dcrm/website/urls.py`: define las rutas internas de la app.
- `dcrm/website/views.py`: contiene la lógica de autenticación, listados y manejo de registros.
- `dcrm/website/forms.py`: formularios de registro de usuario y de registros de clientes.
- `dcrm/website/models.py`: modelo `Record` que representa el cliente.
- `dcrm/website/templates/`: vistas HTML del frontend.

## 2. Funcionalidad principal corregida

### 2.1 Login y home
- El formulario de login se procesa en la vista `home`.
- Si el usuario está autenticado, se muestran los `Record` paginados.
- Si el login falla, se muestra un mensaje de error.

### 2.2 Rutas
- `''` -> `home`
- `'login/'` -> `login_user` (redirige a `home` porque el login se maneja desde `home`)
- `'logout/'` -> `logout_user`
- `'registrar/'` -> `register_user`
- `'record/<str:pk>'` -> `customer_record`
- `'delete-record/<str:pk>'` -> `delete_record`
- `'update-record/<str:pk>'` -> `update_record`

## 3. Cambios aplicados

### 3.1 `website/views.py`
- Se corrigió la vista `home` para:
  - usar `request.POST.get(...)` en lugar de accesos directos.
  - recuperar los registros solo si el usuario está autenticado.
  - paginar los resultados con `Paginator`.
- Se agregó comentario en `login_user` para explicar que el login se maneja desde `home`.

### 3.2 `website/forms.py`
- Se alinearon los nombres de campos del formulario con el modelo `Record`:
  - `phone_number` en lugar de `phone`.
- `RecordForm.Meta.fields` ahora incluye `phone_number`.

### 3.3 `website/templates/home.html`
- Se usó `record.phone_number` en lugar de `record.phone`.
- Se corrigió la URL para ver un registro a `customer_record`.

### 3.4 `website/templates/record.html`
- Se usó `customer_record.phone_number`.
- Se corrigió `customer_record.zip_code`.
- Se habilitaron los botones `Delete` y `Update Record`.

## 4. Observaciones

- El modelo `Record` usa `phone_number`, por lo que todas las referencias deben coincidir con ese campo.
- La vista `home` ahora envía `records` vacío cuando el usuario no está autenticado, evitando errores de plantilla.
- El sistema funciona con la base de datos MySQL configurada en `settings.py`.

## 5. Cómo probar

1. Activar el entorno virtual:
   - `entorno\Scripts\Activate.ps1`
2. Ejecutar migraciones:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
3. Crear usuario o registrar uno desde `/registrar/`.
4. Iniciar sesión desde `/`.
5. Ver los registros creados y navegar con paginación.
## 7. Credenciales de administrador

- Usuario: `profesoradmin`
- Correo: `profesoradmin@example.com`
- Contraseña: `Admin1234!`
---

## 6. Comentarios de los cambios en el código

- En `website/views.py`, la vista `home` ahora procesa login y carga registros.
- En `website/forms.py`, se corrigió `phone_number` para que coincida con el modelo.
- En `website/templates/record.html`, se ajustaron referencias a `customer_record.phone_number` y `customer_record.zip_code`.
