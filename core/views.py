from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import CustomUser, RankResult, Billing, UserStatus, QuotaPurchase, QuotaPackage
from django.contrib.auth import get_user_model
from django.db.models import Count
from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuotaPurchaseForm
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.utils import timezone
from django.db.models.functions import TruncDate
from datetime import timedelta





import random
import requests
import json




def landing_page(request):
    return render(request, 'core/landing.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            # Autentikasi berhasil → langsung login & ke dashboard
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
            device_key='UMSZSzMyen40UdD',
            token='TMeTyUimv75LmlHRlCutowWU2z86QW',
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
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.role == 'admin' or request.user.is_superuser:
        # 7 hari terakhir
        seven_days_ago = timezone.now() - timedelta(days=6)

        rank_per_day = (
            RankResult.objects
            .filter(checked_at__date__gte=seven_days_ago.date())
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

        return render(request, 'core/search_rank.html', {
            # 'result': None,
            # 'history': history,
            # 'user_status': user_status,
            # 'used_quota': used_quota,
            # 'total_quota': total_quota,
            # 'sisa_quota': sisa_kuota
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
        return render(request, 'core/dashboard_users.html', {
            'users': CustomUser.objects.all().order_by('-date_joined')
        })

    elif section == 'billing':
        billing_data = QuotaPurchase.objects.select_related('user', 'package').order_by('-created_at')
        
        return render(request, 'core/dashboard_billing_quota.html', {
            'billing_users': billing_data
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
        return redirect('dashboard')

    return render(request, 'core/update_user.html', {'user_obj': user_obj})

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
            device_key='UMSZSzMyen40UdD',
            token='TMeTyUimv75LmlHRlCutowWU2z86QW',
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
    api_key = "572db24d1b3554570e4013212f0b26160f44709c398abb0a65dee3428e1ed4e6"
    params = {
        "engine": "google",
        "q": keyword,
        "google_domain": google_domain,
        "hl": hl,
        "gl": gl,
        "num": num,
        "api_key": api_key
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

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

        # Request ke SerpAPI
        api_key = "572db24d1b3554570e4013212f0b26160f44709c398abb0a65dee3428e1ed4e6"
        params = {
            "engine": "google",
            "q": keyword,
            "google_domain": google_domain,
            "hl": hl,
            "gl": gl,
            "num": num,
            "api_key": api_key
        }

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

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

    return render(request, 'core/search_rank.html', {
        "result": result_data,
        "history": history
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
    results = RankResult.objects.filter(
        user=request.user,
        keyword=keyword,
        domain=domain
    ).order_by('checked_at')

    grouped_data = defaultdict(list)
    for r in results:
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

    context = {
        'results': results,
        'keyword': keyword,
        'domain': domain,
        'dates': json.dumps(all_labels),
        'datasets': json.dumps(datasets)
    }

    return render(request, 'core/history_detail.html', context)

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
    packages = QuotaPackage.objects.all()
    return render(request, 'core/buy_quota.html', {'packages': packages})


@login_required
def upload_payment_proof_view(request, package_id):
    package = get_object_or_404(QuotaPackage, id=package_id)

    if request.method == 'POST':
        form = QuotaPurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.package = package
            purchase.status = 'pending'
            purchase.save()
            messages.success(
                request, 'Bukti pembayaran berhasil diunggah. Tunggu konfirmasi admin.'
            )
            return redirect('purchase_status')  # atau 'dashboard' jika itu tujuanmu
    else:
        form = QuotaPurchaseForm()

    return render(request, 'core/upload_payment.html', {
        'form': form,
        'package': package,
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
    except QuotaPurchase.DoesNotExist:
        pass

    return redirect('dashboard')

@login_required
def reject_quota(request, purchase_id):
    if not request.user.is_superuser and request.user.role != 'admin':
        return redirect('dashboard')

    try:
        purchase = QuotaPurchase.objects.get(id=purchase_id)
        purchase.status = 'rejected'
        purchase.save()
    except QuotaPurchase.DoesNotExist:
        pass

    return redirect('dashboard')