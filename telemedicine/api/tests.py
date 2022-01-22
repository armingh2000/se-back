from rest_framework.test import APITestCase
from users.models import User, Doctor, Patient
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

        cls.edit_data = {'first_name': 'first',
                         'last_name': 'last',
                         'gender': 1,
                         'profile_picture': cls.get_temporary_image(),
                         'height': 50,
                         'weight': 50.5,
                         'medical_record': 'mmeeddiiccaall rreeccoorrdd',
                         'type': 0}

        cls.preview_data = {'user_pk': None, 'type': 0} # assign in login

        User.objects.create(email='doctor@gmail.com', password='doctor', first_name='first', last_name='last')
        cls.doctor_user = User.objects.get(email='doctor@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              cv='cccvvv',
                              location='tehran'
                              )

        cls.create_comment_data = {"doctor_pk": cls.doctor_user.pk, "body": "ccoommeenntt"}
        cls.get_comment_list_data = {"doctor_pk": cls.doctor_user.pk}

        cls.search_data = {"query": "first"}

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
        return self.client.get(reverse(url), data)

    def sign_up(self):
        response = self.post(self.sign_up_cred, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login(self):
        response = self.post(self.login_cred, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])
        self.preview_data['user_pk'] = response.data['user']['pk']

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

    def search(self):
        response = self.get(self.search_data, url='rest_search')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def create_comment(self):
        response = self.put(self.create_comment_data, url='rest_create_comment')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_comment_list(self):
        response = self.get(self.get_comment_list_data, url='rest_comment_list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_functional(self):
        self.sign_up()
        self.verify_email()
        self.login()
        self.preview_profile()
        self.edit_profile()
        self.search()
        self.create_comment()
        self.get_comment_list()


class DoctorFunctionalTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sign_up_cred = {'email': 'test@gmail.com',
                            'password1': 'testpass',
                            'password2': 'testpass',
                            'is_doctor': True}

        cls.login_cred = {'email': 'test@gmail.com', 'password': 'testpass'}

        cls.edit_data = {'first_name': 'first',
                         'last_name': 'last',
                         'gender': 1,
                         'profile_picture': cls.get_temporary_image(),
                         'cv': 'ddooccttoorr ccvv',
                         'location': 'tehran',
                         'type': 1}

        cls.preview_data = {'user_pk': None, 'type': 1} # assign in login

        cls.create_type_data = {'type': 0}

        cls.add_degree_data = {'name': 'deg', 'picture': cls.get_temporary_image()}
        cls.edit_degree_data = {'degree_pk': 1, 'name': 'deg2', 'picture': cls.get_temporary_image()}
        cls.delete_degree_data = {'degree_pk': 1}

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
        return self.client.get(reverse(url), data)

    def delete(self, data, url):
        return self.client.delete(reverse(url), data)

    def sign_up(self):
        response = self.post(self.sign_up_cred, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login(self):
        response = self.post(self.login_cred, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])
        self.preview_data['user_pk'] = response.data['user']['pk']

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

    def create_user_type(self):
        response = self.post(self.create_type_data, url='rest_create_user_type')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def add_degree(self):
        response = self.put(self.add_degree_data, url='rest_add_degree')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def edit_degree(self):
        response = self.put(self.edit_degree_data, url='rest_edit_degree')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_degree(self):
        response = self.delete(self.delete_degree_data, url='rest_edit_degree')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_functional(self):
        self.sign_up()
        self.verify_email()
        self.login()
        self.preview_profile()
        self.edit_profile()
        self.add_degree()
        self.edit_degree()
        self.delete_degree()
