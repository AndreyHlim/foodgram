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
