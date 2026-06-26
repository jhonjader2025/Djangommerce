# Patrones y enfoques documentados

Este documento reúne 10 patrones, enfoques o decisiones de diseño observables en Djangommerce. Algunos son patrones clásicos y otros son prácticas arquitectónicas aplicadas al proyecto.

1. MTV de Django
- Separación entre modelos, vistas, templates y URLs.

2. CRUD
- Operaciones completas para clientes, pedidos y productos.

3. RBAC
- Control de acceso por roles: `admin`, `vendedor` y `usuario`.

4. Template Inheritance
- `base.html` actúa como plantilla base reutilizable.

5. Pagination Pattern
- Listados de clientes y pedidos paginados.

6. Session Cart
- El carrito de tienda vive en sesión antes de confirmar la compra.

7. Form Validation Pattern
- Formularios Django con validación en backend.

8. Guard Clauses
- Vistas críticas detienen el flujo si el usuario no tiene permisos.

9. Protection by Design
- CSRF, `login_required` y restricciones por rol en vistas sensibles.

10. PROTECT / SET_NULL Strategy
- Relaciones críticas protegidas para evitar borrados inseguros.

## Observación

Si necesitas ampliar la entrega, estos 10 puntos pueden convertirse en 4 diagramas UML + 4 patrones clásicos + 2 prácticas de seguridad/arquitectura, o en más documentación técnica por separado.
