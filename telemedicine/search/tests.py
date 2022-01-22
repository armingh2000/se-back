from rest_framework.test import APITestCase
from users.models import User, Doctor
from django.urls import reverse
from rest_framework import status
from degrees.models import Degree
from PIL import Image
from io import BytesIO


# Create your tests here.


class SearchTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='doctor1@gmail.com', password='doctor', first_name="first1", last_name="last1")
        cls.doctor_user = User.objects.get(email='doctor1@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              cv='cccvvv',
                              location='tehran'
                              )
        cls.doctor = Doctor.objects.get(user=cls.doctor_user)
        Degree.objects.create(doctor=cls.doctor, name='esp1')
        Degree.objects.create(doctor=cls.doctor, name='esp2')


        User.objects.create(email='doctor2@gmail.com', password='doctor', first_name="first2", last_name="last2")
        cls.doctor_user = User.objects.get(email='doctor2@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              cv='cccvvv',
                              location='tehran'
                              )
        cls.doctor = Doctor.objects.get(user=cls.doctor_user)

        Degree.objects.create(doctor=cls.doctor, name='esp1')
        Degree.objects.create(doctor=cls.doctor, name='esp3')

        cls.search_data = {"query": None}

    def get(self, data, url='rest_search'):
        return self.client.get(reverse(url), data)

    def test_search_with_one_result(self):
        search_data = self.search_data.copy()
        search_data['query'] = 'esp3'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_with_multiple_results(self):
        search_data = self.search_data.copy()
        search_data['query'] = 'esp1'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_with_no_result(self):
        search_data = self.search_data.copy()
        search_data['query'] = 'esp0'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_with_first_name(self):
        search_data = self.search_data.copy()
        search_data['query'] = 'first1'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_with_last_name(self):
        search_data = self.search_data.copy()
        search_data['query'] = 'last2'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
