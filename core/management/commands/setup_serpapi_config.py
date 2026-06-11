import os
from django.core.management.base import BaseCommand
from core.models import ApiConfig

class Command(BaseCommand):
    help = 'Setup konfigurasi SerpAPI awal'

    def handle(self, *args, **options):
        # Konfigurasi SerpAPI
        serpapi_config, created = ApiConfig.objects.get_or_create(
            api_name='serpapi',
            defaults={
                'api_key': os.getenv('SERPAPI_KEY', ''),  # API key dari env
                'base_url': 'https://serpapi.com/search',
                'max_results': 100,
                'timeout': 30,
                'is_active': True,
                'description': 'SerpAPI untuk pencarian Google SERP'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('[OK] Konfigurasi SerpAPI berhasil dibuat')
            )
        else:
            self.stdout.write(
                self.style.WARNING('[WARNING] Konfigurasi SerpAPI sudah ada')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'[STATS] Total konfigurasi API: {ApiConfig.objects.count()}')
        ) 