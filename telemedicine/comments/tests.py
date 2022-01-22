from rest_framework.test import APITestCase
from .models import Comment
from users.models import User, Doctor, Patient
from django.urls import reverse
from rest_framework import status
from allauth.account.models import EmailAddress

# Create your tests here.


class CommentListTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='doctor@gmail.com', password='doctor')
        cls.doctor_user = User.objects.get(email='doctor@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              cv='cccvvv',
                              location='tehran'
                              )
        cls.doctor = Doctor.objects.get(user=cls.doctor_user)

        User.objects.create(email='patient@gmail.com', password='patient')
        cls.patient_user = User.objects.get(email='patient@gmail.com')
        Patient.objects.create(user=cls.patient_user,
                               medical_record='mmeeddiiccaall rreeccoorrdd',
                               height=50,
                               weight=50.5)
        cls.patient = Patient.objects.get(user=cls.patient_user)

        Comment.objects.create(doctor=cls.doctor, patient=cls.patient, body='ccoommeenntt')

        cls.get_data = {"doctor_pk": cls.doctor.user.pk}

    def get(self, data, url='rest_comment_list'):
        return self.client.get(reverse(url), data)

    def test_comment_list(self):
        response = self.get(self.get_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_list_with_invalid_pk(self):
        get_data = self.get_data.copy()
        get_data['doctor_pk'] += 1
        response = self.get(get_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='doctor@gmail.com', password='doctor')
        cls.doctor_user = User.objects.get(email='doctor@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              cv='cccvvv',
                              location='tehran'
                              )
        cls.doctor = Doctor.objects.get(user=cls.doctor_user)

        User.objects.create(email='patient@gmail.com', password='patient')
        cls.patient_user = User.objects.get(email='patient@gmail.com')
        Patient.objects.create(user=cls.patient_user,
                               medical_record='mmeeddiiccaall rreeccoorrdd',
                               height=50,
                               weight=50.5)
        cls.patient = Patient.objects.get(user=cls.patient_user)

        Comment.objects.create(doctor=cls.doctor, patient=cls.patient, body='ccoommeenntt')

    def test_comment_model(self):
        comment = Comment.objects.get(doctor=self.doctor, patient=self.patient)
        self.assertEqual(comment.doctor, self.doctor)
        self.assertEqual(comment.patient, self.patient)
        self.assertEqual(comment.body, 'ccoommeenntt')
        self.assertNotEqual(comment.created_on, None)


class CreateCommentTests(APITestCase):
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

        cls.create_data = {"doctor_pk": cls.doctor_user.pk, "body": "ccoommeenntt"}

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

    def put(self, data, url='rest_create_comment'):
        return self.client.put(reverse(url), data)

    def test_create_comment(self):
        response = self.put(self.create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_with_invalid_pk(self):
        create_data = self.create_data.copy()
        create_data['doctor_pk'] -= 1
        response = self.put(create_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment_with_same_account(self):
        create_data = self.create_data.copy()
        create_data['doctor_pk'] += 1
        response = self.put(create_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


