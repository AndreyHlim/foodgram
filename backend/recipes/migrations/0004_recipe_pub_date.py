# Generated by Django 3.2.16 on 2024-02-27 18:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20240224_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата публикации рецепта'),
            preserve_default=False,
        ),
    ]
