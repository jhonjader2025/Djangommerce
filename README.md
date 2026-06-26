# Djangommerce - CRM + Tienda con Roles

Sistema web en Django que integra:
- CRM de clientes y pedidos internos.
- Tienda de frutas con pedidos para usuarios autenticados.
- Control de acceso por roles: admin, vendedor y usuario.

## Tecnologias
- Python 3
- Django
- MySQL
- Bootstrap local (sin CDN)

## Modulos principales

### 1) CRM
- Login y registro de usuarios.
- CRUD de clientes (Record).
- Pedidos CRM (Order).
- Paginacion de clientes y pedidos.

### 2) Tienda
- Catalogo de productos (frutas).
- Pedido por producto para usuario autenticado.
- Control de stock.
- Historial de pedidos de tienda.

### 3) Roles y permisos
- `admin`:
  - Ver todos los pedidos CRM y tienda.
  - Crear, editar, eliminar pedidos CRM.
  - Cambiar cualquier estado del pedido CRM.
  - Reasignar pedidos CRM entre vendedores.
  - Ver resumen global: ventas totales y pedidos por estado.
- `vendedor`:
  - Crear pedidos CRM.
  - Gestion operativa limitada segun reglas de vistas.
- `usuario`:
  - Acceso principal a tienda para realizar pedidos.

## Flujo de pedidos

### Pedido CRM
1. Usuario con rol admin o vendedor entra a `Pedidos`.
2. Crea pedido con cliente, descripcion, monto y estado.
3. Si es admin, puede editar/eliminar y reasignar vendedor.

### Pedido Tienda
1. Usuario autenticado entra a `Tienda`.
2. Selecciona fruta y cantidad.
3. Sistema valida stock y crea pedido.
4. Se descuenta inventario del producto.

## Seguridad aplicada
- `@login_required` en vistas sensibles.
- Validaciones backend en formularios (ej. monto > 0).
- Control de permisos por rol en vistas de administracion.
- Proteccion CSRF en formularios.
- Uso de `PROTECT`/`SET_NULL` en relaciones criticas.

## Rutas clave
- `/` -> Home CRM
- `/pedidos/` -> listado pedidos CRM
- `/crear-pedido/` -> crear pedido CRM
- `/admin/pedidos/` -> panel administrativo de pedidos
- `/tienda/` -> catalogo de frutas

## Estructura relevante
- `dcrm/website/models.py` -> modelos de negocio
- `dcrm/website/views.py` -> logica de permisos y procesos
- `dcrm/website/forms.py` -> formularios y validaciones
- `dcrm/website/urls.py` -> rutas del sistema
- `dcrm/website/templates/` -> interfaz

## Migraciones nuevas incluidas
- `0004_product_productorder.py`
- `0005_order_assigned_seller.py`

## Pruebas
Ejecutar:

```bash
python manage.py test website
```

Resultado esperado: pruebas en estado OK.

## Requisitos de instalacion
1. Crear y activar entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar MySQL en `dcrm/dcrm/settings.py`.
4. Ejecutar migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Iniciar servidor:

```bash
python manage.py runserver
```

## Notas de entrega
- Se trabajo por commits funcionales por modulo.
- El modulo fuerte de la entrega es gestion de pedidos con roles.
- La documentacion principal del proyecto queda centralizada en este `README.md`.
