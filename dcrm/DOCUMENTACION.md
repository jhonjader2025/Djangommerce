# Guía para desarrolladores del sistema DCRM

## 1. Qué hace este sistema

Este proyecto es una aplicación web hecha con Django para gestionar registros de clientes y, en su estado actual, también un módulo básico de pedidos. La idea principal es permitir:

- registrar usuarios del sistema,
- iniciar sesión y cerrar sesión,
- ver una lista de clientes/records,
- ver detalles de un registro,
- actualizar y eliminar registros,
- listar y crear pedidos relacionados con un cliente,
- navegar con paginación.

El módulo de pedidos ya está integrado de forma básica y se puede usar desde la interfaz una vez que el usuario ha iniciado sesión.

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
- [dcrm/website/tests.py](dcrm/website/tests.py): pruebas básicas.

---

## 4. Arquitectura general

El sistema sigue el patrón MVC clásico de Django:

- Modelos: definen la estructura de los datos.
- Vistas: procesan solicitudes y responden con HTML o redirecciones.
- Templates: muestran la interfaz de usuario.
- URLs: conectan rutas con vistas.
- Forms: validan y procesan datos del usuario.

Actualmente, la lógica está concentrada en la app llamada website, que maneja autenticación, clientes y pedidos.

---

## 5. Modelo de datos actual

### 5.1 Modelo Record

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

### 5.2 Modelo Order

El módulo de pedidos usa el modelo Order, también en [dcrm/website/models.py](dcrm/website/models.py).

Campos:

- customer: relación con Record
- description: detalle del pedido
- total_amount: monto total
- status: estado del pedido
- created_at: fecha automática de creación
- updated_at: fecha automática de actualización

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

## 7. Lógica del módulo de pedidos

### 7.1 Qué hace

El módulo de pedidos ya implementa lo siguiente:

- listar pedidos paginados,
- crear un nuevo pedido desde un formulario,
- asociar el pedido a un cliente existente,
- guardar el estado y monto del pedido,
- redirigir al listado después de crear un pedido.

### 7.2 Vistas relacionadas

- `list_orders(request)`: recupera todos los pedidos ordenados por fecha descendente y los muestra con paginación.
- `create_order(request)`: si llega por GET, muestra el formulario; si llega por POST, valida y guarda el pedido.

### 7.3 Formularios

El formulario de pedidos está en [dcrm/website/forms.py](dcrm/website/forms.py) y contiene:

- cliente (`customer`)
- descripción (`description`)
- monto total (`total_amount`)
- estado (`status`)

La lógica de validación asegura que el monto sea mayor a cero.

### 7.4 Plantillas

- [dcrm/website/templates/orders.html](dcrm/website/templates/orders.html): muestra la tabla con los pedidos.
- [dcrm/website/templates/add_order.html](dcrm/website/templates/add_order.html): muestra el formulario para registrar un pedido.

### 7.5 Protección

El módulo está protegido con `@login_required(login_url="home")`, por lo que si el usuario no está autenticado se le redirige a la home.

---

## 8. Rutas actuales

En [dcrm/website/urls.py](dcrm/website/urls.py) están definidas estas rutas:

- '': home
- 'login/': login_user
- 'logout/': logout_user
- 'registrar/': register_user
- 'record/<str:pk>': customer_record
- 'delete-record/<str:pk>': delete_record
- 'update-record/<str:pk>': update_record
- 'pedidos/': list_orders
- 'crear-pedido/': create_order
- 'pedidos/crear/': create_order

La ruta raíz está conectada desde [dcrm/dcrm/urls.py](dcrm/dcrm/urls.py).

---

## 9. Vistas y responsabilidades

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

### list_orders(request)

Muestra todos los pedidos, paginados y ordenados por fecha de creación.

### create_order(request)

Muestra o procesa el formulario de creación de pedidos.

---

## 10. Formularios

Los formularios principales están en [dcrm/website/forms.py](dcrm/website/forms.py).

- UserRegisterForm: para crear usuarios del sistema.
- RecordForm: para crear o editar registros de clientes.
- OrderForm: para crear o editar pedidos.

Estos formularios validan datos como correo, nombre, contraseña y monto del pedido.

---

## 11. Templates y frontend

La interfaz está en [dcrm/website/templates](dcrm/website/templates), con archivos como:

- base.html: estructura base de la web.
- home.html: pantalla principal, login y listado de clientes.
- register.html: formulario de registro.
- record.html: detalle de un cliente.
- update_record.html: formulario de edición.
- orders.html: listado de pedidos.
- add_order.html: formulario de registro de pedidos.

---

## 12. Base de datos y configuración

La configuración de la base de datos está en [dcrm/dcrm/settings.py](dcrm/dcrm/settings.py).

Actualmente está configurada para usar MySQL con una base llamada clientes. El proyecto también tiene archivos estáticos configurados para servir desde la carpeta templates/static.

### Verificación actual

Se validó el proyecto con:

- python manage.py check

Resultado: sin errores.

---

## 13. Puntos importantes para entender el sistema

- El sistema está pensado como un CRM simple, no como una plataforma compleja.
- La autenticación ya está integrada con Django y funciona a nivel de usuario.
- La app website es el núcleo del proyecto y concentra muchas responsabilidades.
- El modelo Record es la entidad de clientes y será la base natural para otros módulos.
- El módulo de pedidos funciona sobre esa base y está protegido por login.

---

## 14. Cambios recientes aplicados al módulo de pedidos

- Se agregó el modelo `Order`.
- Se añadieron las vistas `list_orders` y `create_order`.
- Se añadieron las plantillas `orders.html` y `add_order.html`.
- Se corrigió el vínculo del botón para que apunte a la URL correcta.
- Se añadió una prueba simple para verificar el render del listado de pedidos.

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

Este proyecto es un CRM básico en Django para gestionar clientes. Ya tiene autenticación de usuarios, listado y CRUD de registros, paginación y una base de datos MySQL. Además, ahora cuenta con un módulo de pedidos básico que permite listar y crear pedidos asociados a clientes, todo protegido por login y validado en el backend.
