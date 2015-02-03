from django.contrib.auth.models import User
from django.test import Client, TestCase


class TextPlusStuffTestCase(TestCase):
    """The test suite for django-textplusstuff"""

    fixtures = ['textplusstuff']

    def setUp(self):
        password = '12345'
        user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        client = Client()
        login = client.login(
            username='test',
            password=password
        )
        self.assertTrue(login)
        self.user = user
        self.client = client

    def test_textplusstuff_urls(self):
        """Tests the TextPlusStuff API reponse"""
        response = self.client.get('/textplusstuff/')
        del response
