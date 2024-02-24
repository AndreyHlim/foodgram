from django.core.exceptions import ValidationError
import re


def validate_username(instance):
    name_template = r'^[\w.@+-]+\Z'
    if re.fullmatch(name_template, instance) is None:
        raise ValidationError(
            'Введите корректное значение username. '
            'Должно соответствовать регулярному выражению "^[\\w.@+-]+\\Z"'
        )


def tags_validator(tags_check, model):
    tags = model.objects.filter(id__in=tags_check)
    if len(set(tags_check)) != len(tags_check):
        raise ValidationError('Указан повторяющийся тэг')
    if len(tags) != len(tags_check):
        raise ValidationError('Указан несуществующий тэг')


def ingredients_validator(ingredients, model):
    if not ingredients:
        raise ValidationError('Не указаны ингридиенты')

    valid_ings = {}

    for ing in ingredients:
        if not (isinstance(ing['amount'], int) or ing['amount'].isdigit()):
            raise ValidationError('Неправильное количество ингидиента')

        if int(ing['id']) in valid_ings.keys():
            raise ValidationError('В рецепте есть повторяющиеся ингридиенты')

        valid_ings[ing['id']] = int(ing['amount'])
        if valid_ings[ing['id']] <= 0:
            raise ValidationError('Неправильное количество ингридиента')

    if not valid_ings:
        raise ValidationError('Неправильные ингидиенты')

    db_ings = model.objects.filter(pk__in=valid_ings.keys())
    if not db_ings:
        raise ValidationError('Неправильные ингидиенты')

    for ing in db_ings:
        valid_ings[ing.pk] = (ing, valid_ings[ing.pk])

    return valid_ings
