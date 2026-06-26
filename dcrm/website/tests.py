from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase


class OrdersTemplateTests(SimpleTestCase):
    def test_orders_template_renders_with_create_order_link(self):
        request = RequestFactory().get("/pedidos/")

        rendered = render_to_string("orders.html", {"orders": []}, request=request)

        self.assertIn("Registrar Nuevo Pedido", rendered)
