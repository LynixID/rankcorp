from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class RankResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    domain = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    rank = models.PositiveIntegerField()
    url_result = models.URLField()
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.domain} - {self.keyword} (Rank: {self.rank})"

class Billing(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    status_pembayaran = models.BooleanField(default=False)
    bukti_pembayaran = models.ImageField(upload_to='bukti_pembayaran/')

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return f"Billing for {self.username} - {'Lunas' if self.status_pembayaran else 'Belum Lunas'}"

class UserStatus(models.Model):
    STATUS_CHOICES = (
        ('guest', 'Guest'),
        ('premium', 'Premium'),
    )

    id = models.OneToOneField(
        'core.CustomUser',
        on_delete=models.CASCADE,
        primary_key=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='guest')
    total_quota = models.PositiveIntegerField(default=0)
    used_quota = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def remaining_quota(self):
        return self.total_quota - self.used_quota

    def is_active(self):
        return self.status == 'premium'

    @property
    def username(self):
        return self.id.username

    def __str__(self):
        return f"{self.username} ({self.status}) - Remaining: {self.remaining_quota()}"

    STATUS_CHOICES = (
        ('guest', 'Guest'),
        ('premium', 'Premium'),
    )

    id = models.OneToOneField(
        'core.CustomUser',
        on_delete=models.CASCADE,
        primary_key=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='guest')
    total_quota = models.PositiveIntegerField(default=0)
    used_quota = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def remaining_quota(self):
        return self.total_quota - self.used_quota

    def is_active(self):
        return self.status == 'premium'

    @property
    def username(self):
        return self.id.username

    def __str__(self):
        return f"{self.username} ({self.status}) - Remaining: {self.remaining_quota()}"

    STATUS_CHOICES = (
        ('guest', 'Guest'),
        ('premium', 'Premium'),
    )

    id = models.OneToOneField(
        'core.CustomUser',  # ganti sesuai path app kamu
        on_delete=models.CASCADE,
        primary_key=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='guest')
    total_quota = models.PositiveIntegerField(default=0)
    used_quota = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def remaining_quota(self):
        return self.total_quota - self.used_quota

    def is_active(self):
        return self.status == 'premium'

    def __str__(self):
        return f"{self.id.username} ({self.status}) - Remaining: {self.remaining_quota()}"
    

class QuotaPackage(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quota_amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - Rp{self.price:,} ({self.quota_amount} quota)"


class QuotaPurchase(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(QuotaPackage, on_delete=models.CASCADE)
    payment_proof = models.ImageField(upload_to='bukti_pembayaran/', null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name} ({self.status})"

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey('QuotaPackage', on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    gross_amount = models.IntegerField()
    transaction_status = models.CharField(max_length=50, default='pending')
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SeoAnalysis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    analysis = models.TextField()
    metadata = models.JSONField(blank=True, null=True)
    model_used = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.keyword} - {self.domain} ({self.model_used}) @ {self.created_at:%Y-%m-%d %H:%M}"


class AiModelConfig(models.Model):
    MODEL_CHOICES = (
        ('gemini', 'Gemini (Google)'),
        ('gpt-3.5-turbo', 'GPT-3.5 (OpenAI)'),
        ('gpt-4-1106-preview', 'GPT-4.1 (OpenAI)'),
    )
    
    model_name = models.CharField(max_length=50, choices=MODEL_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quota_cost = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} - {self.quota_cost} kuota"

    class Meta:
        verbose_name = "AI Model Configuration"
        verbose_name_plural = "AI Model Configurations"


class ApiConfig(models.Model):
    API_CHOICES = (
        ('serpapi', 'SerpAPI'),
        ('google_search', 'Google Search API'),
        ('bing_search', 'Bing Search API'),
    )
    
    api_name = models.CharField(max_length=50, choices=API_CHOICES, unique=True)
    api_key = models.CharField(max_length=255, help_text='API Key untuk layanan')
    base_url = models.URLField(max_length=500, help_text='Base URL untuk API')
    max_results = models.PositiveIntegerField(default=100, help_text='Jumlah maksimal hasil')
    timeout = models.PositiveIntegerField(default=30, help_text='Timeout dalam detik')
    is_active = models.BooleanField(default=True, help_text='Status aktif API')
    description = models.TextField(blank=True, help_text='Deskripsi konfigurasi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_api_name_display()} - {'Aktif' if self.is_active else 'Nonaktif'}"

    class Meta:
        verbose_name = "API Configuration"
        verbose_name_plural = "API Configurations"
        ordering = ['api_name']


class CheckoutSession(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(QuotaPackage, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name} ({self.status})"

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

    def get_remaining_time(self):
        from django.utils import timezone
        now = timezone.now()
        if now >= self.expires_at:
            return 0
        return int((self.expires_at - now).total_seconds())

    class Meta:
        verbose_name = "Checkout Session"
        verbose_name_plural = "Checkout Sessions"