import os
from django.core.management.base import BaseCommand
from core.models import AiModelConfig


class Command(BaseCommand):
    help = 'Setup initial AI model configurations'

    def handle(self, *args, **options):
        # Data model AI yang akan disetup
        models_data = [
            {
                'model_name': 'gemini',
                'display_name': 'Gemini (Google)',
                'description': 'Gemini (Google): cepat & murah, cocok untuk analisis ringan.',
                'quota_cost': 3,
                'api_key': os.getenv('GEMINI_API_KEY', ''),
                'is_active': True
            },
            {
                'model_name': 'gpt-3.5-turbo',
                'display_name': 'GPT-3.5 (OpenAI)',
                'description': 'GPT-3.5 (OpenAI): stabil, harga menengah, hasil cukup baik.',
                'quota_cost': 2,
                'api_key': os.getenv('OPENAI_API_KEY', ''),
                'is_active': True
            },
            {
                'model_name': 'gpt-4-1106-preview',
                'display_name': 'GPT-4.1 (OpenAI)',
                'description': 'GPT-4.1 (OpenAI): terbaik, analisis mendalam, kualitas tinggi.',
                'quota_cost': 5,
                'api_key': os.getenv('OPENAI_API_KEY', ''),
                'is_active': True
            }
        ]

        created_count = 0
        updated_count = 0

        for model_data in models_data:
            model, created = AiModelConfig.objects.get_or_create(
                model_name=model_data['model_name'],
                defaults=model_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {model.display_name}')
                )
            else:
                # Update existing model
                for key, value in model_data.items():
                    setattr(model, key, value)
                model.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated: {model.display_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Setup complete! Created: {created_count}, Updated: {updated_count}'
            )
        ) 