from django.contrib import admin
from recipes.models import (
    Favourite, Ingredient, Recipe, ShoppingCart, Tag, AmountIngredients
)
from users.models import Follow, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email')
    list_filter = list_display
    search_fields = ('first_name', 'email')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'display_tags', 'display_favourite')
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingAdmin(admin.ModelAdmin):
    pass


@admin.register(AmountIngredients)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'display_author',)
    list_filter = ('recipe',)
