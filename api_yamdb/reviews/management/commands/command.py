from django.core.management.base import BaseCommand
import csv

from reviews.models import Genre, Category, Title, GenreTitle


class Command(BaseCommand):
    help = 'Создает Genre из csv'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Путь к файлу')

    def handle(self, *args, **kwargs):
        name = kwargs['file']
        file = f'static/data/{name}.csv'
        with open(file, "r", encoding="utf-8-sig") as csv_file:
            data = csv.DictReader(csv_file, delimiter=",")
            if name == 'genre':
                for row in data:
                    Genre.objects.update_or_create(
                        name=row['name'],
                        slug=row['slug']
                    )
            elif name == 'category':
                for row in data:
                    Category.objects.update_or_create(
                        name=row['name'],
                        slug=row['slug']
                    )
            elif name == 'titles':
                for row in data:
                    Title.objects.update_or_create(
                        name=row['name'],
                        year=row['year'],
                        category_id=row['category']
                    )
            elif name == 'genre_title':
                for row in data:
                    print(row)
                    GenreTitle.objects.update_or_create(
                        title=row['title_id'],
                        genre=row['genre_id'],
                    )
