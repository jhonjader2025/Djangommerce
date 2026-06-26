# Guía para desarrolladores del sistema DCRM

## 1. Qué hace este sistema

Este proyecto es una aplicación web sencilla hecha con Django para gestionar registros de clientes. La idea principal es permitir:

- registrar usuarios del sistema,
- iniciar sesión y cerrar sesión,
- ver una lista de clientes/records,
- ver detalles de un registro,
- actualizar y eliminar registros,
- navegar con paginación.

En su estado actual, no existe todavía un módulo de pedidos. El sistema está orientado a CRM básico (clientes), y el módulo de pedidos deberá integrarse sobre esa base.

---

## 2. Tecnologías usadas

- Python
- Django
- MySQL
- HTML + Bootstrap (templates)
- Django auth (usuarios, login, registro)

---

## 3. Estructura del proyecto

Proyecto principal:

- [dcrm/manage.py](dcrm/manage.py): punto de entrada de Django.
- [dcrm/dcrm/settings.py](dcrm/dcrm/settings.py): configuración general del proyecto.
- [dcrm/dcrm/urls.py](dcrm/dcrm/urls.py): rutas globales.

Aplicación principal:

- [dcrm/website/models.py](dcrm/website/models.py): modelos de datos.
- [dcrm/website/views.py](dcrm/website/views.py): lógica de negocio y controladores.
- [dcrm/website/forms.py](dcrm/website/forms.py): formularios.
- [dcrm/website/urls.py](dcrm/website/urls.py): rutas internas de la app.
- [dcrm/website/templates](dcrm/website/templates): plantillas HTML.

---

## 4. Arquitectura general

El sistema sigue el patrón MVC clásico de Django:

- Modelos: definen la estructura de los datos.
- Vistas: procesan solicitudes y responden con HTML o redirecciones.
- Templates: muestran la interfaz de usuario.
- URLs: conectan rutas con vistas.
- Forms: validan y procesan datos del usuario.

Actualmente, la lógica está concentrada en la app llamada website, que maneja tanto autenticación como gestión de clientes.

---

## 5. Modelo de datos actual

El modelo principal es Record, definido en [dcrm/website/models.py](dcrm/website/models.py).

Campos:

- created_at: fecha de creación automática
- first_name: nombre
- last_name: apellido
- email: correo electrónico
- phone_number: teléfono
- address: dirección
- city: ciudad
- state: estado/provincia
- zip_code: código postal

Este modelo representa a un cliente o contacto del sistema.

### Importante

El sistema ya está usando el campo phone_number. Algunas partes antiguas podrían referirse a phone, pero la implementación actual usa phone_number.

---

## 6. Flujo funcional del sistema

### 6.1 Inicio y login

La vista home en [dcrm/website/views.py](dcrm/website/views.py) maneja dos cosas:

- si el usuario entra por primera vez, muestra el formulario de login;
- si envía credenciales, intenta autenticar al usuario.

Si el login es correcto:

- se inicia sesión con Django,
- se muestra el listado de registros,
- se muestran mensajes de éxito.

Si falla:

- se muestra un mensaje de error.

### 6.2 Registro de usuarios

La vista register_user permite crear un usuario nuevo usando UserRegisterForm.

### 6.3 Listado de clientes

Cuando el usuario está autenticado, la vista home:

- carga todos los registros de la base de datos,
- los ordena por fecha de creación descendente,
- aplica paginación de 10 registros por página.

### 6.4 Ver un registro específico

La vista customer_record muestra un detalle de un cliente por su ID.

### 6.5 Actualizar y eliminar registros

- update_record: permite editar los datos de un cliente.
- delete_record: elimina un cliente del sistema.

Ambas vistas están protegidas para que solo usuarios autenticados puedan ejecutarlas.

---

## 7. Rutas actuales

En [dcrm/website/urls.py](dcrm/website/urls.py) están definidas estas rutas:

- '': home
- 'login/': login_user
- 'logout/': logout_user
- 'registrar/': register_user
- 'record/<str:pk>': customer_record
- 'delete-record/<str:pk>': delete_record
- 'update-record/<str:pk>': update_record

La ruta raíz está conectada desde [dcrm/dcrm/urls.py](dcrm/dcrm/urls.py).

---

## 8. Vistas y responsabilidades

### home(request)

Esta es la vista principal. Hace lo siguiente:

- procesa el login si viene por POST,
- si el usuario está autenticado, carga los registros y los pagina,
- renderiza la plantilla home.html.

### login_user(request)

