from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")

def create_user(**params):
    return get_user_model().objects.create_user(**params)



class PublicApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()


    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            "email":"test@example.com",
            "password":"testpass123",
            "name":"Test Name"
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password",res.data)


    def test_user_exists(self):
        "Test error returned if user with email exists"
        payload = {
            "email":"test@example.com",
            "password":"testpass123",
            "name":"Test Name"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
            "email":"test@example.com",
            "password":"pw",
            "name":"Test Name"
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

        user_exixts = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()

        self.assertFalse(user_exixts)

    def create_token_for_user(self):
        """Create a token for the user"""
        user_details = {
            "email":"test@example.com",
            "password":"pw",
            "name":"Test Name"
        }

        create_user(**user_details)

        payload = {
            "emai":user_details.get("email"),
            "password":user_details.get("password")
        }

        res = self.client.post(TOKEN_URL,payload)

        self.assertIn("token",res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        create_user(email="test@londonappdev.com", password="test")
        payload = {"email":"dav@gmail.com","password":"badpass"}

        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn("token",res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):

        payload = {"email":"dav@gmail.com","password":""}

        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn("token",res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)