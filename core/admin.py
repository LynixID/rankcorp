from django.contrib import admin
from .models import QuotaPackage, AiModelConfig, ApiConfig

# Register your models here.
admin.site.register(QuotaPackage)

@admin.register(AiModelConfig)
class AiModelConfigAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'model_name', 'quota_cost', 'is_active', 'created_at')
    list_filter = ('is_active', 'quota_cost')
    search_fields = ('display_name', 'model_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('quota_cost', 'display_name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('model_name', 'display_name', 'description', 'quota_cost', 'is_active')
        }),
        ('API Configuration', {
            'fields': ('api_key',),
            'description': 'API key untuk model AI ini'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ApiConfig)
class ApiConfigAdmin(admin.ModelAdmin):
    list_display = ('api_name', 'is_active', 'max_results', 'timeout', 'created_at')
    list_filter = ('is_active', 'api_name', 'max_results')
    search_fields = ('api_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('api_name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('api_name', 'description', 'is_active')
        }),
        ('API Configuration', {
            'fields': ('api_key', 'base_url', 'max_results', 'timeout'),
            'description': 'Konfigurasi API untuk layanan pencarian'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

