from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls  import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer,RecipeDetailSerializer


RECIPES_URL = reverse("recipe:recipe-list")


def create_recipe(user,**params):

    defaults ={
        "title":"Sample recipe title",
        "time_minutes":"22",
        "price":Decimal('4.00'),
        "description":"Sample description",
        "link":"http://example.com"
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user,**defaults)
    return recipe

def detail_url(recipe_id):
    """Create and return recipe detail url"""
    return reverse("recipe:recipe-detail",args=[recipe_id])


class PublicRecipeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123"
        )

        self.client.force_authenticate(user=self.user)

    def test_retrive_recipes(self):
        create_recipe(user = self.user)
        create_recipe(user = self.user)

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes,many=True)
        self.assertEqual(res.data,serializer.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_recipes_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other@example.com',
            'password123'
            )
        create_recipe(user=user2)
        create_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_get_recipe_detail(self):
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data,serializer.data)


    def test_create_recipe(self):
        """Test create recipe"""

        payload={
            "user":self.user,
            "title":"Sample Recipe",
            "time_minutes":30,
            "price":Decimal("5.99")
            }

        res = self.client.post(RECIPES_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        for k ,v in payload.items():

            self.assertEqual(getattr(recipe,k),v)
        self.assertEqual(recipe.user,self.user)





