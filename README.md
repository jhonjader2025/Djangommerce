# Djangommerce

Sistema web en Django para CRM y tienda de ropa con control por roles. La aplicación combina gestión de clientes, pedidos CRM y pedidos de tienda en un solo flujo, con interfaz local, validaciones en backend y administración de productos con imágenes locales.

## 1. Módulos y funcionalidades del sistema

### Login con roles
- Roles actuales: `admin`, `vendedor` y `usuario`.
- El login se gestiona desde la página principal.
- El registro público crea usuarios como `usuario`.
- El administrador puede crear usuarios con rol desde su panel.

### CRUD completo
- CRUD de clientes (`Record`).
- CRUD de pedidos CRM (`Order`).
- Gestión de productos de ropa desde el panel admin.
- Eliminación segura de productos con confirmación.

### Menú SPA
- Navegación principal persistente con menú tipo aplicación.
- Acceso rápido a CRM, tienda, carrito, panel admin y gestión de productos.
- La interfaz mantiene una experiencia continua sin recargar la navegación completa del sistema.

### Alertas
- Mensajes de éxito, error y aviso con `django.contrib.messages`.
- Confirmaciones visuales para acciones críticas como eliminar y cerrar sesión.

## 2. Interfaz y recursos locales

### Bootstrap local
- Bootstrap se sirve desde archivos locales en `dcrm/website/templates/static`.
- No se utilizan CDNs para la interfaz base.

### Recursos locales
- Las imágenes de productos se resuelven como rutas locales dentro de `static/img/products`.
- Los iconos del sistema se renderizan con SVG embebido.
- El estilo visual está en un tema monocromático simple.

## 3. Seguridad y buenas prácticas

### Validaciones y regex
- Validaciones backend en formularios.
- Validación de monto mayor a cero en pedidos.
- Validación de cantidad y stock en tienda.
- Formato controlado para campos como correo, teléfono y datos de acceso.

### Seguridad de campos críticos
- Protección CSRF en formularios.
- Uso de `login_required` en vistas sensibles.
- Protección de acciones administrativas con permisos de rol.
- Relaciones críticas con `PROTECT` o `SET_NULL` según el caso.

### Cuatro capas de seguridad
- Autenticación de usuario.
- Autorización por rol.
- Validación de entrada.
- Restricción de acciones destructivas por permisos y confirmaciones.

## 4. Repositorio y documentación

### Historial GitHub
- Historial actual verificado: 9 commits.
- El requisito mínimo de 20 commits todavía no está cumplido.
- Este dato se documenta de forma realista para evitar promesas incorrectas.

### README estructurado
- Este archivo centraliza el resumen funcional y técnico.
- La guía profunda para desarrollo queda en [dcrm/DOCUMENTACION.md](dcrm/DOCUMENTACION.md).

### Arquitectura y modelado UML
- Diagramas PlantUML disponibles en `docs/uml`.
- Incluyen arquitectura general, roles y login, flujo CRM y flujo de tienda.

### Patrones documentados
- Los patrones y enfoques de diseño están documentados en [docs/patrones.md](docs/patrones.md).

## 5. Estado funcional del sistema

### CRM
- Login y registro.
- Listado de clientes con paginación.
- Crear, editar y eliminar clientes.
- Crear y administrar pedidos CRM.

### Tienda de ropa
- Catálogo local de ropa.
- Carrito intermedio antes de confirmar compra.
- Confirmación de pedido con "Realizar pedido".
- Fotos locales para productos.
- Gestión de productos desde el panel admin.

### Panel admin
- Crear usuarios con rol.
- Ver resumen de pedidos CRM y tienda.
- Reasignar pedidos CRM.
- Crear y eliminar productos.

## 6. Rutas principales
- `/` -> home
- `/pedidos/` -> pedidos CRM
- `/crear-pedido/` -> formulario de pedido CRM
- `/tienda/` -> tienda de ropa
- `/tienda/carrito/` -> carrito de compra
- `/admin/pedidos/` -> panel admin de pedidos
- `/admin/productos/` -> gestión admin de productos
- `/admin/usuarios/crear/` -> creación de usuarios con rol

## 7. Estructura relevante
- [dcrm/website/models.py](dcrm/website/models.py)
- [dcrm/website/views.py](dcrm/website/views.py)
- [dcrm/website/forms.py](dcrm/website/forms.py)
- [dcrm/website/urls.py](dcrm/website/urls.py)
- [dcrm/website/templates/](dcrm/website/templates)
- [docs/uml/](docs/uml)
- [docs/patrones.md](docs/patrones.md)

## 8. Instalación y ejecución
1. Activar el entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Ejecutar pruebas:

```bash
python manage.py test website
```

5. Levantar el servidor:

```bash
python manage.py runserver
```

## 9. Resumen corto

Djangommerce es un CRM en Django con tienda de ropa integrada, roles, panel administrativo, carrito de compra, imágenes locales y documentación técnica separada para UML y patrones.