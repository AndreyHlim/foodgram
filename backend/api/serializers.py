import base64

from api.func import obj_in_table, recipe_ingredients_set
from foodgram.validators import ingredients_validator, tags_validator
from recipes.models import Favourite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from users.models import Follow

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import F

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'Ингредиенты'.
    Используется для отображения списка ингредиентов.
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'Тег'.
    Используется для отображения списка тегов.
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользовательской модели User.
    Используется для отображение пользовател(я/ей),
    а также библиотекой Djoser через настройки SETTINGS.DJOSER.
    """

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, user):
        """Узнаёт подписан ли запрашиваемый пользователь на запрашивающего"""

        request = self.context.get('request')
        return request is not None and Follow.objects.filter(
            user_id=request.user.id, following=user
        ).exists()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта/рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = ProfileSerializer(many=False, read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, recipe):
        return recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe__amount'),
        )

    def get_is_favorited(self, recipe):
        """Определяет находится ли рецепт в избранном."""

        return obj_in_table(
            user=self.context.get('request').user,
            object=recipe,
            model=Favourite
        )

    def get_is_in_shopping_cart(self, recipe):
        """Определяет, есть ли рецепт в избранных рецептах пользователя."""

        return obj_in_table(
            user=self.context.get('request').user,
            object=recipe,
            model=ShoppingCart
        )

    def validate(self, data):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        image = self.initial_data.get('image')

        if not (tags and ingredients and image):
            raise ValidationError('Мало данных для создания рецепта.')

        tags_validator(tags, Tag)

        ingredients = ingredients_validator(ingredients, Ingredient)

        data.update(
            {
                'tags': tags,
                'ingredients': ingredients,
                'author': self.context.get('request').user,
            }
        )
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe_ingredients_set(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)

        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        recipe_ingredients_set(instance, ingredients)

        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)

        instance.save()
        return instance


class RecipeLittleSerializer(serializers.ModelSerializer):
    """Короткий сериализатор для отображения рецепта/рецептов."""

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, user):
        follow = Follow.objects.filter(user_id=user.id)
        return follow.exists()

    def get_recipes_count(self, user):
        return len(Recipe.objects.filter(author=user.id))

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeLittleSerializer(recipes, many=True, read_only=True)
        return serializer.data


# Оптимизировать запросы к БД
