# from django.db import models
# from django.contrib.auth import get_user_model


# class Ingredient(models.Model):
#     name = models.CharField(max_length=200, unique=True)
#     measurement_unit = models.CharField(max_length=200)

#     class Meta:
#         verbose_name = 'ингридиент'
#         verbose_name_plural = 'Ингридиенты'

#     def __str__(self):
#         return self.name


# class Tag(models.Model):
#     name = models.CharField(
#         max_length=200,
#         unique=True,
#     )
#     color = models.CharField(
#         max_length=7,
#         null=True,
#         blank=True,
#     )
#     slug = models.SlugField(
#         max_length=200,
#         null=True,
#         blank=True,
#         unique=True,
#     )

#     class Meta:
#         verbose_name = 'тег'
#         verbose_name_plural = 'Теги'

#     def __str__(self) -> str:
#         return self.name


# User = get_user_model()
