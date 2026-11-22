from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class RegistrationTests(TestCase):
    def test_signup_accepts_rendered_fields(self):
        response = self.client.post(reverse('register'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone_number': '555-0100',
            'password': 'V3ryStrongPassword!',
            'agree_terms': 'on',
        })

        self.assertRedirects(response, reverse('dashboard'))
        user = User.objects.get(email='test@example.com')
        self.assertEqual(user.username, 'test@example.com')
        self.assertEqual(user.first_name, 'Test User')
        self.assertTrue(user.check_password('V3ryStrongPassword!'))


class BuyPageTests(TestCase):
    def test_admin_product_data_is_displayed_on_buy_page(self):
        category = Category.objects.create(name='Ceramic')
        product = Product.objects.create(
            name='Marble Tile',
            sku='MARBLE-001',
            category=category,
            description='Polished marble tile for living rooms.',
            price='2500.00',
            stock=12,
        )

        response = self.client.get(reverse('buy'))

        self.assertContains(response, product.name)
        self.assertContains(response, product.description)
        self.assertContains(response, 'KSh 2500.00')


class SelectedTileOrderTests(TestCase):
    def test_selected_tile_details_display_on_order_page(self):
        user = User.objects.create_user(username='tilecustomer', password='StrongPassword123!')
        category = Category.objects.create(name='Ceramic')
        product = Product.objects.create(
            name='Selected Marble Tile',
            sku='SELECTED-001',
            category=category,
            description='A selected marble tile.',
            price='3200.00',
            stock=10,
        )
        self.client.login(username='tilecustomer', password='StrongPassword123!')

        response = self.client.get(reverse('order'), {'product': product.id})

        self.assertContains(response, 'Selected Tile')
        self.assertContains(response, 'Tile ID')
        self.assertContains(response, str(product.id))
        self.assertContains(response, product.name)
        self.assertContains(response, '3200.00')
