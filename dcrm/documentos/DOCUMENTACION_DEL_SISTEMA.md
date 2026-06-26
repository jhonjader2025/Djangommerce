# Documentación del sistema Djangommerce

## 1. Estructura general

- `dcrm/manage.py`: entrada principal de Django.
- `dcrm/dcrm/settings.py`: configuración general, base de datos y estáticos.
- `dcrm/dcrm/urls.py`: enruta la aplicación principal y las rutas de administración.
- `dcrm/website/models.py`: modelos `Record`, `Order`, `Product` y `ProductOrder`.
- `dcrm/website/views.py`: autenticación, CRM, tienda y administración.
- `dcrm/website/forms.py`: formularios con validaciones.
- `dcrm/website/templates/`: interfaz HTML.
- `dcrm/website/tests.py`: pruebas básicas.

## 2. Funcionalidad principal actual

### 2.1 Login con roles
- Roles activos: `admin`, `vendedor` y `usuario`.
- El login se maneja desde la vista `home`.
- El registro público crea usuarios normales.
- El admin puede crear usuarios con rol desde el panel.

### 2.2 CRM
- Listado de clientes con paginación.
- CRUD de clientes.
- CRUD de pedidos CRM.
- Reasignación de pedidos a vendedores.

### 2.3 Tienda de ropa
- Catálogo de ropa con imágenes locales.
- Carrito en sesión.
- Confirmación final con "Realizar pedido".
- Registro de pedidos en el mismo modelo `Order`.

### 2.4 Administración
- Panel admin de pedidos.
- Panel admin de productos.
- Creación de usuarios con rol.
- Eliminación segura de productos.

## 3. Rutas

- `''` -> `home`
- `'login/'` -> `login_user`
- `'logout/'` -> `logout_user`
- `'registrar/'` -> `register_user`
- `'pedidos/'` -> `list_orders`
- `'crear-pedido/'` -> `create_order`
- `'pedidos/crear/'` -> `create_order`
- `'admin/pedidos/'` -> `admin_orders_dashboard`
- `'admin/productos/'` -> `admin_manage_products`
- `'admin/usuarios/crear/'` -> `admin_create_user`
- `'tienda/'` -> `store_home`
- `'tienda/carrito/'` -> `store_cart`
- `'tienda/carrito/checkout/'` -> `checkout_store_cart`

## 4. Cambios aplicados

### 4.1 Vista y formularios
- `home` procesa login y muestra registros.
- `OrderForm` valida monto positivo.
- `ProductAdminForm` permite cargar productos con imagen local.
- `UserRegisterForm` no expone la selección de rol.

### 4.2 Modelo de productos
- `Product.image_url` guarda una ruta local.
- Las imágenes se renderizan desde `static/img/products`.
- Los productos base usan SVG locales.

### 4.3 Seguridad
- `login_required` protege vistas sensibles.
- CSRF activo en formularios.
- Paneles especiales limitados por rol y permisos Django.

## 5. Evidencia de requisitos cubiertos

- Login con roles: implementado.
- CRUD completo: implementado.
- Menú SPA: implementado en navegación persistente.
- Alertas: implementadas con mensajes Django.
- Bootstrap local: implementado.
- Validaciones regex y backend: implementadas.
- Seguridad de campos críticos: implementada.
- Cuatro capas de seguridad: documentadas arriba.
- README.md estructurado: implementado.
- UML PlantUML: implementado en `docs/uml`.
- Patrones documentados: implementado en `docs/patrones.md`.

## 6. Observación sobre GitHub

- Historial actual verificado: 9 commits.
- El requisito de 20 commits aún no está cumplido.
- La documentación reporta el valor real del repositorio.

## 7. Cómo probar

1. Activar el entorno virtual.
2. Ejecutar migraciones.
3. Ejecutar pruebas:

```bash
python manage.py test website
```

4. Levantar el servidor:

```bash
python manage.py runserver
```

## 8. Resumen final

El sistema ya integra CRM, tienda de ropa, panel administrativo, imágenes locales, navegación continua, validaciones y seguridad por roles. La documentación ahora queda alineada con esa implementación y con la lista de entrega solicitada.