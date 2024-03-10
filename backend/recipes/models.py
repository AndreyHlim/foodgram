import foodgram.constants as var
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from colorfield.fields import ColorField

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=var.INGREDIENT_MAX_NAME,
        unique=True,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=var.INGREDIENT_MAX_NAME_UNIT,
        verbose_name='Единыцы измерений',
    )

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=var.TAG_MAX_NAME,
        unique=True,
        verbose_name='Название',
    )
    color = ColorField(
        format='hex',
        null=True,
        blank=True,
        verbose_name='Цвет',
    )
    slug = models.SlugField(
        max_length=var.TAG_MAX_LEN_SLUG_NAME,
        unique=True,
        verbose_name='URL тега',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='AmountIngredients',
        verbose_name='Ингредиенты для приготовления',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег(-и)',
        related_name='recipes',
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to='recipes/images/',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=var.RECIPE_MAX_NAME,
    )
    text = models.CharField(
        verbose_name='Описание рецепта',
        max_length=var.RECIPE_MAX_TEXT,
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(var.RECIPE_MIN_TIME,),
        )
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
    )
    pub_date = models.DateTimeField(
        'Дата публикации рецепта',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe'
            )
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        self.name = self.name.capitalize()
        return super().clean()

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

    def display_favourite(self):
        query = Favourite.objects.filter(recipe_id=self.pk)
        return query.count()
    display_favourite.short_description = 'Количество добавлений в избранное'

    def display_tags(self):
        return ', '.join([recipe.name for recipe in self.tags.all()])
    display_tags.short_description = 'Теги'


class AmountIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиенты'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(1,),
        )
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Количество ингредиентов в рецептах'

    def __str__(self):
        return (f'Рецепт "{self.recipe}"')

    def display_author(self):
        return self.recipe.author.get_username()
    display_author.short_description = 'Автор рецепта'


class Favourite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourites'
            )
        ]

    def __str__(self):
        return (f'Пользователь {self.user} добавил '
                f'рецепт "{self.recipe}" себе в избранное')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_add_recipes'
            )
        ]

    def __str__(self):
        return (f'Пользователь {self.user} планирует купить '
                f'ингредиенты рецепта: {self.recipe}')
