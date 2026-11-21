from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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
