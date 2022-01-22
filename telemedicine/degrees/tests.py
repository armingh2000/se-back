from rest_framework.test import APITestCase
from users.models import User, Doctor
from django.urls import reverse
from rest_framework import status
from degrees.models import Degree
from PIL import Image
from io import BytesIO
from allauth.account.models import EmailAddress


# Create your tests here.

class DegreeModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@gmail.com')
        user = User.objects.get(email='test@gmail.com')
        Doctor.objects.create(user=user,
                              cv='cv',
                              location='tehran')
        cls.doctor = Doctor.objects.get(user=user)
        Degree.objects.create(doctor=cls.doctor, name='deg')

    def test_degree_model(self):
        degree = Degree.objects.get(doctor=self.doctor)
        self.assertEqual(degree.name, 'deg')
        self.assertEqual(degree.doctor, self.doctor)


class AddDegreeTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.signup_cred = {'email': 'doctor@gmail.com',
                            'password1': 'doctor',
                            'password2': 'doctor',
                            'is_doctor': True}

        cls.login_cred = {'email': 'doctor@gmail.com', 'password': 'doctor'}

        cls.add_degree_data = {'name': 'deg', 'picture': cls.get_temporary_image()}

    @classmethod
    def get_temporary_image(cls):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self):
        response = self.post(self.signup_cred, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        email = EmailAddress.objects.get(email='doctor@gmail.com')
        email.verified = '1'
        email.save()
        response = self.post(self.login_cred, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])

    def post(self, data, url):
        return self.client.post(reverse(url), data)

    def put(self, data, url='rest_add_degree'):
        return self.client.put(reverse(url), data, format='multipart')

    def test_add_degree(self):
        response = self.put(self.add_degree_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_degree_with_empty_name(self):
        add_degree_data = self.add_degree_data.copy()
        add_degree_data['name'] = ''
        response = self.put(add_degree_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_degree_with_empty_picture(self):
        add_degree_data = self.add_degree_data.copy()
        add_degree_data['picture'] = ''
        response = self.put(add_degree_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_degree_with_invalid_picture(self):
        add_degree_data = self.add_degree_data.copy()
        add_degree_data['picture'] = 'picture' # must be image
        response = self.put(add_degree_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class EditDegreeTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.signup_cred = {'email': 'doctor1@gmail.com',
                            'password1': 'doctor1',
                            'password2': 'doctor1',
                            'is_doctor': True}

        cls.login_cred = {'email': 'doctor1@gmail.com', 'password': 'doctor1'}

        User.objects.create(email='doctor1@gmail.com', password='doctor1', first_name="first1", last_name="last1")
        doctor_user = User.objects.get(email='doctor1@gmail.com')
        Doctor.objects.create(user=doctor_user,
                              cv='cccvvv',
                              location='tehran')
        doctor = Doctor.objects.get(user=doctor_user)
        Degree.objects.create(doctor=doctor, name='deg')

        cls.signup_cred = {'email': 'doctor2@gmail.com',
                            'password1': 'doctor2',
                            'password2': 'doctor2',
                            'is_doctor': True}

        cls.login_cred = {'email': 'doctor2@gmail.com', 'password': 'doctor2'}
        cls.add_degree_data = {'name': 'deg', 'picture': cls.get_temporary_image()}
        cls.edit_degree_data = {'degree_pk': 2,
                                'name': 'deg',
                                'picture': cls.get_temporary_image()}
        cls.delete_degree_data = {'degree_pk': 2}

    @classmethod
    def get_temporary_image(cls):
        file = BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'temp.png'
        file.seek(0)
        return file

    def setUp(self):
        response = self.post(self.signup_cred, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        email = EmailAddress.objects.get(email='doctor2@gmail.com')
        email.verified = '1'
        email.save()
        response = self.post(self.login_cred, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])
        response = self.put(self.add_degree_data, url='rest_add_degree')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post(self, data, url):
        return self.client.post(reverse(url), data)

    def delete(self, data, url='rest_edit_degree'):
        return self.client.delete(reverse(url), data)

    def put(self, data, url='rest_edit_degree'):
        return self.client.put(reverse(url), data, format='multipart')

    def test_edit_degree(self):
        response = self.put(self.edit_degree_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_degree(self):
        response = self.delete(self.delete_degree_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_degree_for_another_doctor(self):
        edit_degree_data = self.edit_degree_data.copy()
        edit_degree_data['degree_pk'] = 1
        response = self.put(edit_degree_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_degree_for_another_doctor(self):
        delete_degree_data = self.delete_degree_data.copy()
        delete_degree_data['degree_pk'] = 1
        response = self.delete(delete_degree_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_degree_with_empty_name(self):
        edit_degree_data = self.edit_degree_data.copy()
        edit_degree_data['name'] = ''
        response = self.put(edit_degree_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_degree_with_empty_picture(self):
        edit_degree_data = self.edit_degree_data.copy()
        edit_degree_data['picture'] = ''
        response = self.put(edit_degree_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


