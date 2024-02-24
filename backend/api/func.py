from recipes.models import AmountIngredients


def recipe_ingredients_set(recipe, ingredients):
    objs = []

    for ingredient, amount in ingredients.values():
        objs.append(
            AmountIngredients(
                recipe=recipe, ingredient=ingredient, amount=amount
            )
        )

    AmountIngredients.objects.bulk_create(objs)


def obj_in_table(self, object, model):
    """
    Определяет, есть ли запрашиваемый рецепт (object) в:
    - избранных рецептах, если в качестве model передали модель Favourite,
    - списке рецептов к покупке, если в качестве model передали ShoppingCart.
    """

    user = self.context.get('request').user
    if not user.id:
        # запрос от анонимного пользователя
        return False
    recipe = model.objects.filter(
        user=user,
        recipe=object,
    )
    return recipe.exists()
