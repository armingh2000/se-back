from rest_framework.test import APIClient, APITestCase
from users.models import User
from rest_framework import status
from django.urls import reverse
from allauth.account.models import EmailAddress
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO


# Create your tests here.

class PatientEditProfileTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.signup_credentials = {'email': 'patient@gmail.com',
                                  'password1': 'test',
                                  'password2': 'test',
                                  'is_doctor': False}

        cls.login_credentials = {'email': 'patient@gmail.com',
                                 'password': 'test'}

        cls.edit_data = {'pk': None, # assign in setUp
                         'first_name': 'first',
                         'last_name': 'last',
                         'gender': 1,
                         'profile_picture': cls.get_temporary_image(),
                         'height': 50,
                         'weight': 50.5,
                         'medical_record': 'mmeeddiiccaall rreeccoorrdd'}

    def put(self, data, url='rest_edit'):
        return self.client.put(reverse(url), data, format='multipart')

    def post(self, data, url):
        return self.client.post(reverse(url), data)

    @classmethod
    def get_temporary_image(cls):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self):
        response = self.post(self.signup_credentials, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        email = EmailAddress.objects.get(email='patient@gmail.com')
        email.verified = '1'
        email.save()
        response = self.post(self.login_credentials, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])
        self.edit_data['pk'] = response.data['user']['pk']

    def test_edit_profile_patient(self):
        response = self.put(self.edit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_edit_profile_with_unauthorized_pk(self):
        data = self.edit_data.copy()
        data['pk'] = self.edit_data['pk'] + 1
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_edit_profile_with_invalid_gender(self):
        data = self.edit_data.copy()
        data['gender'] = 2
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_edit_profile_with_invalid_profile_picture(self):
        data = self.edit_data.copy()
        data['profile_picture'] = 'string' # must be file
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_edit_profile_with_invalid_height(self):
        data = self.edit_data.copy()
        data['height'] = -10
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_edit_profile_with_invalid_weight(self):
        data = self.edit_data.copy()
        data['weight'] = -10
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_edit_profile_with_invalid_medical_record(self):
        data = self.edit_data.copy()
        data['medical_record'] = self.get_temporary_image() # must be text
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DoctorEditProfileTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.signup_credentials = {'email': 'doctor@gmail.com',
                                  'password1': 'test',
                                  'password2': 'test',
                                  'is_doctor': True}

        cls.login_credentials = {'email': 'doctor@gmail.com',
                                 'password': 'test'}

        cls.edit_data = {'pk': None, # assign in setUp
                         'first_name': 'first',
                         'last_name': 'last',
                         'gender': 1,
                         'profile_picture': cls.get_temporary_image(),
                         'degree': 3,
                         'degree_picture': cls.get_temporary_image(),
                         'cv': 'ddooccttoorr ccvv',
                         'location': 'Tehran',}

    def put(self, data, url='rest_edit'):
        return self.client.put(reverse(url), data, format='multipart')

    def post(self, data, url):
        return self.client.post(reverse(url), data)

    @classmethod
    def get_temporary_image(cls):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self):
        self.post(self.signup_credentials, 'rest_register')
        email = EmailAddress.objects.get(email='doctor@gmail.com')
        email.verified = '1'
        email.save()
        response = self.post(self.login_credentials, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])
        self.edit_data['pk'] = response.data['user']['pk']

    def test_edit_profile_doctor(self):
        response = self.put(self.edit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_edit_profile_with_unauthorized_pk(self):
        data = self.edit_data.copy()
        data['pk'] = self.edit_data['pk'] + 1
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_doctor_edit_profile_with_invalid_gender(self):
        data = self.edit_data.copy()
        data['gender'] = 2
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doctor_edit_profile_with_invalid_profile_picture(self):
        data = self.edit_data.copy()
        data['profile_picture'] = 'string' # must be file
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doctor_edit_profile_with_invalid_degree(self):
        data = self.edit_data.copy()
        data['degree'] = -1
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doctor_edit_profile_with_invalid_degree_picture(self):
        data = self.edit_data.copy()
        data['degree_picture'] = 'string' # must be file
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doctor_edit_profile_with_invalid_cv(self):
        data = self.edit_data.copy()
        data['cv'] = self.get_temporary_image()
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doctor_edit_profile_with_invalid_location(self):
        data = self.edit_data.copy()
        data['location'] = self.get_temporary_image()
        response = self.put(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
