from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase

from .views import can_manage_records, get_user_role


class OrdersTemplateTests(SimpleTestCase):
    def test_orders_template_renders_with_create_order_link(self):
        request = RequestFactory().get("/pedidos/")

        rendered = render_to_string(
            "orders.html", {"orders": [], "user_role": "admin"}, request=request
        )

        self.assertIn("Registrar Nuevo Pedido", rendered)


class RoleHelperTests(SimpleTestCase):
    def test_basic_user_has_basic_role_by_default(self):
        class AnonymousUser:
            is_authenticated = False

        self.assertEqual(get_user_role(AnonymousUser()), "usuario")

    def test_authenticated_user_uses_profile_role(self):
        class Profile:
            role = "vendedor"

        class AuthUser:
            is_authenticated = True
            profile = Profile()

        self.assertEqual(get_user_role(AuthUser()), "vendedor")

    def test_only_admin_and_vendedor_can_manage_records(self):
        self.assertTrue(can_manage_records("admin"))
        self.assertTrue(can_manage_records("vendedor"))
        self.assertFalse(can_manage_records("usuario"))
