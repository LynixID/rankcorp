from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    # path('history/', views.history_view, name='history'),
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
    path('upload-proof/<int:package_id>/', views.upload_payment_proof_view, name='upload_proof'),
    path('status-pembelian/', views.purchase_status_view, name='purchase_status'),
    path('approve-quota/<int:purchase_id>/', views.approve_quota, name='approve_quota'),
    path('reject-quota/<int:purchase_id>/', views.reject_quota, name='reject_quota'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
