from rest_framework.test import APITestCase
from users.models import User
from rest_framework import status
from django.urls import reverse
from allauth.account.models import EmailAddress
from PIL import Image
from io import BytesIO


# Create your tests here.

class SignUpTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {'email': 'test@gmail.com',
                           'password1': 'testpass',
                           'password2': 'testpass',
                           'is_doctor': False}

    def post(self, data, url='rest_register'):
        return self.client.post(reverse(url), data)

    def test_sign_up(self):
        response = self.post(self.credentials)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        User.objects.create(email='test@gmail.com', password='testpass')
        response = self.post(self.credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_empty_is_doctor(self):
        cred = self.credentials.copy()
        cred['is_doctor'] = None
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {'email': 'test@gmail.com', 'password': 'testpass'}

    def post(self, data, url='rest_login'):
        return self.client.post(reverse(url), data)

    def setUp(self):
        signup_cred = {'email': 'test@gmail.com',
                       'password1': 'testpass',
                       'password2': 'testpass',
                       'is_doctor': False}

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


class ResetPasswordTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.credentials = {'email': 'test@gmail.com'}

    def post(self, data, url='rest_password_reset'):
        return self.client.post(reverse(url), data)

    def setUp(self):
        signup_cred = {'email': 'test@gmail.com',
                       'password1': 'testpass',
                       'password2': 'testpass',
                       'is_doctor': False}

        self.post(signup_cred, 'rest_register')
        email = EmailAddress.objects.get(email='test@gmail.com')
        email.verified = '1'
        email.save()

    def test_reset_password(self):
        response = self.post(self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_with_invalid_email(self):
        cred = self.credentials.copy()
        cred['email'] = 'test.com'
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_with_empty_email(self):
        cred = self.credentials.copy()
        cred['email'] = ''
        response = self.post(cred)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PatientFunctionalTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sign_up_cred = {'email': 'test@gmail.com',
                            'password1': 'testpass',
                            'password2': 'testpass',
                            'is_doctor': False}

        cls.login_cred = {'email': 'test@gmail.com', 'password': 'testpass'}

        cls.edit_data = {'pk': None, # assign in login
                         'first_name': 'first',
                         'last_name': 'last',
                         'gender': 1,
                         'profile_picture': cls.get_temporary_image(),
                         'height': 50,
                         'weight': 50.5,
                         'medical_record': 'mmeeddiiccaall rreeccoorrdd'}

        cls.preview_data = {'pk': None} # assign in login

    @classmethod
    def get_temporary_image(cls):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def post(self, data, url):
        return self.client.post(reverse(url), data)

    def put(self, data, url='rest_profile_edit'):
        return self.client.put(reverse(url), data, format='multipart')

    def get(self, data, url='rest_profile_preview'):
        return self.client.get(reverse(url), {'user_id': data['pk']})

    def sign_up(self):
        response = self.post(self.sign_up_cred, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login(self):
        response = self.post(self.login_cred, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])
        self.edit_data['pk'] = response.data['user']['pk']
        self.preview_data['pk'] = response.data['user']['pk']

    def verify_email(self):
        email = EmailAddress.objects.get(email='test@gmail.com')
        email.verified = '1'
        email.save()

        email = EmailAddress.objects.get(email='test@gmail.com')
        self.assertEqual(email.verified, True)

    def preview_profile(self):
        response = self.get(self.preview_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def edit_profile(self):
        response = self.put(self.edit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_functional(self):
        self.sign_up()
        self.verify_email()
        self.login()
        self.preview_profile()
        self.edit_profile()


class DoctorFunctionalTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sign_up_cred = {'email': 'test@gmail.com',
                            'password1': 'testpass',
                            'password2': 'testpass',
                            'is_doctor': True}

        cls.login_cred = {'email': 'test@gmail.com', 'password': 'testpass'}

        cls.edit_data = {'pk': None, # assign in setUp
                         'first_name': 'first',
                         'last_name': 'last',
                         'gender': 1,
                         'profile_picture': cls.get_temporary_image(),
                         'degree': 3,
                         'degree_picture': cls.get_temporary_image(),
                         'cv': 'ddooccttoorr ccvv',
                         'location': 'Tehran',}

        cls.preview_data = {'pk': None} # assign in login

    @classmethod
    def get_temporary_image(cls):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def post(self, data, url):
        return self.client.post(reverse(url), data)

    def put(self, data, url='rest_profile_edit'):
        return self.client.put(reverse(url), data, format='multipart')

    def get(self, data, url='rest_profile_preview'):
        return self.client.get(reverse(url), {'user_id': data['pk']})

    def sign_up(self):
        response = self.post(self.sign_up_cred, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login(self):
        response = self.post(self.login_cred, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])
        self.edit_data['pk'] = response.data['user']['pk']
        self.preview_data['pk'] = response.data['user']['pk']

    def verify_email(self):
        email = EmailAddress.objects.get(email='test@gmail.com')
        email.verified = '1'
        email.save()

        email = EmailAddress.objects.get(email='test@gmail.com')
        self.assertEqual(email.verified, True)

    def preview_profile(self):
        response = self.get(self.preview_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def edit_profile(self):
        response = self.put(self.edit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_functional(self):
        self.sign_up()
        self.verify_email()
        self.login()
        self.preview_profile()
        self.edit_profile()
