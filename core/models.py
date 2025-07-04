from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

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
