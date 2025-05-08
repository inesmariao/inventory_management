from django.core.management.base import BaseCommand
from apps.company.models import Country
import json
from pathlib import Path
from django.conf import settings

class Command(BaseCommand):
    help = 'Import countries from JSON file'

    def handle(self, *args, **kwargs):
        file_path = settings.BASE_DIR / 'apps' / 'company' / 'fixtures' / 'country.json'
        if not file_path.exists():
            self.stdout.write(self.style.ERROR('Country JSON file not found'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i, item in enumerate(data, 1):
                Country.objects.update_or_create(
                    alpha_2=item['alpha_2'],
                    defaults={
                        'name': item['spanish_name'],
                        'alpha_3': item['alpha_3'],
                        'numeric_code': int(item['numeric_code']),
                    }
                )
                self.stdout.write(f"[{i}] Imported country: {item['spanish_name']}")
            self.stdout.write(self.style.SUCCESS('Countries imported successfully'))
