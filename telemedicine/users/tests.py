from django.test import TestCase
from .models import User

# Create your tests here.

class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email='test@gmail.com', password='testpass')

    def test_user_info(self):
        user = User.objects.get(email='test@gmail.com')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(user.password, 'testpass')
