from rest_framework.test import APITestCase
from .models import User, Patient, Doctor
from PIL import Image
from io import BytesIO


# Create your tests here.


class UserModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@gmail.com',
                            password='testpass',
                            first_name='first',
                            last_name='last',
                            gender=0)

    def test_user_model(self):
        user = User.objects.get(email='test@gmail.com')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(user.password, 'testpass')
        self.assertEqual(user.first_name, 'first')
        self.assertEqual(user.last_name, 'last')
        self.assertEqual(user.gender, 0)


class PatientModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@gmail.com', password='testpass')
        cls.user = User.objects.get(email='test@gmail.com')
        Patient.objects.create(user=cls.user,
                               medical_record='mmeeddiiccaall rreeccoorrdd',
                               height=50,
                               weight=50.5)

    def test_patient_model(self):
        patient = Patient.objects.get(user=self.user)
        self.assertEqual(patient.medical_record, 'mmeeddiiccaall rreeccoorrdd')
        self.assertEqual(patient.height, 50)
        self.assertEqual(patient.weight, 50.5)


class DoctorModelTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@gmail.com', password='testpass')
        cls.user = User.objects.get(email='test@gmail.com')
        Doctor.objects.create(user=cls.user,
                              cv='cccvvv',
                              location='tehran'
                              )

    def test_doctor_model(self):
        doctor = Doctor.objects.get(user=self.user)
        self.assertEqual(doctor.cv, 'cccvvv')
        self.assertEqual(doctor.location, 'tehran')
