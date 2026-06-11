from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import CustomUser, RankResult, Billing, UserStatus, QuotaPurchase, QuotaPackage, Transaction, SeoAnalysis, AiModelConfig, ApiConfig, CheckoutSession
from django.contrib.auth import get_user_model
from django.db.models import Count
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuotaPurchaseForm
from django.http import HttpResponseForbidden, HttpResponseNotFound, JsonResponse, HttpResponseNotAllowed
from django.utils import timezone
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.core.paginator import Paginator


import random
import requests
import json
import midtransclient
import uuid
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_ai_models_data():
    """
    Fungsi helper untuk mendapatkan data model AI dari database
    """
    try:
        models = AiModelConfig.objects.filter(is_active=True).order_by('quota_cost')
        return models
    except:
        # Fallback jika tabel belum ada atau error
        return []


def landing_page(request):
    return render(request, 'core/landing.html')

def login_view(request):
    # ✅ Cek jika user sudah login → redirect ke dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'core/login.html')

def generate_otp():
    return str(random.randint(100000, 999999))

def register_view(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        whatsapp = request.POST.get('whatsapp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validasi username sudah digunakan
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
            return redirect('register')

        # Validasi email sudah digunakan (opsional)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan.')
            return redirect('register')

        # Validasi format nomor WhatsApp (harus dimulai dengan 62)
        if not whatsapp.startswith('62'):
            messages.error(request, 'Nomor WhatsApp harus dimulai dengan 62 (contoh: 6281234567890).')
            return redirect('register')

        # Validasi konfirmasi password
        if password != confirm_password:
            messages.error(request, 'Konfirmasi password tidak cocok.')
            return redirect('register')

        # Jika semua valid → Simpan session + kirim OTP
        otp = generate_otp()
        request.session['pending_user'] = {
            'username': username,
            'email': email,
            'whatsapp': whatsapp,
            'password': password,
            'otp': otp
        }

        send_whatsapp_direct(
            device_key='sEVok3IhQs4avF5',
            token='al018FyLBRT1bwG3Z4C8gACULNZ3o5',
            phone=whatsapp,
            message=f"Kode OTP Anda: {otp}"
        )

        messages.success(request, 'Kode OTP telah dikirim ke WhatsApp Anda.')
        return redirect('verify_otp')

    return render(request, 'core/register.html')

def verify_otp_view(request):
    pending_user = request.session.get('pending_user')

    if not pending_user:
        messages.error(request, "Tidak ada proses pendaftaran yang berlangsung.")
        return redirect('register')

    if request.method == 'POST':
        input_otp = request.POST.get('otp')

        if input_otp == pending_user['otp']:
            User = get_user_model()

            # Cegah duplikasi user (misalnya karena refresh)
            if User.objects.filter(username=pending_user['username']).exists():
                messages.warning(request, "Akun sudah terdaftar, silakan login.")
                del request.session['pending_user']
                return redirect('login')

            # Buat user baru
            user = User.objects.create_user(
                username=pending_user['username'],
                email=pending_user['email'],
                password=pending_user['password'],
                whatsapp_number=pending_user['whatsapp'],
                role='user',
                is_active=True
            )

            # Tambahkan entri ke UserStatus
            UserStatus.objects.create(
                id=user,
                status='guest',
                total_quota=3,
                used_quota=0
            )

            # Bersihkan session
            del request.session['pending_user']

            messages.success(request, 'OTP berhasil diverifikasi. Silakan login.')
            return redirect('login')
        else:
            messages.error(request, 'Kode OTP salah.')

    return render(request, 'core/verify_otp.html', {'user_obj': pending_user})

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def dashboard(request):
    if request.user.role == 'admin' or request.user.is_superuser:
        # 30 hari terakhir
        thirty_days_ago = timezone.now() - timedelta(days=29)

        rank_per_day = (
            RankResult.objects
            .filter(checked_at__date__gte=thirty_days_ago.date())
            .annotate(day=TruncDate('checked_at'))
            .values('day')
            .annotate(total=Count('id'))
            .order_by('day')
        )

        dates = [item['day'].strftime("%Y-%m-%d") for item in rank_per_day]
        counts = [item['total'] for item in rank_per_day]

        datasets = [{
            "label": "Jumlah Cek Harian",
            "data": counts,
        }]

        # Data lainnya untuk dashboard
        total_users = CustomUser.objects.count()
        total_pembayaran_sukses = QuotaPurchase.objects.filter(status='approved').count()
        total_rank = RankResult.objects.count()
        pending_billings = QuotaPurchase.objects.filter(status='pending').count()
        recent_ranks = RankResult.objects.select_related('user').order_by('-checked_at')[:5]
        users = CustomUser.objects.all().order_by('-date_joined')
        billing_users = QuotaPurchase.objects.select_related('user', 'package').order_by('status')
        
        return render(request, 'core/dashboard_admin.html', {
            'total_users': total_users,
            'total_pembayaran_sukses': total_pembayaran_sukses,
            'total_rank': total_rank,
            'pending_billings': pending_billings,
            'recent_ranks': recent_ranks,
            'users': users,
            'billing_users': billing_users,
            'dates': json.dumps(dates),
            'datasets': json.dumps(datasets),
        })
    else:
        # Dashboard untuk user biasa
        history = RankResult.objects.filter(user=request.user).order_by('-checked_at')
        # Cek status pengguna
        try:
            user_status = request.user.userstatus
            used_quota = user_status.used_quota or 0
            total_quota = user_status.total_quota or 0
            sisa_kuota = total_quota - used_quota
        except UserStatus.DoesNotExist:
            user_status = None
            used_quota = total_quota = sisa_kuota = 0
        # Buat list unik kombinasi keyword-domain
        unique_history = []
        seen = set()
        for h in history:
            key = (h.keyword, h.domain)
            if key not in seen:
                unique_history.append({'keyword': h.keyword, 'domain': h.domain})
                seen.add(key)
        return render(request, 'core/search_rank.html', {
            'history': history,
            'unique_history': unique_history,
            'user_status': user_status,
            'used_quota': used_quota,
            'total_quota': total_quota,
            'sisa_quota': sisa_kuota,
            'result': None
        })

@login_required
def dashboard_section(request, section):
    # Batasi hanya untuk admin di section tertentu
    if section in ['stats', 'users'] and request.user.role != 'admin' and not request.user.is_superuser:
        return HttpResponseForbidden("Tidak punya akses")

    if section == 'stats':
        return render(request, 'core/dashboard_stats.html', {
            'total_users': CustomUser.objects.count(),
            'total_pembayaran_sukses': Billing.objects.filter(status_pembayaran=True).count(),
            'total_rank': RankResult.objects.count()
        })

    elif section == 'users':
        from django.core.paginator import Paginator
        users_qs = CustomUser.objects.all().order_by('-date_joined')
        paginator = Paginator(users_qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'core/dashboard_users.html', {
            'users': page_obj,
            'page_obj': page_obj
        })

    elif section == 'billing':
        from django.core.paginator import Paginator
        billing_data = QuotaPurchase.objects.select_related('user', 'package').order_by('-created_at')
        paginator = Paginator(billing_data, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'core/dashboard_billing_quota.html', {
            'billing_users': page_obj,
            'page_obj': page_obj
        })
    elif section == 'quotapackage':
        from django.core.paginator import Paginator
        packages_qs = QuotaPackage.objects.all().order_by('id')
        paginator = Paginator(packages_qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'core/dashboard_quotapackage.html', {
            'packages': page_obj,
            'page_obj': page_obj
        })
    elif section == 'transaction':
        from django.core.paginator import Paginator
        transactions = Transaction.objects.select_related('user', 'package').order_by('-created_at')
        paginator = Paginator(transactions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'core/dashboard_payment_gateway.html', {
            'transactions': page_obj,
            'page_obj': page_obj
        })
    elif section == 'aimodelconfig':
        from django.core.paginator import Paginator
        ai_models = AiModelConfig.objects.all().order_by('model_name')
        paginator = Paginator(ai_models, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'core/dashboard_aimodelconfig.html', {
            'ai_models': page_obj,
            'page_obj': page_obj
        })
    elif section == 'apiconfig':
        # Get API configurations
        api_configs = ApiConfig.objects.all().order_by('api_name')
        return render(request, 'core/dashboard_apiconfig.html', {
            'api_configs': api_configs
        })
        
    return HttpResponseNotFound("Section tidak ditemukan")

@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Kamu tidak punya akses.")
        return redirect('dashboard')

    user_obj = get_object_or_404(CustomUser, id=user_id)
    user_obj.delete()
    messages.success(request, "User berhasil dihapus.")
    
    # Redirect dengan indikator section users
    return redirect('/dashboard/?section=users')

@login_required
def update_user(request, user_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, "Kamu tidak punya akses.")
        return redirect('dashboard')

    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user_obj.username = request.POST.get('username')
        user_obj.email = request.POST.get('email')
        user_obj.whatsapp_number = request.POST.get('whatsapp')
        user_obj.role = request.POST.get('role')
        user_obj.save()

        messages.success(request, 'User berhasil diupdate.')
        return redirect('dashboard_section', section='users')

    return render(request, 'core/update_user.html', {'user_obj': user_obj})

@login_required
def add_quota_package(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quota_amount = request.POST.get('quota_amount')
        QuotaPackage.objects.create(name=name, price=price, quota_amount=quota_amount)
    return redirect('dashboard')

@login_required
def update_quota_package(request, package_id):
    package = get_object_or_404(QuotaPackage, id=package_id)
    if request.method == 'POST':
        package.name = request.POST.get('name')
        package.price = request.POST.get('price')
        package.quota_amount = request.POST.get('quota_amount')
        package.save()
    return redirect('dashboard')

@login_required
def delete_quota_package(request, package_id):
    package = get_object_or_404(QuotaPackage, id=package_id)
    package.delete()
    return redirect('dashboard')

# AI Model Config CRUD Operations
@login_required
def add_ai_model_config(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Kamu tidak punya akses.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        model_name = request.POST.get('model_name')
        display_name = request.POST.get('display_name')
        description = request.POST.get('description', '')
        quota_cost = request.POST.get('quota_cost')
        api_key = request.POST.get('api_key', '')
        is_active = request.POST.get('is_active') == 'on'
        
        # Validasi model_name unik
        if AiModelConfig.objects.filter(model_name=model_name).exists():
            messages.error(request, f"Model '{model_name}' sudah ada.")
            return redirect('dashboard')
        
        AiModelConfig.objects.create(
            model_name=model_name,
            display_name=display_name,
            description=description,
            quota_cost=quota_cost,
            api_key=api_key if api_key else None,
            is_active=is_active
        )
        
        messages.success(request, 'Model AI berhasil ditambahkan!')
        return redirect('dashboard')
    
    messages.error(request, 'Method tidak valid.')
    return redirect('dashboard')

@login_required
def update_ai_model_config(request, model_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Kamu tidak punya akses.')
        return redirect('dashboard')
    
    model = get_object_or_404(AiModelConfig, id=model_id)
    
    if request.method == 'POST':
        model.model_name = request.POST.get('model_name')
        model.display_name = request.POST.get('display_name')
        model.description = request.POST.get('description', '')
        model.quota_cost = request.POST.get('quota_cost')
        model.is_active = request.POST.get('is_active') == 'on'
        
        # Update API key hanya jika diisi
        api_key = request.POST.get('api_key', '')
        if api_key:
            model.api_key = api_key
        
        # Validasi model_name unik (kecuali untuk model yang sedang diedit)
        if AiModelConfig.objects.filter(model_name=model.model_name).exclude(id=model_id).exists():
            messages.error(request, f"Model '{model.model_name}' sudah ada.")
            return redirect('dashboard')
        
        model.save()
        messages.success(request, 'Model AI berhasil diupdate!')
        return redirect('dashboard')
    
    messages.error(request, 'Method tidak valid.')
    return redirect('dashboard')

@login_required
def delete_ai_model_config(request, model_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Kamu tidak punya akses.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        model = get_object_or_404(AiModelConfig, id=model_id)
        model_name = model.display_name
        model.delete()
        
        messages.success(request, f'Model AI "{model_name}" berhasil dihapus!')
        return redirect('dashboard')
    
    messages.error(request, 'Method tidak valid.')
    return redirect('dashboard')

@login_required
def approve_pembayaran(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
  
    billing = Billing.objects.filter(user=user).first()
    if billing:
        billing.status_pembayaran = True
        billing.save()

    # Update User
    user.is_active = True
    user.save()

    # Kirim WhatsApp konfirmasi aktif
    if user.whatsapp_number:
        send_whatsapp_direct(
            device_key='sEVok3IhQs4avF5',
            token='al018FyLBRT1bwG3Z4C8gACULNZ3o5',
            phone=user.whatsapp_number,
            message=f"Halo {user.username}, pembayaran Anda sudah diterima. Akun Anda sudah aktif. Silakan login."
        )

    messages.success(request, f"Pembayaran untuk {user.username} disetujui dan akun sudah aktif.")
    return redirect('dashboard')

def send_whatsapp_direct(device_key, token, phone, message, file_url=None):
    api_url = 'https://api.quods.id/api/direct-send'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'device_key': device_key,
        'phone': phone,
        'message': message
    }

    # Tambahkan file_url jika diberikan
    if file_url:
        payload['file_url'] = file_url

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        print("Status code:", response.status_code)
        print("Response text:", response.text)

        if response.status_code != 200:
            print("❌ Status code bukan 200.")
            return None

        result = response.json()
        print("Parsed JSON result:", result)

        if result.get('status') == 'success':
            print("✅ Pesan berhasil dikirim.")
        else:
            print(f"❌ Gagal: {result.get('message')}")
        return result

    except Exception as e:
        print(f"⚠ Error mengirim WA: {e}")
        return None
    
def get_ranks_serpapi(keyword, domain, hl, gl, google_domain, num):
    """
    Fungsi untuk mengambil ranking dari SerpAPI dengan retry logic dan error handling yang lebih baik.
    """
    try:
        # Ambil konfigurasi SerpAPI dari database
        api_config = ApiConfig.objects.get(api_name='serpapi', is_active=True)
        api_key = api_config.api_key
        base_url = api_config.base_url
        timeout = api_config.timeout
    except ApiConfig.DoesNotExist:
        # Fallback ke env jika tidak ada di database
        import os
        api_key = os.getenv("SERPAPI_KEY", "")
        base_url = "https://serpapi.com/search"
        timeout = 30
    
    params = {
        "engine": "google",
        "q": keyword,
        "google_domain": google_domain,
        "hl": hl,
        "gl": gl,
        "num": num,
        "api_key": api_key
    }
    
    # Setup retry strategy dengan exponential backoff
    retry_strategy = Retry(
        total=3,  # Maksimal 3 kali retry
        backoff_factor=1,  # Delay: 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504],  # Retry untuk status code ini
        allowed_methods=["GET"]
    )
    
    # Setup HTTPAdapter dengan retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # Buat session untuk connection pooling
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    # Set headers untuk menghindari connection issues
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = session.get(
                base_url, 
                params=params, 
                timeout=timeout,
                headers=headers
            )
            
            # Cek status code sebelum parsing JSON
            if response.status_code != 200:
                error_msg = f"SerpAPI returned status code {response.status_code}"
                if response.status_code == 429:
                    error_msg += " - Rate limit exceeded. Please try again later."
                elif response.status_code == 401:
                    error_msg += " - Invalid API key."
                elif response.status_code == 402:
                    error_msg += " - Insufficient credits."
                print(f"Error request SerpAPI: {error_msg}")
                return []
            
            # Parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"Error parsing SerpAPI JSON response: {e}")
                print(f"Response text: {response.text[:200]}")
                return []
            
            # Check for error in response
            if "error" in data:
                print(f"SerpAPI error: {data.get('error', 'Unknown error')}")
                return []
            
            ranks = []
            if "organic_results" in data:
                for idx, result in enumerate(data["organic_results"]):
                    link = result.get("link", "")
                    if domain in link:
                        ranks.append({
                            "position": idx + 1,
                            "link": link
                        })
            return ranks
            
        except requests.exceptions.ConnectionError as e:
            retry_count += 1
            error_detail = str(e)
            
            # Handle ConnectionResetError (10054) specifically
            if "10054" in error_detail or "Connection aborted" in error_detail or "forcibly closed" in error_detail:
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count  # Exponential backoff: 2s, 4s, 8s
                    print(f"Connection reset by remote host. Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Error koneksi ke SerpAPI setelah {max_retries} percobaan: Connection reset by remote host. Silakan coba lagi nanti.")
                    return []
            else:
                print(f"Error koneksi ke SerpAPI: {e}")
                return []
                
        except requests.exceptions.Timeout as e:
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2 ** retry_count
                print(f"Request timeout. Retrying in {wait_time} seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                print(f"Error request SerpAPI: Timeout setelah {max_retries} percobaan")
                return []
                
        except requests.RequestException as e:
            print(f"Error request SerpAPI: {e}")
            return []
            
        except Exception as e:
            print(f"Error tidak terduga saat memproses SerpAPI: {e}")
            return []
    
    return []

@login_required
def check_rank_view(request):
    result_data = None

    if request.method == "POST":
        # Ambil userstatus
        try:
            user_status = request.user.userstatus
        except UserStatus.DoesNotExist:
            messages.error(request, "Status user tidak ditemukan. Hubungi admin.")
            return redirect('dashboard')

        # Cek kuota
        if user_status.remaining_quota() <= 0:
            messages.error(request, "Kuota search Anda habis. Silakan lakukan pengisian ulang pada menu.")
            return redirect('dashboard')

        # Ambil data dari form
        domain = request.POST.get("domain")
        keyword = request.POST.get("keyword")
        hl = request.POST.get("hl")
        gl = request.POST.get("gl")
        google_domain = request.POST.get("google_domain")
        num = request.POST.get("num")

        # Request ke SerpAPI menggunakan konfigurasi dari database
        try:
            api_config = ApiConfig.objects.get(api_name='serpapi', is_active=True)
            api_key = api_config.api_key
            base_url = api_config.base_url
            timeout = api_config.timeout
        except ApiConfig.DoesNotExist:
            # Fallback ke env jika tidak ada di database
            import os
            api_key = os.getenv("SERPAPI_KEY", "")
            base_url = "https://serpapi.com/search"
            timeout = 30
        
        params = {
            "engine": "google",
            "q": keyword,
            "google_domain": google_domain,
            "hl": hl,
            "gl": gl,
            "num": num,
            "api_key": api_key
        }

        # Setup retry strategy dengan exponential backoff
        retry_strategy = Retry(
            total=3,  # Maksimal 3 kali retry
            backoff_factor=1,  # Delay: 1s, 2s, 4s
            status_forcelist=[429, 500, 502, 503, 504],  # Retry untuk status code ini
            allowed_methods=["GET"]
        )
        
        # Setup HTTPAdapter dengan retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy)
        
        # Buat session untuk connection pooling
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        # Set headers untuk menghindari connection issues
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        
        max_retries = 3
        retry_count = 0
        ranks = []
        
        while retry_count < max_retries:
            try:
                response = session.get(
                    base_url, 
                    params=params, 
                    timeout=timeout,
                    headers=headers
                )
                
                # Cek status code sebelum parsing JSON
                if response.status_code != 200:
                    error_msg = f"SerpAPI mengembalikan status code {response.status_code}"
                    if response.status_code == 429:
                        error_msg = "Rate limit SerpAPI tercapai. Silakan coba lagi dalam beberapa menit."
                    elif response.status_code == 401:
                        error_msg = "API key SerpAPI tidak valid atau expired."
                    elif response.status_code == 402:
                        error_msg = "Quota SerpAPI habis. Silakan hubungi admin."
                    messages.error(request, error_msg)
                    return render(request, 'core/search_rank.html', {
                        "result": None,
                        "history": [],
                        "unique_history": []
                    })
                
                # Parse JSON response
                try:
                    data = response.json()
                except json.JSONDecodeError as e:
                    messages.error(request, f"Error memproses response SerpAPI: Format data tidak valid")
                    return render(request, 'core/search_rank.html', {
                        "result": None,
                        "history": [],
                        "unique_history": []
                    })
                
                # Check for error in response
                if "error" in data:
                    error_msg = data.get('error', 'Unknown error')
                    messages.error(request, f"Error dari SerpAPI: {error_msg}")
                    return render(request, 'core/search_rank.html', {
                        "result": None,
                        "history": [],
                        "unique_history": []
                    })

                ranks = []
                if "organic_results" in data:
                    for idx, result in enumerate(data["organic_results"]):
                        link = result.get("link", "")
                        if domain in link:
                            ranks.append({
                                "position": idx + 1,
                                "link": link
                            })
                            # Simpan ke database
                            RankResult.objects.create(
                                user=request.user,
                                domain=domain,
                                keyword=keyword,
                                rank=idx + 1,
                                url_result=link
                            )
                
                # Berhasil, keluar dari loop retry
                break
                
            except requests.exceptions.ConnectionError as e:
                retry_count += 1
                error_detail = str(e)
                
                # Handle ConnectionResetError (10054) specifically
                if "10054" in error_detail or "Connection aborted" in error_detail or "forcibly closed" in error_detail:
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count  # Exponential backoff: 2s, 4s, 8s
                        time.sleep(wait_time)
                        continue
                    else:
                        messages.error(request, f"Error koneksi ke SerpAPI: Koneksi ditutup paksa oleh server setelah {max_retries} percobaan. Silakan coba lagi nanti atau hubungi admin jika masalah berlanjut.")
                        return render(request, 'core/search_rank.html', {
                            "result": None,
                            "history": [],
                            "unique_history": []
                        })
                else:
                    if retry_count >= max_retries:
                        messages.error(request, f"Error koneksi ke SerpAPI: {e}. Silakan periksa koneksi internet Anda.")
                        return render(request, 'core/search_rank.html', {
                            "result": None,
                            "history": [],
                            "unique_history": []
                        })
                    else:
                        wait_time = 2 ** retry_count
                        time.sleep(wait_time)
                        continue
                        
            except requests.exceptions.Timeout as e:
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    time.sleep(wait_time)
                    continue
                else:
                    messages.error(request, f"Request ke SerpAPI timeout setelah {max_retries} percobaan. Silakan coba lagi nanti.")
                    return render(request, 'core/search_rank.html', {
                        "result": None,
                        "history": [],
                        "unique_history": []
                    })
                    
            except requests.RequestException as e:
                messages.error(request, f"Error koneksi ke SerpAPI: {e}")
                return render(request, 'core/search_rank.html', {
                    "result": None,
                    "history": [],
                    "unique_history": []
                })
                
            except Exception as e:
                messages.error(request, f"Error memproses hasil SerpAPI: {e}")
                return render(request, 'core/search_rank.html', {
                    "result": None,
                    "history": [],
                    "unique_history": []
                })

        # Kurangi kuota jika hasil ditemukan
        user_status.used_quota += 1
        user_status.save()

        result_data = {
            "domain": domain,
            "keyword": keyword,
            "num": num,
            "total_found": len(ranks),
            "ranks": ranks
        }

    # Histori juga ditampilkan (opsional)
    history = RankResult.objects.filter(user=request.user).order_by('-checked_at')
    # Buat list unik kombinasi keyword-domain
    unique_history = []
    seen = set()
    for h in history:
        key = (h.keyword, h.domain)
        if key not in seen:
            unique_history.append({'keyword': h.keyword, 'domain': h.domain})
            seen.add(key)
    return render(request, 'core/search_rank.html', {
        "result": result_data,
        "history": history,
        "unique_history": unique_history
    })

@login_required
def history_view(request):
    results = RankResult.objects.filter(user=request.user).order_by('-checked_at')
    return render(request, 'core/history.html', {'results': results})

@login_required
def history_summary_view(request):
    # Grouping berdasarkan keyword + domain
    summaries = (
        RankResult.objects.filter(user=request.user)
        .values('keyword', 'domain')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    return render(request, 'core/history_summary.html', {'summaries': summaries})

@login_required
def history_detail(request, keyword, domain):
    results_qs = RankResult.objects.filter(
        user=request.user,
        keyword=keyword,
        domain=domain
    ).order_by('checked_at')

    # Paginasi
    page_number = request.GET.get('page', 1)
    paginator = Paginator(results_qs, 10)
    results = paginator.get_page(page_number)

    grouped_data = defaultdict(list)
    for r in results_qs:
        label = r.url_result  # Kelompokkan berdasarkan URL
        grouped_data[label].append((r.checked_at.strftime("%Y-%m-%d %H:%M"), r.rank))

    datasets = []
    all_labels = sorted(set(ts for values in grouped_data.values() for ts, _ in values))

    for url, values in grouped_data.items():
        # Buat dict dari timestamp → rank
        value_map = {ts: rank for ts, rank in values}
        rank_list = [value_map.get(ts, None) for ts in all_labels]

        datasets.append({
            'label': url[:40] + '...' if len(url) > 40 else url,
            'data': rank_list
        })

    # Cek status user
    try:
        user_status = request.user.userstatus
    except UserStatus.DoesNotExist:
        user_status = None

    # Ambil data model AI dari database
    ai_models = get_ai_models_data()
    
    # Siapkan data JSON untuk JavaScript
    if ai_models:
        ai_models_json = json.dumps({
            model.model_name: f"{model.description or model.display_name} ({model.quota_cost} Kuota)"
            for model in ai_models
        })
        ai_models_cost_json = json.dumps({
            model.model_name: model.quota_cost
            for model in ai_models
        })
    else:
        # Fallback data
        ai_models_json = json.dumps({
            "gemini": "Gemini (Google): cepat & murah, cocok untuk analisis ringan. (3 Kuota)",
            "gpt-3.5-turbo": "GPT-3.5 (OpenAI): stabil, harga menengah, hasil cukup baik. (2 Kuota)",
            "gpt-4-1106-preview": "GPT-4.1 (OpenAI): terbaik, analisis mendalam, kualitas tinggi. (5 Kuota)"
        })
        ai_models_cost_json = json.dumps({
            "gemini": 3,
            "gpt-3.5-turbo": 2,
            "gpt-4-1106-preview": 5
        })
    
    context = {
        'results': results,
        'keyword': keyword,
        'domain': domain,
        'dates': json.dumps(all_labels),
        'datasets': json.dumps(datasets),
        'rank_history_json': json.dumps([
            {
                "date": r.checked_at.strftime("%Y-%m-%d %H:%M"),
                "rank": r.rank,
                "url": r.url_result
            } for r in results_qs
        ]),
        'paginator': paginator,
        'page_obj': results,
        'user_status': user_status,
        'ai_models': ai_models,
        'ai_models_json': ai_models_json,
        'ai_models_cost_json': ai_models_cost_json,
    }

    return render(request, 'core/history_detail.html', context)

@csrf_exempt
@login_required
def seo_analysis(request):
    if request.method == "POST":
        # Cek status premium user dengan validasi yang lebih robust
        try:
            user_status = request.user.userstatus
            if not user_status:
                return JsonResponse({
                    "error": "Status user tidak ditemukan. Silakan hubungi admin.",
                    "redirect": True,
                    "message": "Status user tidak ditemukan. Silakan hubungi admin."
                }, status=403)
            
            if user_status.status != 'premium':
                return JsonResponse({
                    "error": "Fitur Analisa SEO hanya tersedia untuk user Premium",
                    "redirect": True,
                    "message": "Anda harus upgrade ke Premium untuk mengakses fitur Analisa SEO. Silakan lakukan pembelian kuota untuk upgrade status Anda.",
                    "upgrade_url": reverse('buy_quota')
                }, status=403)
                
        except UserStatus.DoesNotExist:
            return JsonResponse({
                "error": "Status user tidak ditemukan. Silakan hubungi admin.",
                "redirect": True,
                "message": "Status user tidak ditemukan. Silakan hubungi admin."
            }, status=403)
        
        # Validasi data input
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Data request tidak valid",
                "message": "Format data yang dikirim tidak valid."
            }, status=400)
            
        keyword = data.get("keyword")
        domain = data.get("domain")
        rank_history = data.get("rank_history", [])
        model_choice = data.get("model", "gpt-4o")  # Default ke GPT-4o
        
        # Validasi data yang diperlukan
        if not keyword or not domain:
            return JsonResponse({
                "error": "Data tidak lengkap",
                "message": "Keyword dan domain harus diisi."
            }, status=400)

        # Validasi model choice
        valid_models = ["gemini", "gpt-3.5-turbo", "gpt-4-1106-preview"]
        if model_choice not in valid_models:
            return JsonResponse({
                "error": "Model tidak valid",
                "message": "Pilihan model tidak valid."
            }, status=400)

        # Hitung cost kuota berdasarkan model
        try:
            model_config = AiModelConfig.objects.get(model_name=model_choice)
            quota_cost = model_config.quota_cost
        except AiModelConfig.DoesNotExist:
            quota_cost = 5 # Default cost jika model tidak ditemukan

        # Cek kuota cukup
        if user_status.remaining_quota() < quota_cost:
            return JsonResponse({
                "error": "Kuota Anda tidak cukup untuk analisa dengan model ini.",
                "message": f"Model {model_choice} membutuhkan {quota_cost} kuota. Sisa kuota Anda: {user_status.remaining_quota()}.",
                "upgrade_url": reverse('buy_quota')
            }, status=403)

        # Analisis data ranking untuk konteks tambahan
        trend = "tidak cukup data"
        stability = "tidak cukup data"
        avg_rank = rank_history[0]['rank'] if rank_history else 0

        if len(rank_history) >= 2:
            first_rank = rank_history[0]['rank']
            last_rank = rank_history[-1]['rank']
            rank_change = first_rank - last_rank
            
            if rank_change > 0:
                trend = "meningkat"
            elif rank_change < 0:
                trend = "menurun"
            else:
                trend = "stabil"
                
            avg_rank = sum(rh['rank'] for rh in rank_history) / len(rank_history)
            rank_variance = sum((rh['rank'] - avg_rank) ** 2 for rh in rank_history) / len(rank_history)
            stability = "stabil" if rank_variance < 5 else "fluktuatif"

        # Prompt yang disesuaikan berdasarkan model
        base_prompt = f"""Analisa performa SEO website berikut secara mendalam dan berikan insight actionable:\n\n**DATA WEBSITE:**\nKeyword: {keyword}\nDomain: {domain}\nJumlah data histori: {len(rank_history)} data\n\n**HISTORI RANKING:**\n"""
        for rh in rank_history:
            base_prompt += f"- {rh['date']}: rank {rh['rank']} ({rh['url']})\\n"

        # Routing berdasarkan model
        if model_choice == "gemini":
            # --- GEMINI API ---
            prompt = base_prompt + """
**ANALISIS YANG DIMINTA:**

1. **RINGKASAN SINGKAT** (2-3 kalimat):
   - Bagaimana tren ranking secara keseluruhan?
   - Apakah performa SEO sudah baik, stabil, menurun, atau perlu perbaikan?

2. **ANALISIS TREN** (detail):
   - Jelaskan pola perubahan ranking dari waktu ke waktu
   - Identifikasi titik-titik kritis (naik/turun signifikan)
   - Bandingkan dengan tren rata-rata

3. **PENYEBAB KEMUNGKINAN**:
   - Faktor internal: perubahan konten, struktur website, technical SEO
   - Faktor eksternal: update algoritma Google, kompetitor, seasonality
   - Berikan analisis berdasarkan data yang tersedia

4. **REKOMENDASI KONKRIT** (minimal 3):
   - Rekomendasi untuk meningkatkan ranking
   - Rekomendasi untuk mempertahankan ranking (jika sudah baik)
   - Prioritas rekomendasi (high/medium/low)
   - Estimasi waktu implementasi

5. **TARGET & MONITORING**:
   - Target ranking yang realistis
   - Metrik yang perlu dimonitor
   - Frekuensi pengecekan yang disarankan

**FORMAT OUTPUT:**
Gunakan format berikut dengan bahasa yang mudah dipahami user non-teknis:

**📊 RINGKASAN**
[Ringkasan singkat tren dan status SEO]

**📈 ANALISIS TREN**
[Detail analisis tren ranking]

**🔍 PENYEBAB**
[Analisis kemungkinan penyebab]

**💡 REKOMENDASI**
1. [Rekomendasi 1] - Prioritas: [High/Medium/Low]
2. [Rekomendasi 2] - Prioritas: [High/Medium/Low]
3. [Rekomendasi 3] - Prioritas: [High/Medium/Low]

**🎯 TARGET & MONITORING**
[Target dan metrik monitoring]

Berikan analisis yang actionable dan mudah diimplementasikan oleh pemilik website."""
            # Ambil API key dari database
            try:
                model_config = AiModelConfig.objects.get(model_name=model_choice)
                API_KEY = model_config.api_key
                if not API_KEY:
                    return JsonResponse({
                        "error": "API key tidak tersedia untuk model ini",
                        "message": "Model AI belum dikonfigurasi dengan benar. Silakan hubungi admin."
                    }, status=500)
            except AiModelConfig.DoesNotExist:
                return JsonResponse({
                    "error": "Model AI tidak ditemukan",
                    "message": "Model AI yang dipilih tidak tersedia."
                }, status=400)
            gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": API_KEY
            }
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                }
            }
            try:
                response = requests.post(gemini_url, headers=headers, json=payload, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    candidates = result.get("candidates", [])
                    if candidates and len(candidates) > 0:
                        content = candidates[0].get("content", {})
                        parts = content.get("parts", [])
                        if parts and len(parts) > 0:
                            analysis = parts[0].get("text", "")
                            if analysis and len(analysis.strip()) > 50:
                                # Simpan ke database
                                SeoAnalysis.objects.create(
                                    user=request.user,
                                    keyword=keyword,
                                    domain=domain,
                                    analysis=analysis,
                                    metadata={
                                        "trend": trend,
                                        "stability": stability,
                                        "avg_rank": round(avg_rank, 1),
                                        "data_points": len(rank_history),
                                        "analysis_quality": "high",
                                        "model_used": model_config.display_name
                                    },
                                    model_used=model_config.model_name
                                )
                                # Setelah analisis sukses, kurangi kuota:
                                user_status.used_quota += quota_cost
                                user_status.save()
                                return JsonResponse({
                                    "analysis": analysis,
                                    "metadata": {
                                        "trend": trend,
                                        "stability": stability,
                                        "avg_rank": round(avg_rank, 1),
                                        "data_points": len(rank_history),
                                        "analysis_quality": "high",
                                        "model_used": model_config.display_name
                                    }
                                })
                            else:
                                return JsonResponse({
                                    "error": "Hasil analisis terlalu pendek atau kosong",
                                    "message": "API mengembalikan hasil yang tidak memadai. Silakan coba lagi."
                                }, status=500)
                        else:
                            return JsonResponse({
                                "error": "Format response API tidak valid",
                                "message": "Struktur response dari API tidak sesuai yang diharapkan."
                            }, status=500)
                    else:
                        return JsonResponse({
                            "error": "Tidak ada hasil dari API",
                            "message": "API tidak mengembalikan hasil analisis."
                        }, status=500)
                else:
                    error_message = f"API Error: {response.status_code}"
                    if response.status_code == 429:
                        error_message = "API rate limit tercapai. Silakan coba lagi dalam beberapa menit."
                    elif response.status_code == 400:
                        error_message = "Request tidak valid. Silakan periksa data yang dikirim."
                    elif response.status_code == 401:
                        error_message = "API key tidak valid atau expired."
                    return JsonResponse({
                        "error": error_message,
                        "message": "Gagal mengambil analisis dari API. Silakan coba lagi."
                    }, status=response.status_code)
            except requests.exceptions.Timeout:
                return JsonResponse({
                    "error": "Timeout",
                    "message": "Request ke API timeout. Silakan coba lagi."
                }, status=408)
            except requests.exceptions.ConnectionError:
                return JsonResponse({
                    "error": "Connection Error",
                    "message": "Gagal terhubung ke API. Periksa koneksi internet Anda."
                }, status=503)
            except Exception as e:
                return JsonResponse({
                    "error": "Unexpected Error",
                    "message": f"Terjadi kesalahan tidak terduga: {str(e)}"
                }, status=500)

        else:
            # --- OPENAI API ---
            if model_choice == "gpt-3.5-turbo":
                openai_model = "gpt-3.5-turbo"
                max_tokens = 2500
            else:
                openai_model = "gpt-4-1106-preview"
                max_tokens = 3000
            prompt = base_prompt + """
**ANALISIS YANG DIMINTA:**

1. **RINGKASAN SINGKAT** (2-3 kalimat):
   - Bagaimana tren ranking secara keseluruhan?
   - Apakah performa SEO sudah baik, stabil, menurun, atau perlu perbaikan?

2. **ANALISIS TREN** (detail):
   - Jelaskan pola perubahan ranking dari waktu ke waktu
   - Identifikasi titik-titik kritis (naik/turun signifikan)
   - Bandingkan dengan tren rata-rata

3. **PENYEBAB KEMUNGKINAN**:
   - Faktor internal: perubahan konten, struktur website, technical SEO
   - Faktor eksternal: update algoritma Google, kompetitor, seasonality
   - Berikan analisis berdasarkan data yang tersedia

4. **REKOMENDASI KONKRIT** (minimal 3):
   - Rekomendasi untuk meningkatkan ranking
   - Rekomendasi untuk mempertahankan ranking (jika sudah baik)
   - Prioritas rekomendasi (high/medium/low)
   - Estimasi waktu implementasi

5. **TARGET & MONITORING**:
   - Target ranking yang realistis
   - Metrik yang perlu dimonitor
   - Frekuensi pengecekan yang disarankan

**FORMAT OUTPUT:**
Gunakan format berikut dengan bahasa yang mudah dipahami user non-teknis:

**📊 RINGKASAN**
[Ringkasan singkat tren dan status SEO]

**📈 ANALISIS TREN**
[Detail analisis tren ranking]

**🔍 PENYEBAB**
[Analisis kemungkinan penyebab]

**💡 REKOMENDASI**
1. [Rekomendasi 1] - Prioritas: [High/Medium/Low]
2. [Rekomendasi 2] - Prioritas: [High/Medium/Low]
3. [Rekomendasi 3] - Prioritas: [High/Medium/Low]

**🎯 TARGET & MONITORING**
[Target dan metrik monitoring]

Berikan analisis yang actionable dan mudah diimplementasikan oleh pemilik website."""
            import os
            try:
                model_config = AiModelConfig.objects.get(model_name=model_choice)
                OPENAI_API_KEY = model_config.api_key or os.getenv("OPENAI_API_KEY", "")
            except AiModelConfig.DoesNotExist:
                OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
            openai_url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            payload = {
                "model": openai_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Anda adalah ahli SEO yang berpengalaman. Berikan analisis yang akurat, actionable, dan mudah dipahami oleh pemilik website."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            try:
                response = requests.post(openai_url, headers=headers, json=payload, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    choices = result.get("choices", [])
                    if choices and len(choices) > 0:
                        message = choices[0].get("message", {})
                        analysis = message.get("content", "")
                        if analysis and len(analysis.strip()) > 50:
                            # Simpan ke database
                            SeoAnalysis.objects.create(
                                user=request.user,
                                keyword=keyword,
                                domain=domain,
                                analysis=analysis,
                                metadata={
                                    "trend": trend,
                                    "stability": stability,
                                    "avg_rank": round(avg_rank, 1),
                                    "data_points": len(rank_history),
                                    "analysis_quality": "high",
                                    "model_used": openai_model
                                },
                                model_used=openai_model
                            )
                            # Setelah analisis sukses, kurangi kuota:
                            user_status.used_quota += quota_cost
                            user_status.save()
                            return JsonResponse({
                                "analysis": analysis,
                                "metadata": {
                                    "trend": trend,
                                    "stability": stability,
                                    "avg_rank": round(avg_rank, 1),
                                    "data_points": len(rank_history),
                                    "analysis_quality": "high",
                                    "model_used": openai_model
                                }
                            })
                        else:
                            return JsonResponse({
                                "error": "Hasil analisis terlalu pendek atau kosong",
                                "message": "API mengembalikan hasil yang tidak memadai. Silakan coba lagi."
                            }, status=500)
                    else:
                        return JsonResponse({
                            "error": "Tidak ada hasil dari API",
                            "message": "API tidak mengembalikan hasil analisis."
                        }, status=500)
                else:
                    error_message = f"API Error: {response.status_code}"
                    if response.status_code == 429:
                        error_message = "API rate limit tercapai. Silakan coba lagi dalam beberapa menit."
                    elif response.status_code == 400:
                        error_message = "Request tidak valid. Silakan periksa data yang dikirim."
                    elif response.status_code == 401:
                        error_message = "API key tidak valid atau expired."
                    elif response.status_code == 402:
                        error_message = "Quota API habis. Silakan cek saldo OpenAI Anda."
                    return JsonResponse({
                        "error": error_message,
                        "message": "Gagal mengambil analisis dari API. Silakan coba lagi."
                    }, status=response.status_code)
            except requests.exceptions.Timeout:
                return JsonResponse({
                    "error": "Timeout",
                    "message": "Request ke API timeout. Silakan coba lagi."
                }, status=408)
            except requests.exceptions.ConnectionError:
                return JsonResponse({
                    "error": "Connection Error",
                    "message": "Gagal terhubung ke API. Periksa koneksi internet Anda."
                }, status=503)
            except Exception as e:
                return JsonResponse({
                    "error": "Unexpected Error",
                    "message": f"Terjadi kesalahan tidak terduga: {str(e)}"
                }, status=500)

@login_required
def pembayaran(request):
    if request.method == 'POST':
        metode = request.POST.get('metode')
        bukti_file = request.FILES.get('bukti')

        if not metode or not bukti_file:
            messages.error(request, 'Metode dan bukti pembayaran wajib diisi.')
            return redirect('pembayaran')

        # Simpan file bukti pembayaran
        fs = FileSystemStorage()
        filename = fs.save(bukti_file.name, bukti_file)
        file_url = request.build_absolute_uri(fs.url(filename))

        # Masukkan ke tabel Billing
        from .models import Billing
        Billing.objects.create(
            user=request.user,
            bukti_pembayaran=filename,  # simpan path file
            status_pembayaran=False
        )

        # Kirim WA ke admin (opsional)
        send_whatsapp_direct(
            device_key="UMSZSzMyen40UdD",
            token="TMeTyUimv75LmlHRlCutowWU2z86QW",
            phone="6285941051469",
            message=(
                f"Bukti transfer diterima.\n"
                f"User: {request.user.username}\n"
                f"Metode: {metode}\n"
                f"Nominal: Rp 199.000\n"
                f"Lihat bukti: {file_url}"
            )
        )

        messages.success(request, 'Bukti pembayaran dikirim. Tunggu persetujuan admin.')
        return redirect('pembayaran_sukses')

    return render(request, 'core/pembayaran.html')

def pembayaran_sukses(request):
    return render(request, 'core/pembayaran_sukses.html')

def pembayaran_diproses(request):
    # Hanya user yang belum aktif yang boleh ke sini
    if request.user.is_active:
        return redirect('dashboard')
    
    return render(request, 'core/pembayaran_diproses.html')


@login_required
def update_user_status(request, user_id, action):
    if request.user.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Kamu tidak punya akses.')
        return redirect('dashboard')

    user = get_object_or_404(CustomUser, id=user_id)

    if action == 'activate':
        user.is_active = True
        messages.success(request, f"{user.username} telah diaktifkan.")
    elif action == 'deactivate':
        user.is_active = False
        messages.success(request, f"{user.username} telah dinonaktifkan.")
    else:
        messages.error(request, "Aksi tidak valid.")
        return redirect('dashboard')

    user.save()
    return redirect('dashboard')

@login_required
def buy_quota_view(request):
    # Check if user has an active session first
    active_session = CheckoutSession.objects.filter(
        user=request.user,
        status='active'
    ).first()
    
    if active_session and not active_session.is_expired():
        # If user has active session, redirect directly to upload page
        return redirect('upload_proof', package_id=active_session.package.id)
    
    # If no active session or session expired, show packages
    packages = QuotaPackage.objects.all()
    return render(request, 'core/buy_quota.html', {'packages': packages})


@login_required
def create_checkout_session(request, package_id):
    """Create a new checkout session for manual transfer"""
    from django.utils import timezone
    from datetime import timedelta
    import uuid
    
    package = get_object_or_404(QuotaPackage, id=package_id)
    
    # Check if user already has an active session
    existing_session = CheckoutSession.objects.filter(
        user=request.user,
        status='active'
    ).first()
    
    if existing_session:
        # If session is not expired, redirect to upload page
        if not existing_session.is_expired():
            return redirect('upload_proof', package_id=existing_session.package.id)
        else:
            # Mark expired session as expired
            existing_session.status = 'expired'
            existing_session.save()
    
    # Create new session
    session_id = str(uuid.uuid4())
    expires_at = timezone.now() + timedelta(hours=2)
    
    checkout_session = CheckoutSession.objects.create(
        user=request.user,
        package=package,
        session_id=session_id,
        expires_at=expires_at
    )
    
    return redirect('upload_proof', package_id=package_id)


@login_required
def cancel_checkout_session(request, session_id):
    """Cancel a checkout session"""
    try:
        session = CheckoutSession.objects.get(
            session_id=session_id,
            user=request.user,
            status='active'
        )
        session.status = 'cancelled'
        session.save()
        messages.success(request, 'Pesanan berhasil dibatalkan.')
    except CheckoutSession.DoesNotExist:
        messages.error(request, 'Sesi tidak ditemukan atau sudah tidak aktif.')
    
    return redirect('buy_quota')


@login_required
def upload_payment_proof_view(request, package_id):
    package = get_object_or_404(QuotaPackage, id=package_id)
    
    # Check for active session
    active_session = CheckoutSession.objects.filter(
        user=request.user,
        package=package,
        status='active'
    ).first()
    
    if not active_session or active_session.is_expired():
        messages.error(request, 'Sesi checkout tidak ditemukan atau sudah berakhir. Silakan pilih paket lagi.')
        return redirect('buy_quota')
    
    if request.method == 'POST':
        form = QuotaPurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.package = package
            purchase.status = 'pending'
            purchase.save()
            
            # Mark session as completed
            active_session.status = 'completed'
            active_session.save()
            
            messages.success(
                request, 'Bukti pembayaran berhasil diunggah. Tunggu konfirmasi admin.'
            )
            return redirect('purchase_status')
    else:
        form = QuotaPurchaseForm()

    return render(request, 'core/upload_payment.html', {
        'form': form,
        'package': package,
        'checkout_session': active_session,
    })

@login_required
def purchase_status_view(request):
    purchases = QuotaPurchase.objects.filter(user=request.user).select_related('package').order_by('-created_at')
    return render(request, 'core/purchase_status.html', {'purchases': purchases})

@login_required
def approve_quota(request, purchase_id):
    if not request.user.is_superuser and request.user.role != 'admin':
        return redirect('dashboard')

    try:
        purchase = QuotaPurchase.objects.get(id=purchase_id)
        purchase.status = 'approved'
        purchase.save()

        # Tambahkan kuota ke user
        user_status, created = UserStatus.objects.get_or_create(id=purchase.user)
        user_status.total_quota += purchase.package.quota_amount
        user_status.save()

        # Kirim notifikasi WhatsApp ke user
        try:
            if hasattr(purchase.user, 'whatsapp_number') and purchase.user.whatsapp_number:
                # Format nomor WhatsApp (hapus spasi, strip, pastikan format benar)
                phone_number = purchase.user.whatsapp_number.strip().replace(' ', '').replace('-', '').replace('+', '')
                
                # Jika nomor tidak dimulai dengan 62 (kode Indonesia), tambahkan
                if phone_number.startswith('0'):
                    phone_number = '62' + phone_number[1:]
                elif not phone_number.startswith('62'):
                    phone_number = '62' + phone_number
                
                message = (
                    f"✅ *Pembayaran Disetujui*\n\n"
                    f"Halo {purchase.user.username},\n\n"
                    f"🎉 Pembayaran paket *{purchase.package.name}* seharga *Rp {purchase.package.price:,}* telah *disetujui* oleh admin.\n\n"
                    f"📦 Kuota Anda bertambah *{purchase.package.quota_amount}* kuota.\n"
                    f"💰 Total kuota Anda sekarang: *{user_status.total_quota}* kuota.\n\n"
                    f"💬 Terima kasih telah menggunakan layanan kami!"
                )

                print(f"📱 Mengirim notifikasi WA ke {phone_number} untuk user {purchase.user.username}")
                result = send_whatsapp_direct(
                    device_key=settings.QUODS_DEVICE_KEY,
                    token=settings.QUODS_BEARER_TOKEN,
                    phone=phone_number,
                    message=message
                )
                
                if result and result.get('status') == 'success':
                    print(f"✅ Notifikasi WA berhasil dikirim ke {purchase.user.username}")
                else:
                    print(f"⚠️ Gagal mengirim notifikasi WA ke {purchase.user.username}: {result}")
            else:
                print(f"⚠️ User {purchase.user.username} tidak memiliki nomor WhatsApp")
        except Exception as e:
            print(f"⚠️ Error saat mengirim notifikasi WA: {e}")
            # Jangan gagalkan proses approve jika WA gagal

        messages.success(request, f"Pembayaran paket '{purchase.package.name}' dari {purchase.user.username} berhasil disetujui.")
        return redirect('dashboard')

    except QuotaPurchase.DoesNotExist:
        messages.error(request, "Pembelian kuota tidak ditemukan.")
        return redirect('dashboard')

@login_required
def reject_quota(request, purchase_id):
    if not request.user.is_superuser and request.user.role != 'admin':
        return redirect('dashboard')

    try:
        purchase = QuotaPurchase.objects.get(id=purchase_id)
        purchase.status = 'rejected'
        purchase.save()

        # Kirim notifikasi WhatsApp ke user
        try:
            if hasattr(purchase.user, 'whatsapp_number') and purchase.user.whatsapp_number:
                # Format nomor WhatsApp (hapus spasi, strip, pastikan format benar)
                phone_number = purchase.user.whatsapp_number.strip().replace(' ', '').replace('-', '').replace('+', '')
                
                # Jika nomor tidak dimulai dengan 62 (kode Indonesia), tambahkan
                if phone_number.startswith('0'):
                    phone_number = '62' + phone_number[1:]
                elif not phone_number.startswith('62'):
                    phone_number = '62' + phone_number
                
                message = (
                    f"❌ *Pembayaran Ditolak*\n\n"
                    f"Halo {purchase.user.username},\n\n"
                    f"Maaf, pembayaran paket *{purchase.package.name}* seharga *Rp {purchase.package.price:,}* telah *ditolak* oleh admin.\n\n"
                    f"📋 *Kemungkinan alasan:*\n"
                    f"• Bukti pembayaran tidak jelas atau tidak valid\n"
                    f"• Nominal pembayaran tidak sesuai\n"
                    f"• Rekening tujuan tidak sesuai\n"
                    f"• Atau alasan lainnya\n\n"
                    f"💡 *Tindakan selanjutnya:*\n"
                    f"Silakan periksa kembali bukti pembayaran Anda dan upload ulang jika diperlukan.\n\n"
                    f"💬 Jika ada pertanyaan, silakan hubungi admin."
                )

                print(f"📱 Mengirim notifikasi WA ke {phone_number} untuk user {purchase.user.username}")
                result = send_whatsapp_direct(
                    device_key=settings.QUODS_DEVICE_KEY,
                    token=settings.QUODS_BEARER_TOKEN,
                    phone=phone_number,
                    message=message
                )
                
                if result and result.get('status') == 'success':
                    print(f"✅ Notifikasi WA berhasil dikirim ke {purchase.user.username}")
                else:
                    print(f"⚠️ Gagal mengirim notifikasi WA ke {purchase.user.username}: {result}")
            else:
                print(f"⚠️ User {purchase.user.username} tidak memiliki nomor WhatsApp")
        except Exception as e:
            print(f"⚠️ Error saat mengirim notifikasi WA: {e}")
            # Jangan gagalkan proses reject jika WA gagal

        messages.success(request, f"Pembayaran paket '{purchase.package.name}' dari {purchase.user.username} berhasil ditolak.")
        return redirect('dashboard')

    except QuotaPurchase.DoesNotExist:
        messages.error(request, "Pembelian kuota tidak ditemukan.")
        return redirect('dashboard')

def start_payment(request, package_id):
    package = get_object_or_404(QuotaPackage, id=package_id)
    order_id = str(uuid.uuid4())

    trx = Transaction.objects.create(
        user=request.user,
        package=package,
        order_id=order_id,
        gross_amount=package.price,
    )

    snap = midtransclient.Snap(
        is_production=settings.MIDTRANS_IS_PRODUCTION,
        server_key=settings.MIDTRANS_SERVER_KEY,
        client_key=settings.MIDTRANS_CLIENT_KEY
    )

    transaction = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": package.price,
        },
        "customer_details": {
            "first_name": request.user.username,
            "email": request.user.email,
        },
        "callbacks": {
            "finish": request.build_absolute_uri("/payment/finish/")
        }
    }

    snap_token = snap.create_transaction(transaction)["token"]

    return JsonResponse({
        "snap_token": snap_token,
        "client_key": settings.MIDTRANS_CLIENT_KEY
    })

@csrf_exempt
def payment_notification(request):
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")
        status = data.get("transaction_status")

        trx = Transaction.objects.select_related('package', 'user').get(order_id=order_id)

        is_new_settlement = status == "settlement"

        trx.transaction_status = status
        trx.payment_type = data.get("payment_type")
        trx.save()

        if is_new_settlement:
            # ✅ Update kuota dan status user
            user_status, _ = UserStatus.objects.get_or_create(id=trx.user)
            user_status.total_quota += trx.package.quota_amount
            user_status.status = "premium"
            user_status.save()

            # ✅ Kirim WhatsApp ke nomor user
            if hasattr(trx.user, 'whatsapp_number') and trx.user.whatsapp_number:
                message = (
                    f"🎉 Pembayaran paket *{trx.package.name}* Seharga *Rp.{trx.package.price}* berhasil!\n\n"
                    f"📦 Kuota Anda bertambah *{trx.package.quota_amount}*.\n"
                    f"💬 Terima kasih telah menggunakan layanan kami."
                )

                send_whatsapp_direct(
                    device_key=settings.QUODS_DEVICE_KEY,
                    token=settings.QUODS_BEARER_TOKEN,
                    phone=trx.user.whatsapp_number,  # ✅ disesuaikan
                    message=message
                )

        return JsonResponse({"message": "Transaction & user status updated"})

    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Order ID not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@staff_member_required
def delete_transaction(request, trx_id):
    trx = get_object_or_404(Transaction, id=trx_id)
    trx.delete()
    return redirect(reverse('dashboard'))

@login_required
def seo_analysis_history_view(request):
    analyses = SeoAnalysis.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(analyses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/seo_analysis_history.html', {
        'page_obj': page_obj,
    })

@login_required
def seo_analysis_detail_view(request, analysis_id):
    analysis = get_object_or_404(SeoAnalysis, id=analysis_id, user=request.user)
    return render(request, 'core/seo_analysis_detail.html', {
        'analysis': analysis,
    })



@login_required
@staff_member_required
def toggle_api_config_view(request, config_id):
    """View untuk toggle status aktif/nonaktif API"""
    if request.method == 'POST':
        try:
            api_config = ApiConfig.objects.get(id=config_id)
            api_config.is_active = not api_config.is_active
            api_config.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Status API {api_config.get_api_name_display()} berhasil diubah'
            })
        except ApiConfig.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Konfigurasi API tidak ditemukan'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error mengubah status API: {e}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Method tidak diizinkan'
    })

