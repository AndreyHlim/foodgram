import csv

from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.import_ingredients()
        print('Загрузка тегов завершена.')

    def import_ingredients(self, file='tags.csv'):
        print(f'Загрузка {file}...')
        with open(file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                status, created = Tag.objects.update_or_create(
                    name=row[0],
                    color=row[1],
                    slug=row[2],
                )
