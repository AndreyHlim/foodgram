from django.contrib import admin
from recipes.models import Favourite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Follow, Profile


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


# @admin.register(AmountIngredients)
# class AmountAdmin(admin.ModelAdmin):
#     pass
