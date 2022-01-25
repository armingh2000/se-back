from rest_framework.test import APITestCase
from users.models import User, Doctor, Patient
from django.urls import reverse
from rest_framework import status
from .models import Rate
from allauth.account.models import EmailAddress


# Create your tests here.

class RateModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@gmail.com')
        user = User.objects.get(email='test@gmail.com')
        doctor = Doctor.objects.create(user=user)
        patient = Patient.objects.create(user=user)
        Rate.objects.create(rate=5, doctor=doctor, patient=patient)

    def test_degree_model(self):
        rate = Rate.objects.get(rate=5)
        self.assertEqual(rate.rate, 5)


class RateAddTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.patient_signup_credentials = {'email': 'patient@gmail.com',
                                          'password1': 'test',
                                          'password2': 'test',
                                          'is_doctor': False}

        cls.patient_login_credentials = {'email': 'patient@gmail.com',
                                         'password': 'test'}

        User.objects.create(email='doctor@gmail.com', password='doctor')
        cls.doctor_user = User.objects.get(email='doctor@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              cv='cccvvv',
                              location='tehran'
                              )

        cls.rate_data = {"doctor_pk": cls.doctor_user.pk, "rate": 5}

    def setUp(self):
        response = self.post(self.patient_signup_credentials, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        email = EmailAddress.objects.get(email='patient@gmail.com')
        email.verified = '1'
        email.save()
        response = self.post(self.patient_login_credentials, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])

    def post(self, data, url):
        return self.client.post(reverse(url), data)

    def put(self, data, url='rest_add_rate'):
        return self.client.put(reverse(url), data)

    def test_add_rate(self):
        response = self.put(self.rate_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_rate_with_invalid_doctor_pk(self):
        rate_data = self.rate_data.copy()
        rate_data['doctor_pk'] = '23a'
        response = self.put(rate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rate_with_unavailable_doctor_pk(self):
        rate_data = self.rate_data.copy()
        rate_data['doctor_pk'] = 23
        response = self.put(rate_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_rate_with_empty_rate(self):
        rate_data = self.rate_data.copy()
        rate_data['rate'] = ''
        response = self.put(rate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rate_with_invalid_rate(self):
        rate_data = self.rate_data.copy()
        rate_data['rate'] = 10
        response = self.put(rate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rate_with_string_rate(self):
        rate_data = self.rate_data.copy()
        rate_data['rate'] = 'twelve'
        response = self.put(rate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rate_double(self):
        response = self.put(self.rate_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.put(self.rate_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)



class RateEditTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.patient_signup_credentials = {'email': 'patient@gmail.com',
                                          'password1': 'test',
                                          'password2': 'test',
                                          'is_doctor': False}

        cls.patient_login_credentials = {'email': 'patient@gmail.com',
                                         'password': 'test'}

        User.objects.create(email='doctor@gmail.com', password='doctor')
        cls.doctor_user = User.objects.get(email='doctor@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              cv='cccvvv',
                              location='tehran'
                              )

        User.objects.create(email='test@gmail.com', is_doctor=False)
        user = User.objects.get(email='test@gmail.com')
        Patient.objects.create(user=user)
        patient = Patient.objects.get(user=user)
        doctor = Doctor.objects.get(user=cls.doctor_user)
        Rate.objects.create(rate=4, patient=patient, doctor=doctor)

        cls.add_rate_data = {"doctor_pk": cls.doctor_user.pk, "rate": 5}
        cls.edit_rate_data = {"rate_pk": 2, "rate": 2}

    def setUp(self):
        response = self.post(self.patient_signup_credentials, 'rest_register')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        email = EmailAddress.objects.get(email='patient@gmail.com')
        email.verified = '1'
        email.save()
        response = self.post(self.patient_login_credentials, 'rest_login')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access_token'])

        response = self.put(self.add_rate_data, url='rest_add_rate')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post(self, data, url):
        return self.client.post(reverse(url), data)

    def put(self, data, url='rest_edit_rate'):
        return self.client.put(reverse(url), data)

    def test_edit_rate(self):
        response = self.put(self.edit_rate_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_rate_with_strig_rate_pk(self):
        edit_rate_data = self.edit_rate_data.copy()
        edit_rate_data['rate_pk'] = '2s'
        response = self.put(edit_rate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_rate_with_invalid_rate_pk(self):
        edit_rate_data = self.edit_rate_data.copy()
        edit_rate_data['rate_pk'] = 3
        response = self.put(edit_rate_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_rate_with_invalid_rate(self):
        edit_rate_data = self.edit_rate_data.copy()
        edit_rate_data['rate'] = 10
        response = self.put(edit_rate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_rate_with_string_rate(self):
        edit_rate_data = self.edit_rate_data.copy()
        edit_rate_data['rate'] = 'one'
        response = self.put(edit_rate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_rate_with_empty_rate(self):
        edit_rate_data = self.edit_rate_data.copy()
        edit_rate_data['rate_pk'] = ''
        response = self.put(edit_rate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_rate_for_another_patient(self):
        edit_rate_data = self.edit_rate_data.copy()
        edit_rate_data['rate_pk'] = 1
        response = self.put(edit_rate_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
