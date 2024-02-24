from django.contrib import admin
from api.models import (
    Ingredient, Tag
)
from users.models import Profile, Follow
from recipes.models import Recipe, Favourite, ShoppingCart, AmountIngredients


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
