from rest_framework.test import APITestCase
from users.models import User, Doctor
from django.urls import reverse
from rest_framework import status


# Create your tests here.


class SearchTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='doctor1@gmail.com', password='doctor', first_name="first1", last_name="last1")
        cls.doctor_user = User.objects.get(email='doctor1@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              degree='["esp1", "esp2"]',
                              cv='cccvvv',
                              location='tehran'
                              )

        User.objects.create(email='doctor2@gmail.com', password='doctor', first_name="first2", last_name="last2")
        cls.doctor_user = User.objects.get(email='doctor2@gmail.com')
        Doctor.objects.create(user=cls.doctor_user,
                              degree='["esp1", "esp3"]',
                              cv='cccvvv',
                              location='tehran'
                              )

        cls.search_data = {"search": None}

    def get(self, data, url='rest_search'):
        return self.client.get(reverse(url), data)

    def test_search_with_one_result(self):
        search_data = self.search_data.copy()
        search_data['search'] = 'esp3'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_with_multiple_results(self):
        search_data = self.search_data.copy()
        search_data['search'] = 'esp1'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_with_no_result(self):
        search_data = self.search_data.copy()
        search_data['search'] = 'esp0'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_with_no_result(self):
        search_data = self.search_data.copy()
        search_data['search'] = 'esp0'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_with_first_name(self):
        search_data = self.search_data.copy()
        search_data['search'] = 'first1'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_with_last_name(self):
        search_data = self.search_data.copy()
        search_data['search'] = 'last2'
        response = self.get(search_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
