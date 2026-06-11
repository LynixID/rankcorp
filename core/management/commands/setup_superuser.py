from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import UserStatus

User = get_user_model()


class Command(BaseCommand):
    help = 'Setup atau reset superuser dengan username: root, password: root@2025'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset-password',
            action='store_true',
            help='Reset password superuser yang sudah ada',
        )

    def handle(self, *args, **options):
        username = 'root'
        email = 'root.superuser@gmail.com'
        password = 'root@2025'
        
        reset_password = options['reset_password']
        
        try:
            # Cek apakah user sudah ada
            user = User.objects.filter(username=username).first()
            
            if user:
                if reset_password:
                    # Reset password
                    user.set_password(password)
                    user.is_superuser = True
                    user.is_staff = True
                    user.is_active = True
                    user.role = 'admin'
                    user.email = email
                    user.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Password superuser "{username}" berhasil direset!'
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'   Username: {username}'
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'   Password: {password}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Superuser "{username}" sudah ada!'
                        )
                    )
                    self.stdout.write(
                        self.style.WARNING(
                            f'   Gunakan --reset-password untuk reset password'
                        )
                    )
                    self.stdout.write(
                        self.style.WARNING(
                            f'   Contoh: python manage.py setup_superuser --reset-password'
                        )
                    )
            else:
                # Buat superuser baru
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    role='admin',
                    is_active=True
                )
                
                # Buat UserStatus untuk superuser
                UserStatus.objects.get_or_create(
                    id=user,
                    defaults={
                        'status': 'premium',
                        'total_quota': 999999,  # Unlimited quota untuk superuser
                        'used_quota': 0
                    }
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Superuser berhasil dibuat!'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'   Username: {username}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'   Email: {email}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'   Password: {password}'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Error: {str(e)}'
                )
            )







