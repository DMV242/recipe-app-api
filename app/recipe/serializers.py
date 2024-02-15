from rest_framework import serializers
from core.models import Recipe,Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields= ["id","name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""

    tags = TagSerializer(many=True,required=False)
    class Meta:
        model = Recipe
        fields = ["id","title","time_minutes","price","link","tags"]
        read_only_fieds = ["id"]

    def _get_or_create_tags(self,tags,recipe):
        auth_user = self.context["request"].user
        for tag_name in tags:
            tag_obj , created = Tag.objects.get_or_create(user=auth_user, **tag_name)
            recipe.tags.add(tag_obj)
        return recipe

    def create(self, validated_data):
        """Create tag"""
        tags = validated_data.pop("tags",[])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags,recipe)

        return recipe





    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance




class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""

    class Meta(RecipeSerializer.Meta):
        fieds = RecipeSerializer.Meta.fields + ["description"]



