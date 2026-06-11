from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # API Config URLs (moved to top to avoid conflicts)
    path('api-config/<int:config_id>/update/', views.update_api_config_ajax, name='update_api_config_ajax_simple'),
    path('admin/api-config/<int:config_id>/toggle/', views.toggle_api_config_view, name='toggle_api_config'),
    path('admin/api-config/<int:config_id>/update/', views.update_api_config_ajax, name='update_api_config_ajax'),
    path('admin/api-config/<int:config_id>/test/', views.test_api_config, name='test_api_config'),
    
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('history/', views.history_summary_view, name='history_summary'),
    path('history/<str:keyword>/<str:domain>/', views.history_detail, name='history_detail'),
    path('pembayaran/', views.pembayaran, name='pembayaran'),
    path('pembayaran/sukses/', views.pembayaran_sukses, name='pembayaran_sukses'),
    path('pembayaran/diproses/', views.pembayaran_diproses, name='pembayaran_diproses'),
    path('approve-pembayaran/<int:user_id>/', views.approve_pembayaran, name='approve_pembayaran'),
    path('cek-rank/', views.check_rank_view, name='cek_rank'),
    path('dashboard/section/<str:section>/', views.dashboard_section, name='dashboard_section'),
    path('update-user-status/<int:user_id>/<str:action>/', views.update_user_status, name='update_user_status'),
    path('buy-quota/', views.buy_quota_view, name='buy_quota'),
    
    # Checkout Session URLs
    path('checkout/<int:package_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('cancel-checkout/<str:session_id>/', views.cancel_checkout_session, name='cancel_checkout_session'),
    
    path('upload-proof/<int:package_id>/', views.upload_payment_proof_view, name='upload_proof'),
    path('status-pembelian/', views.purchase_status_view, name='purchase_status'),
    path('approve-quota/<int:purchase_id>/', views.approve_quota, name='approve_quota'),
    path('reject-quota/<int:purchase_id>/', views.reject_quota, name='reject_quota'),
   
#    Paket Kuota
    path('add-quota-package/', views.add_quota_package, name='add_quota_package'),
    path('update-quota-package/<int:package_id>/', views.update_quota_package, name='update_quota_package'),
    path('delete-quota-package/<int:package_id>/', views.delete_quota_package, name='delete_quota_package'),
    
    # AI Model Config URLs
    path('add-ai-model-config/', views.add_ai_model_config, name='add_ai_model_config'),
    path('update-ai-model-config/<int:model_id>/', views.update_ai_model_config, name='update_ai_model_config'),
    path('delete-ai-model-config/<int:model_id>/', views.delete_ai_model_config, name='delete_ai_model_config'),

    path('payment/<int:package_id>/', views.start_payment, name='start_payment'),
    path('payment/notification/', views.payment_notification, name='payment_notification'),
    path('delete-transaction/<int:trx_id>/', views.delete_transaction, name='delete_transaction'),
    
    path('seo-analysis/', views.seo_analysis, name='seo_analysis'),
    path('seo-analysis-history/', views.seo_analysis_history_view, name='seo_analysis_history'),
    path('seo-analysis-detail/<int:analysis_id>/', views.seo_analysis_detail_view, name='seo_analysis_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
