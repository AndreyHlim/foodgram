from django.contrib import admin
from api.models import (
    Profile, Ingredient, Tag, Recipe, Follow, Favourite,
    ShoppingCart, AmountIngredients
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingAdmin(admin.ModelAdmin):
    pass


@admin.register(AmountIngredients)
class AmountAdmin(admin.ModelAdmin):
    pass
