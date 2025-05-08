from django.core.management.base import BaseCommand
from apps.company.models import Department, Country
import json
from pathlib import Path
from django.conf import settings

class Command(BaseCommand):
    help = 'Import departments from JSON file'

    def handle(self, *args, **kwargs):
        file_path = settings.BASE_DIR / 'apps' / 'company' / 'fixtures' / 'department.json'
        if not file_path.exists():
            self.stdout.write(self.style.ERROR('Department JSON file not found'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i, item in enumerate(data, 1):
                try:
                    country = Country.objects.get(numeric_code=item['country_numeric_code'])
                    Department.objects.update_or_create(
                        code=item['code'],
                        defaults={
                            'name': item['name'],
                            'country': country
                        }
                    )
                    self.stdout.write(f"[{i}] Imported department: {item['name']}")
                except Country.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"[{i}] Country not found for department: {item['name']}"))

            self.stdout.write(self.style.SUCCESS('Departments imported successfully'))