@login_required
@staff_member_required
def update_api_config_ajax(request, config_id):
    """View untuk update API config via AJAX"""
    print(f"=== update_api_config_ajax called ===")
    print(f"config_id: {config_id}")
    print(f"Request method: {request.method}")
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"User is staff: {request.user.is_staff}")
    print(f"User is superuser: {request.user.is_superuser}")
    print(f"User: {request.user}")
    print(f"CSRF Token in headers: {request.headers.get('X-CSRFToken', 'Not found')}")
    print(f"CSRF Token in POST: {request.POST.get('csrfmiddlewaretoken', 'Not found')}")
    
    if request.method != 'POST':
        print("Method not allowed")
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
    
    try:
        config = ApiConfig.objects.get(id=config_id)
        print(f"Found config: {config}")
        print(f"POST data: {request.POST}")
        
        # Update fields
        config.api_key = request.POST.get('api_key', config.api_key)
        config.base_url = request.POST.get('base_url', config.base_url)
        config.max_results = int(request.POST.get('max_results', config.max_results))
        config.timeout = int(request.POST.get('timeout', config.timeout))
        config.description = request.POST.get('description', config.description)
        # Always set is_active to True
        config.is_active = True
        
        config.save()
        print("Config saved successfully")
        
        return JsonResponse({
            'success': True,
            'message': f'API configuration {config.get_api_name_display()} updated successfully'
        })
        
    except ApiConfig.DoesNotExist:
        print(f"ApiConfig with id {config_id} not found")
        return JsonResponse({'success': False, 'error': 'API configuration not found'})
    except ValueError as e:
        print(f"ValueError: {e}")
        return JsonResponse({'success': False, 'error': f'Invalid value: {str(e)}'})
    except Exception as e:
        print(f"Exception: {e}")
        return JsonResponse({'success': False, 'error': f'Error updating configuration: {str(e)}'})

