from rest_framework import serializers
from core.models import Recipe




class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    class Meta:
        model = Recipe
        fields = ["id","title","time_minutes","price","link"]
        read_only_fieds = ["id"]

class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""

    class Meta(RecipeSerializer.Meta):
        fieds = RecipeSerializer.Meta.fields + ["description"]