Actualmente no realiza el login directamente, porque esa lógica está en home. Solo redirige al inicio.

### logout_user(request)

Cierra la sesión y redirige a home.

### register_user(request)

Crea un usuario nuevo mediante formulario.

### delete_record(request, pk)

Elimina un Record por su ID.

### update_record(request, pk)

Edita un Record existente.

### customer_record(request, pk)

Muestra un detalle del cliente.

---

## 9. Formularios

Los formularios principales están en [dcrm/website/forms.py](dcrm/website/forms.py).

- UserRegisterForm: para crear usuarios del sistema.
- RecordForm: para crear o editar registros de clientes.

Estos formularios validan datos como correo, nombre y contraseña.

---

## 10. Templates y frontend

La interfaz está en [dcrm/website/templates](dcrm/website/templates), con archivos como:

- base.html: estructura base de la web.
- home.html: pantalla principal, login y listado de clientes.
- register.html: formulario de registro.
- record.html: detalle de un cliente.
- update_record.html: formulario de edición.

La vista home tiene un diseño con dos secciones:

- una para login o bienvenida,
- otra para listar registros si el usuario ya inició sesión.

---

## 11. Base de datos y configuración

La configuración de la base de datos está en [dcrm/dcrm/settings.py](dcrm/dcrm/settings.py).

Actualmente está configurada para usar MySQL con una base llamada clientes. El proyecto también tiene archivos estáticos configurados para servir desde la carpeta templates/static.

### Verificación actual

Se validó el proyecto con:

- python manage.py check

Resultado: sin errores.

---

## 12. Puntos importantes para entender el sistema

- El sistema está pensado como un CRM simple, no como una plataforma compleja.
- La autenticación ya está integrada con Django y funciona a nivel de usuario.
- La app website es el núcleo del proyecto y concentra muchas responsabilidades.
- El modelo Record es la entidad de clientes y será la base natural para otros módulos.
- El login no está en una vista separada; se procesa desde home.

---

## 13. Cómo debería integrarse el módulo de pedidos

Para implementar pedidos, lo más limpio sería pensar en el sistema así:

### Opción recomendada

Crear un nuevo módulo o app llamada orders que tenga:

- un modelo Order para representar un pedido,
- un modelo OrderItem si se necesita detalle por producto,
- vistas para listar, crear, ver y editar pedidos,
- templates para la interfaz,
- rutas propias.

### Relación con el modelo actual

El modelo Record (cliente) puede servir como relación para un pedido. Por ejemplo:

- un pedido pertenece a un cliente (Record)
- un cliente puede tener muchos pedidos

Eso permitiría que cada pedido esté asociado a un usuario/cliente existente.

### Recomendación de diseño

Modelo Order:

- customer: relación con Record
- created_at: fecha
- status: estado del pedido
- total: total del pedido
- notes: observaciones

Modelo OrderItem:

- order: relación con Order
- product_name: nombre del producto
- quantity: cantidad
- price: precio unitario

### Integración con la autenticación actual

El módulo de pedidos debería reutilizar el sistema de login y sesiones ya existente. Un usuario autenticado debería poder crear y ver pedidos.

### Lugar donde conectar la nueva UI

La pantalla principal home podría ampliarse para mostrar también un acceso a pedidos, o se podría crear una ruta nueva como /pedidos/.

---

## 14. Recomendaciones para los desarrolladores que vayan a trabajar el módulo

1. Entender primero el modelo Record y la lógica de autenticación.
2. Mantener el estilo actual de las vistas y plantillas.
3. No duplicar lógica de login; reutilizar la sesión existente.
4. Si el módulo será grande, conviene separarlo en una app nueva para mantener orden.
5. Para futuras mejoras, sería recomendable migrar a una arquitectura más limpia con apps específicas como customers, orders, users, etc.

---

## 15. Cómo arrancar el proyecto

1. Activar el entorno virtual:
   - entorno\Scripts\Activate.ps1
2. Entrar a la carpeta del proyecto:
   - cd dcrm
3. Ejecutar:
   - python manage.py migrate
   - python manage.py runserver

---

## 16. Resumen corto para pasar a otros devs

Este proyecto es un CRM básico en Django para gestionar clientes. Ya tiene autenticación de usuarios, listado y CRUD de registros, paginación y una base de datos MySQL. El punto de entrada principal es la vista home, que también maneja el login. El módulo de pedidos debería integrarse como una nueva funcionalidad sobre el modelo Record y reutilizando el sistema de autenticación actual.
