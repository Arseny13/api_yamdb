import csv

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает Данные из csv, параметр название файла'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Путь к файлу')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file']
        if file_name == 'titles':
            name = 'title'
        else:
            name = ''.join(file_name.split('_'))
        model = ContentType.objects.get(
            app_label='reviews',
            model=name
        )
        file = f'static/data/{file_name}.csv'
        with open(file, "r", encoding="utf-8-sig") as csv_file:
            data = csv.DictReader(csv_file, delimiter=",")
            for row in data:
                model.model_class().objects.update_or_create(
                    **row
                )
