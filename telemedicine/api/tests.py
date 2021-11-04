from django.test import TestCase, Client
from users.models import User
from rest_framework import status
from django.urls import reverse
from allauth.account.models import EmailAddress

import json

content_type = 'application/json'

# Create your tests here.

class SignUpTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {'username': 'test',
                           'email': 'test@gmail.com',
                           'password1': 'testpass',
                           'password2': 'testpass'}

    def post(self, data, url='rest_register'):
        return self.client.post(reverse(url), data=data, content_type=content_type)

    def setUp(self):
        self.client = Client()

    def test_sign_up(self):
        response = self.post(self.credentials)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sign_up_with_empty_username(self):
        cred = self.credentials.copy()
        cred['username'] = ''
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_empty_email(self):
        cred = self.credentials.copy()
        cred['email'] = ''
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_invalid_email(self):
        cred = self.credentials.copy()
        cred['email'] = 'test.com'
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_miss_matched_passwords(self):
        cred = self.credentials.copy()
        cred['password2'] = 'test'
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_duplicate_email(self):
        User.objects.create(username='test', email='test@gmail.com', password='testpass')
        response = self.post(self.credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_duplicate_username(self):
        User.objects.create(username='test', email='test@gmail.com', password='testpass')
        response = self.post(self.credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_short_password_less_than_8(self):
        cred = self.credentials.copy()
        cred['password1'] = '123'
        cred['password2'] = '123'
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {'email': 'test@gmail.com', 'password': 'testpass'}

    def post(self, data, url='rest_login'):
        return self.client.post(reverse(url), json.dumps(data), content_type=content_type)

    def setUp(self):
        self.client = Client()

        signup_cred = {'username': 'test',
                       'email': 'test@gmail.com',
                       'password1': 'testpass',
                       'password2': 'testpass'}

        self.post(signup_cred, 'rest_register')
        email = EmailAddress.objects.get(email='test@gmail.com')
        email.verified = '1'
        email.save()

    def test_login(self):
        response = self.post(self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_empty_email(self):
        cred = self.credentials.copy()
        cred['email'] = ''
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_empty_password(self):
        cred = self.credentials.copy()
        cred['password'] = ''
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_wrong_password(self):
        cred = self.credentials.copy()
        cred['password'] = 'wrongpass'
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_unavailable_email(self):
        cred = self.credentials.copy()
        cred['email'] = 'notest@gmail.com'
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FunctionalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.sign_up_cred = {'username': 'test',
                            'email': 'test@gmail.com',
                            'password1': 'testpass',
                            'password2': 'testpass'}
        cls.login_cred = {'email': 'test@gmail.com', 'password': 'testpass'}

    def post(self, data, url):
        return self.client.post(reverse(url), json.dumps(data), content_type=content_type)

    def sign_up(self):
        response = self.post(self.sign_up_cred, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login(self):
        response = self.post(self.login_cred, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def verify_email(self):
        email = EmailAddress.objects.get(email='test@gmail.com')
        email.verified = '1'
        email.save()

        email = EmailAddress.objects.get(email='test@gmail.com')
        self.assertEqual(email.verified, True)

    def test_run_functional_test(self):
        self.sign_up()
        self.verify_email()
        self.login()
