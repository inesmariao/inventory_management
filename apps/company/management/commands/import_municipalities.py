from django.core.management.base import BaseCommand
from apps.company.models import Municipality, Department
import json
from pathlib import Path
from django.conf import settings

class Command(BaseCommand):
    help = 'Import municipalities from JSON file'

    def handle(self, *args, **kwargs):
        file_path = settings.BASE_DIR / 'apps' / 'company' / 'fixtures' / 'municipality.json'
        if not file_path.exists():
            self.stdout.write(self.style.ERROR('Municipality JSON file not found'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i, item in enumerate(data, 1):
                try:
                    department = Department.objects.get(code=item['department_code'])
                    Municipality.objects.update_or_create(
                        code=item['code'],
                        defaults={
                            'name': item['name'],
                            'department': department
                        }
                    )
                    self.stdout.write(f"[{i}] Imported municipality: {item['name']}")
                except Department.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"[{i}] Department not found for municipality: {item['name']}"))

            self.stdout.write(self.style.SUCCESS('Municipalities imported successfully'))
