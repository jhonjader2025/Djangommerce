# UML de Djangommerce

Este directorio contiene los diagramas PlantUML del sistema.

## Diagramas existentes

- [arquitectura.puml](arquitectura.puml): vista general de la arquitectura Django.
- [login_roles.puml](login_roles.puml): actores y acceso por roles.
- [pedidos_crm.puml](pedidos_crm.puml): flujo de creación de pedido CRM.
- [tienda_carrito.puml](tienda_carrito.puml): flujo de carrito y compra.
- [modelo_clases.puml](modelo_clases.puml): relaciones entre modelos del dominio.
- [casos_uso.puml](casos_uso.puml): actores y funcionalidades principales.
- [secuencia_checkout.puml](secuencia_checkout.puml): secuencia del proceso de compra.

## Orden recomendado para exponer

1. Arquitectura general.
2. Casos de uso.
3. Modelo de clases.
4. Secuencia de compra.
5. Flujos específicos de CRM y tienda.

## Idea de explicación

El sistema se apoya en una arquitectura Django clásica. Los usuarios se dividen por roles, el CRM gestiona clientes y pedidos internos, la tienda maneja el carrito y la compra confirmada, y el panel admin unifica la administración de usuarios, pedidos y productos.