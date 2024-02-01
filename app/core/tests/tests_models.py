from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user(email="user@example.com",password="testpass123"):
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):
    """Test models """

    def test_create_user_with_successful(self):
        email = "test@example.com"
        password = "testpass1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )


        self.assertEqual(user.email,email)

        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com',"test1@example.com"],
            ['test2@EXAMPLE.Com',"test2@example.com"],
        ]

        for email,excepted in sample_emails:
            user = get_user_model().objects.create_user(email,"sample123")
            self.assertEqual(user.email,excepted)


    def test_new_user_without_email_raises_error(self):
        with  self.assertRaises(ValueError):
            get_user_model().objects.create_user("","test123")


    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'admin@example.com',
            'admin123'
        )

        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password("admin123"))


    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
              email = "test@example.com",
                password = "testpass1234"
        )


        recipe = models.Recipe.objects.create(
            user = user,
            title="Sample Recipe",
            time_minutes=5,
            price=Decimal("9.00"),
            description = "Simple recipe"
        )

        self.assertEqual(str(recipe),recipe.title)


    def test_create_tag(self):
        user =create_user()
        tag = models.Tag.objects.create(user=user,name="Tag1")

        self.assertEqual(str(tag),tag.name)

