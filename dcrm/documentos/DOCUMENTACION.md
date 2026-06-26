# Guía técnica del sistema Djangommerce

## 1. Objetivo del sistema

Djangommerce integra dos bloques principales:
- CRM de clientes y pedidos internos.
- Tienda de ropa con carrito y confirmación de compra.

El sistema usa Django, MySQL, Bootstrap local y una capa de permisos por roles para controlar qué puede hacer cada usuario.

## 2. Módulos y funcionalidades del sistema

### Login con roles
- Roles: `admin`, `vendedor` y `usuario`.
- El login se procesa en la pantalla principal.
- El registro público no expone selección de rol.
- El administrador puede crear usuarios con rol desde su panel.

### CRUD completo
- CRUD de clientes.
- CRUD de pedidos CRM.
- Alta, listado y eliminación de productos de ropa.
- Confirmación de pedidos de tienda desde un carrito.

### Menú SPA
- El menú principal mantiene acceso continuo a CRM, tienda y panel admin.
- La navegación es consistente y evita rutas dispersas.

### Alertas
- Mensajes de éxito, advertencia y error.
- Confirmaciones visuales para acciones críticas.

## 3. Interfaz y recursos locales

### Bootstrap local
- Bootstrap se carga desde archivos locales dentro de `dcrm/website/templates/static`.
- No se usan CDNs externos.

### Recursos locales
- Las imágenes de producto se guardan como rutas locales en `static/img/products`.
- Los iconos del sistema se representan con SVG embebido.
- El tema visual usa blanco, negro y grises.

## 4. Seguridad y buenas prácticas

### Validaciones y regex
- Validación de campos en formularios Django.
- Validación de monto positivo en pedidos.
- Validación de cantidad y stock en la tienda.
- Formato correcto de campos como correo, teléfono y contraseña.

### Seguridad de campos críticos
- Protección CSRF.
- `login_required` en vistas sensibles.
- Restricción de paneles por rol y permisos Django.
- Uso de `PROTECT` y `SET_NULL` en relaciones críticas.

### Cuatro capas de seguridad
- Autenticación.
- Autorización.
- Validación.
- Confirmación de acciones destructivas.

## 5. Modelo de datos

### Record
- Representa clientes.
- Incluye nombre, correo, teléfono, dirección y ubicación.

### Order
- Representa pedidos CRM y pedidos de tienda.
- Incluye cliente, vendedor reasignado, creador, canal, monto, descripción y estado.

### Product
- Representa prendas de ropa.
- Incluye nombre, descripción, imagen local, precio, stock y estado activo.

### ProductOrder
- Se conserva como referencia histórica, pero el flujo real de tienda usa `Order`.

## 6. Flujo funcional

### Login y home
- La vista `home` procesa autenticación.
- Si el login es correcto, se muestran los registros con paginación.
- Si falla, se muestra un mensaje de error.

### CRM
- El usuario autenticado puede ver registros.
- Usuarios con permisos pueden crear pedidos CRM.
- El admin puede reasignar y administrar pedidos.

### Tienda
- La tienda muestra productos de ropa.
- El usuario agrega productos a un carrito en sesión.
- El usuario confirma con "Realizar pedido".
- El pedido se registra en `Order` con canal `TIENDA`.

### Administración
- El admin crea usuarios con rol.
- El admin administra productos y fotos locales.
- El admin accede al panel global de pedidos.

## 7. Historial GitHub y documentación

### Historial real
- Commit count verificado: 9 commits.
- El objetivo de 20 commits todavía no se alcanza.
- La documentación lo reporta tal como está.

### README
- El archivo principal es [README.md](../README.md).
- Resume la solución y enlaza documentos técnicos.

### UML
- Diagramas PlantUML en [docs/uml](../docs/uml).

### Patrones
- Patrones y enfoques documentados en [docs/patrones.md](../docs/patrones.md).

## 8. Archivos clave

- [dcrm/website/models.py](dcrm/website/models.py)
- [dcrm/website/views.py](dcrm/website/views.py)
- [dcrm/website/forms.py](dcrm/website/forms.py)
- [dcrm/website/urls.py](dcrm/website/urls.py)
- [dcrm/website/templates/](dcrm/website/templates)
- [docs/uml/](../docs/uml)
- [docs/patrones.md](../docs/patrones.md)

## 9. Instalación y pruebas

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py test website
python manage.py runserver
```

## 10. Resumen final

Djangommerce es un CRM con tienda de ropa, carrito, panel administrativo, recursos locales, validaciones en backend y documentación técnica separada para cumplir con la entrega de módulos, seguridad, UML, patrones y README estructurado.