@login_required
@staff_member_required
def test_api_config(request, config_id):
    """View untuk test API configuration dengan melakukan actual API call menggunakan logic search rank yang sama"""
    import time
    
    if request.method != 'POST':
        return JsonResponse({
            'success': False, 
            'error': 'Method not allowed',
            'message': 'Method tidak diizinkan',
            'status_code': 405,
            'response_time': 0
        }, status=405)
    
    # Check if user has permission
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False, 
            'error': 'Unauthorized',
            'message': 'Anda harus login terlebih dahulu',
            'status_code': 401,
            'response_time': 0
        }, status=401)
    
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({
            'success': False, 
            'error': 'Forbidden',
            'message': 'Anda tidak memiliki akses untuk melakukan test API',
            'status_code': 403,
            'response_time': 0
        }, status=403)
    
    try:
        config = ApiConfig.objects.get(id=config_id)
        
        # Test berdasarkan jenis API
        start_time = time.time()
        test_result = {
            'success': False,
            'message': '',
            'status_code': None,
            'response_time': 0,
            'ranks': [],
            'error': None
        }
        
        if config.api_name == 'serpapi':
            # Test SerpAPI dengan parameter yang sama seperti search rank
            # Keyword: "serp api", Domain: "serpapi.com", Region: Indonesia
            keyword = "serp api"
            domain = "serpapi.com"
            hl = "id"  # Bahasa Indonesia
            gl = "id"  # Region Indonesia
            google_domain = "google.co.id"  # Google Indonesia
            num = config.max_results if config.max_results else 10
            
            # Gunakan logic yang sama persis seperti get_ranks_serpapi
            params = {
                "engine": "google",
                "q": keyword,
                "google_domain": google_domain,
                "hl": hl,
                "gl": gl,
                "num": num,
                "api_key": config.api_key
            }
            
            # Setup retry strategy dengan exponential backoff
            retry_strategy = Retry(
                total=3,  # Maksimal 3 kali retry
                backoff_factor=1,  # Delay: 1s, 2s, 4s
                status_forcelist=[429, 500, 502, 503, 504],  # Retry untuk status code ini
                allowed_methods=["GET"]
            )
            
            # Setup HTTPAdapter dengan retry strategy
            adapter = HTTPAdapter(max_retries=retry_strategy)
            
            # Buat session untuk connection pooling
            session = requests.Session()
            session.mount("https://", adapter)
            session.mount("http://", adapter)
            
            # Set headers untuk menghindari connection issues
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Connection': 'keep-alive'
            }
            
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    response = session.get(
                        config.base_url, 
                        params=params, 
                        timeout=config.timeout,
                        headers=headers
                    )
                    
                    response_time = round((time.time() - start_time) * 1000, 2)  # dalam milliseconds
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                        except json.JSONDecodeError as e:
                            test_result['message'] = 'API test gagal: Format response tidak valid'
                            test_result['response_time'] = response_time
                            test_result['error'] = f'JSON decode error: {str(e)}'
                            break
                        
                        # Check for error in response
                        if "error" in data:
                            test_result['message'] = f'API test gagal: Error dari SerpAPI'
                            test_result['response_time'] = response_time
                            test_result['error'] = data.get('error', 'Unknown error')
                            break
                        
                        # Gunakan logic yang sama persis seperti get_ranks_serpapi
                        ranks = []
                        if "organic_results" in data:
                            for idx, result in enumerate(data["organic_results"]):
                                link = result.get("link", "")
                                if domain in link:
                                    ranks.append({
                                        "position": idx + 1,
                                        "link": link
                                    })
                        
                        test_result['success'] = True
                        if len(ranks) > 0:
                            test_result['message'] = f'API test berhasil! Koneksi dan konfigurasi API benar. Domain ditemukan di {len(ranks)} posisi.'
                        else:
                            test_result['message'] = 'API test berhasil! Koneksi dan konfigurasi API benar. Namun domain tidak ditemukan di hasil pencarian.'
                        test_result['response_time'] = response_time
                        test_result['ranks'] = ranks
                        break  # Berhasil, keluar dari loop
                    else:
                        response_time = round((time.time() - start_time) * 1000, 2)
                        test_result['message'] = f'API test gagal dengan status code {response.status_code}'
                        test_result['status_code'] = response.status_code
                        test_result['response_time'] = response_time
                        try:
                            test_result['error'] = response.text[:500] if hasattr(response, 'text') else 'No error details available'
                        except:
                            test_result['error'] = 'No error details available'
                        break
                        
                except requests.exceptions.ConnectionError as e:
                    retry_count += 1
                    error_detail = str(e)
                    
                    # Handle ConnectionResetError (10054) specifically
                    if "10054" in error_detail or "Connection aborted" in error_detail or "forcibly closed" in error_detail:
                        if retry_count < max_retries:
                            wait_time = 2 ** retry_count
                            time.sleep(wait_time)
                            continue
                        else:
                            response_time = round((time.time() - start_time) * 1000, 2)
                            test_result['message'] = f'API test gagal: Koneksi ditutup paksa oleh server setelah {max_retries} percobaan'
                            test_result['response_time'] = response_time
                            test_result['error'] = f'Connection reset by remote host (10054): {str(e)}'
                            break
                    else:
                        if retry_count >= max_retries:
                            response_time = round((time.time() - start_time) * 1000, 2)
                            test_result['message'] = 'API test gagal: Error koneksi'
                            test_result['response_time'] = response_time
                            test_result['error'] = str(e)
                            break
                        else:
                            wait_time = 2 ** retry_count
                            time.sleep(wait_time)
                            continue
                            
                except requests.exceptions.Timeout:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count
                        time.sleep(wait_time)
                        continue
                    else:
                        response_time = round((time.time() - start_time) * 1000, 2)
                        test_result['message'] = f'API test timeout setelah {max_retries} percobaan'
                        test_result['response_time'] = response_time
                        test_result['error'] = 'Request timeout - API tidak merespon dalam waktu yang ditentukan'
                        break
                        
                except requests.RequestException as e:
                    response_time = round((time.time() - start_time) * 1000, 2)
                    test_result['message'] = 'API test gagal: Error koneksi'
                    test_result['response_time'] = response_time
                    test_result['error'] = str(e)
                    break
                    
                except Exception as e:
                    response_time = round((time.time() - start_time) * 1000, 2)
                    test_result['message'] = 'API test gagal: Error tidak diketahui'
                    test_result['response_time'] = response_time
                    test_result['error'] = str(e)
                    break
        
        elif config.api_name == 'google_search':
            # Test Google Search API (jika diimplementasikan)
            response_time = round((time.time() - start_time) * 1000, 2)
            test_result['message'] = 'Google Search API test belum diimplementasikan'
            test_result['error'] = 'Fitur test untuk Google Search API belum tersedia'
            test_result['response_time'] = response_time
        
        elif config.api_name == 'bing_search':
            # Test Bing Search API (jika diimplementasikan)
            response_time = round((time.time() - start_time) * 1000, 2)
            test_result['message'] = 'Bing Search API test belum diimplementasikan'
            test_result['error'] = 'Fitur test untuk Bing Search API belum tersedia'
            test_result['response_time'] = response_time
        
        else:
            response_time = round((time.time() - start_time) * 1000, 2)
            test_result['message'] = 'Jenis API tidak dikenal'
            test_result['error'] = f'API type "{config.api_name}" tidak didukung untuk test'
            test_result['response_time'] = response_time
        
        return JsonResponse(test_result)
        
    except ApiConfig.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'error': 'API configuration not found',
            'message': 'Konfigurasi API tidak ditemukan',
            'status_code': 404,
            'response_time': 0
        }, status=404)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in test_api_config: {error_trace}")
        response_time = round((time.time() - start_time) * 1000, 2) if 'start_time' in locals() else 0
        return JsonResponse({
            'success': False, 
            'error': str(e),
            'message': f'Error saat testing API: {str(e)}',
            'status_code': 500,
            'response_time': response_time
        }, status=500)
