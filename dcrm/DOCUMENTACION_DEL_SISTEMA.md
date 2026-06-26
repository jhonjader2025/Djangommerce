# Documentación del sistema DCRM

## 1. Estructura general

- `dcrm/manage.py`: punto de entrada de Django.
- `dcrm/dcrm/settings.py`: configuración principal de Django, base de datos, aplicaciones instaladas, archivos estáticos.
- `dcrm/dcrm/urls.py`: enruta la raíz a la app `website`.
- `dcrm/website/urls.py`: define las rutas internas de la app.
- `dcrm/website/views.py`: contiene la lógica de autenticación, listados, clientes y pedidos.
- `dcrm/website/forms.py`: formularios de registro de usuario, clientes y pedidos.
- `dcrm/website/models.py`: modelos `Record` y `Order`.
- `dcrm/website/templates/`: vistas HTML del frontend.
- `dcrm/website/tests.py`: pruebas básicas para verificar el render de plantillas del módulo de pedidos.

## 2. Funcionalidad principal actual

### 2.1 Login y home
- El formulario de login se procesa en la vista `home`.
- Si el usuario está autenticado, se muestran los `Record` paginados.
- Si el login falla, se muestra un mensaje de error.

### 2.2 Módulo de pedidos
- El sistema ahora cuenta con un módulo de pedidos funcional básico.
- Requiere que el usuario esté autenticado.
- Permite listar pedidos paginados.
- Permite crear un nuevo pedido desde un formulario.
- Cada pedido está asociado a un cliente existente (`Record`).

### 2.3 Rutas
- `''` -> `home`
- `'login/'` -> `login_user` (redirige a `home` porque el login se maneja desde `home`)
- `'logout/'` -> `logout_user`
- `'registrar/'` -> `register_user`
- `'record/<str:pk>'` -> `customer_record`
- `'delete-record/<str:pk>'` -> `delete_record`
- `'update-record/<str:pk>'` -> `update_record`
- `'pedidos/'` -> `list_orders`
- `'crear-pedido/'` -> `create_order`
- `'pedidos/crear/'` -> `create_order`

## 3. Cambios aplicados

### 3.1 `website/views.py`
- Se corrigió la vista `home` para:
  - usar `request.POST.get(...)` en lugar de accesos directos.
  - recuperar los registros solo si el usuario está autenticado.
  - paginar los resultados con `Paginator`.
- Se agregó la vista `list_orders(request)` para mostrar pedidos paginados.
- Se agregó la vista `create_order(request)` para procesar el formulario de creación.
- Ambas vistas están protegidas con `@login_required(login_url="home")`.

### 3.2 `website/forms.py`
- Se alinearon los nombres de campos del formulario con el modelo `Record`:
  - `phone_number` en lugar de `phone`.
- `RecordForm.Meta.fields` ahora incluye `phone_number`.
- Se agregó `OrderForm` para gestionar pedidos con campos: cliente, descripción, monto total y estado.
- `OrderForm` valida que `total_amount` sea mayor a cero.

### 3.3 Plantillas y UI
- Se corrigió la plantilla de pedidos para que use la ruta correcta `create_order`.
- Se agregaron las plantillas:
  - `orders.html` para listar pedidos.
  - `add_order.html` para crear pedidos.
- El botón de “Registrar Nuevo Pedido” ahora apunta a la URL correcta.

### 3.4 Pruebas
- Se añadió una prueba básica en `website/tests.py` para verificar que la plantilla `orders.html` renderiza correctamente el botón de creación.

## 4. Lógica del módulo de pedidos

### 4.1 Modelo
- `Order` representa un pedido del sistema.
- Está asociado a un cliente mediante `customer = ForeignKey(Record, on_delete=models.PROTECT)`.
- Tiene campos para:
  - `description`: detalle del pedido.
  - `total_amount`: monto total.
  - `status`: estado del pedido (`Pendiente`, `Pagado`, `Enviado`, `Cancelado`).
  - `created_at` y `updated_at`: fechas automáticas.

### 4.2 Flujo
1. El usuario inicia sesión.
2. Desde la vista de pedidos se lista el contenido existente.
3. Si el usuario pulsa “Registrar Nuevo Pedido”, se abre un formulario.
4. Al enviar el formulario, Django valida los datos.
5. Si la validación pasa, el pedido se guarda y se redirige al listado.
6. Si hay errores, se muestran mensajes de error.

### 4.3 Seguridad
- El módulo está protegido por sesión.
- Si el usuario no está autenticado, es redirigido a la página de inicio.
- El monto total debe ser mayor a cero.

## 5. Observaciones

- El modelo `Record` usa `phone_number`, por lo que todas las referencias deben coincidir con ese campo.
- La vista `home` ahora envía `records` vacío cuando el usuario no está autenticado, evitando errores de plantilla.
- El sistema funciona con la base de datos MySQL configurada en `settings.py`.
- El módulo de pedidos actualmente está en una versión básica, pero ya permite listar y crear pedidos.

## 6. Cómo probar

1. Activar el entorno virtual:
   - `entorno\Scripts\Activate.ps1`
2. Ejecutar migraciones si aplica:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
3. Crear usuario o registrar uno desde `/registrar/`.
4. Iniciar sesión desde `/`.
5. Abrir `/pedidos/` para ver el listado.
6. Usar “Registrar Nuevo Pedido” para crear uno nuevo.
7. Verificar que el pedido aparece en la tabla y que el sistema redirige correctamente.

## 7. Credenciales de administrador

- Usuario: `profesoradmin`
- Correo: `profesoradmin@example.com`
- Contraseña: `Admin1234!`

## 8. Comentarios de los cambios en el código

- En `website/views.py`, la vista `home` procesa login y carga registros.
- En `website/views.py`, se agregaron `list_orders` y `create_order`.
- En `website/forms.py`, se corrigió `phone_number` y se añadió `OrderForm`.
- En las plantillas, se añadió el flujo de pedidos y se corrigió la ruta de navegación del botón de creación.