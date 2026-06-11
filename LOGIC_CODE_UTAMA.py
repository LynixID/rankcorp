"""
================================================================================
DOKUMENTASI LOGIC CODE UTAMA - SISTEM RANK CHECKER (U-RANK)
File ini berisi LOGIC UTAMA/CORE dari sistem, fokus pada fitur bisnis inti
================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import CustomUser, RankResult, UserStatus, QuotaPurchase, QuotaPackage, Transaction, SeoAnalysis, AiModelConfig, ApiConfig, CheckoutSession
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.forms import QuotaPurchaseForm
import random
import requests
import json
import midtransclient
import uuid
from datetime import timedelta


# ====================================================================================
# ====================================================================================
# A. AUTHENTICATION & REGISTRATION (4 Logic Utama)
# ====================================================================================
# ====================================================================================

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 1: Generate OTP 6 Digit
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def generate_otp():
    """
    Fungsi untuk generate OTP 6 digit secara random
    Returns: String OTP 6 digit (100000-999999)
    """
    return str(random.randint(100000, 999999))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 2: Register View dengan Validasi Lengkap
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def register_view(request):    
    """
    Logic registrasi user baru dengan validasi lengkap:
    - Validasi username unique
    - Validasi email unique
    - Validasi format WhatsApp (harus mulai dengan 62)
    - Validasi password confirmation
    - Generate OTP dan simpan ke session
    - Kirim OTP via WhatsApp
    """
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

        # Validasi email sudah digunakan
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 3: Verifikasi OTP dan Create User Baru
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def verify_otp_view(request):
    """
    Logic verifikasi OTP:
    - Validasi session pending_user
    - Cek OTP yang diinput dengan OTP di session
    - Cegah duplikasi user
    - Create user baru dengan role 'user'
    - Create UserStatus dengan status 'guest' dan 3 kuota gratis
    - Hapus session pending_user
    """
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

            # Tambahkan entri ke UserStatus dengan 3 kuota gratis
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 4: Login View
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def login_view(request):
    """
    Logic login user:
    - Cek jika user sudah login → redirect ke dashboard
    - Authenticate username dan password
    - Jika valid → login dan redirect ke dashboard
    - Jika tidak valid → error message
    """
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


# ====================================================================================
# ====================================================================================
# B. CEK RANKING (2 Logic Utama)
# ====================================================================================
# ====================================================================================

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 5: Get Ranks dari SerpAPI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_ranks_serpapi(keyword, domain, hl, gl, google_domain, num):
    """
    Logic untuk mengambil ranking dari SerpAPI:
    - Ambil konfigurasi SerpAPI dari database (ApiConfig)
    - Fallback ke hardcoded jika tidak ada di database
    - Request GET ke SerpAPI dengan parameter lengkap
    - Parse JSON response
    - Filter domain di organic_results dengan loop
    - Return list ranks dengan position dan link
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
    
    try:
        response = requests.get(base_url, params=params, timeout=timeout)
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
    except requests.RequestException as e:
        print(f"Error request SerpAPI: {e}")
        return []
    except Exception as e:
        print(f"Error parsing SerpAPI response: {e}")
        return []


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 6: Check Rank View - Proses Pengecekan Ranking Utama
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@login_required
def check_rank_view(request):
    """
    Logic utama untuk pengecekan ranking:
    - Validasi UserStatus ada
    - Cek remaining_quota > 0
    - Ambil parameter dari form (domain, keyword, hl, gl, google_domain, num)
    - Request ke SerpAPI menggunakan konfigurasi dari database
    - Parse hasil dan simpan setiap rank ke database (RankResult)
    - Kurangi kuota user (used_quota += 1) jika hasil ditemukan
    - Return hasil dan histori
    """
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

        try:
            response = requests.get(base_url, params=params, timeout=timeout)
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

    # Histori juga ditampilkan
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


# ====================================================================================
# ====================================================================================
# C. SEO ANALYSIS DENGAN AI (1 Logic Utama)
# ====================================================================================
# ====================================================================================

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 7: SEO Analysis dengan AI (Gemini/OpenAI)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@csrf_exempt
@login_required
def seo_analysis(request):
    """
    Logic utama untuk analisis SEO dengan AI:
    - Validasi status premium user
    - Validasi data input (keyword, domain, rank_history, model)
    - Validasi model choice (gemini, gpt-3.5-turbo, gpt-4-1106-preview)
    - Hitung quota_cost berdasarkan model yang dipilih
    - Cek kuota cukup untuk analisis
    - Analisis trend & stability dari rank_history
    - Build prompt SEO yang disesuaikan berdasarkan model
    - Routing ke Gemini API atau OpenAI API
    - Parse response dan simpan ke SeoAnalysis database
    - Kurangi kuota sesuai quota_cost
    - Return JSON response dengan analysis dan metadata
    """
    if request.method == "POST":
        # Cek status premium user
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
1. **RINGKASAN SINGKAT** (2-3 kalimat)
2. **ANALISIS TREN** (detail)
3. **PENYEBAB KEMUNGKINAN**
4. **REKOMENDASI KONKRIT** (minimal 3)
5. **TARGET & MONITORING**
"""
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
            
            gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
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
                                # Kurangi kuota
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
1. **RINGKASAN SINGKAT** (2-3 kalimat)
2. **ANALISIS TREN** (detail)
3. **PENYEBAB KEMUNGKINAN**
4. **REKOMENDASI KONKRIT** (minimal 3)
5. **TARGET & MONITORING**
"""
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
                            # Kurangi kuota
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
            except Exception as e:
                return JsonResponse({
                    "error": "Unexpected Error",
                    "message": f"Terjadi kesalahan tidak terduga: {str(e)}"
                }, status=500)


# ====================================================================================
# ====================================================================================
# D. SISTEM KUOTA (3 Logic Utama)
# ====================================================================================
# ====================================================================================

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 8: Model Method - Remaining Quota Calculation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Method ini ada di models.py - UserStatus class
def remaining_quota(self):
    """
    Method di UserStatus model:
    Menghitung sisa kuota = total_quota - used_quota
    Returns: Integer sisa kuota
    """
    return self.total_quota - self.used_quota


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 9: Approve Quota Purchase (Admin)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@login_required
def approve_quota(request, purchase_id):
    """
    Logic untuk approve pembayaran kuota (transfer bank manual):
    - Validasi admin permission
    - Get QuotaPurchase berdasarkan purchase_id
    - Update status menjadi 'approved'
    - Tambahkan kuota ke UserStatus (total_quota += package.quota_amount)
    - Save UserStatus
    """
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

        messages.success(request, f"Pembayaran paket '{purchase.package.name}' dari {purchase.user.username} berhasil disetujui.")
        return redirect('dashboard')

    except QuotaPurchase.DoesNotExist:
        messages.error(request, "Pembelian kuota tidak ditemukan.")
        return redirect('dashboard')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 10: Payment Notification Callback (Midtrans - Auto Approve)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@csrf_exempt
def payment_notification(request):
    """
    Logic callback dari Midtrans (auto-approve pembayaran):
    - Parse JSON data dari request body
    - Get Transaction berdasarkan order_id
    - Update transaction_status dan payment_type
    - Jika status = 'settlement' (pembayaran berhasil):
        * Get atau create UserStatus
        * Tambahkan kuota (total_quota += package.quota_amount)
        * Update status menjadi 'premium' (auto upgrade)
        * Kirim WhatsApp notifikasi ke user
    - Return JSON response
    """
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
            # Update kuota dan status user
            user_status, _ = UserStatus.objects.get_or_create(id=trx.user)
            user_status.total_quota += trx.package.quota_amount
            user_status.status = "premium"  # Auto upgrade ke premium
            user_status.save()

            # Kirim WhatsApp ke nomor user
            if hasattr(trx.user, 'whatsapp_number') and trx.user.whatsapp_number:
                message = (
                    f"🎉 Pembayaran paket *{trx.package.name}* Seharga *Rp.{trx.package.price}* berhasil!\n\n"
                    f"📦 Kuota Anda bertambah *{trx.package.quota_amount}*.\n"
                    f"💬 Terima kasih telah menggunakan layanan kami."
                )

                send_whatsapp_direct(
                    device_key=settings.QUODS_DEVICE_KEY,
                    token=settings.QUODS_BEARER_TOKEN,
                    phone=trx.user.whatsapp_number,
                    message=message
                )

        return JsonResponse({"message": "Transaction & user status updated"})

    except Transaction.DoesNotExist:
        return JsonResponse({"error": "Order ID not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ====================================================================================
# ====================================================================================
# E. PAYMENT & CHECKOUT (3 Logic Utama)
# ====================================================================================
# ====================================================================================

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 11: Create Checkout Session (Transfer Bank Manual)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@login_required
def create_checkout_session(request, package_id):
    """
    Logic untuk membuat checkout session (transfer bank manual):
    - Get QuotaPackage berdasarkan package_id
    - Cek apakah user sudah punya session aktif
    - Jika ada session aktif dan belum expired → redirect ke upload page
    - Jika session expired → update status menjadi 'expired'
    - Generate session_id dengan UUID
    - Set expires_at = now + 2 jam
    - Create CheckoutSession dengan status 'active'
    """
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 12: Upload Payment Proof (Transfer Bank Manual)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@login_required
def upload_payment_proof_view(request, package_id):
    """
    Logic untuk upload bukti pembayaran:
    - Get QuotaPackage berdasarkan package_id
    - Cek CheckoutSession aktif untuk user dan package
    - Validasi session tidak expired
    - Jika POST: validasi form, simpan QuotaPurchase dengan status 'pending'
    - Update CheckoutSession status menjadi 'completed'
    """
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 13: Start Payment Midtrans
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def start_payment(request, package_id):
    """
    Logic untuk memulai pembayaran Midtrans:
    - Get QuotaPackage berdasarkan package_id
    - Generate order_id dengan UUID
    - Create Transaction record dengan status 'pending'
    - Initialize Midtrans Snap client
    - Build transaction payload
    - Generate Snap token
    - Return JSON dengan snap_token dan client_key
    """
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


# ====================================================================================
# ====================================================================================
# F. WHATSAPP INTEGRATION (1 Logic Utama)
# ====================================================================================
# ====================================================================================

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGIC UTAMA 14: Send WhatsApp Direct (OTP & Notifikasi)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def send_whatsapp_direct(device_key, token, phone, message, file_url=None):
    """
    Logic untuk mengirim pesan WhatsApp via Quods API:
    - Build API URL dan headers dengan Bearer token
    - Build payload dengan device_key, phone, message
    - Jika ada file_url → tambahkan ke payload
    - POST request ke Quods API
    - Handle response dan error
    - Return result JSON atau None jika error
    Digunakan untuk: Kirim OTP registrasi, notifikasi pembayaran sukses
    """
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


"""
================================================================================
END OF DOCUMENTATION - LOGIC UTAMA
Total Logic Utama: 14 Logic

RINGKASAN LOGIC UTAMA:
A. Authentication & Registration: 4 Logic (Generate OTP, Register, Verify OTP, Login)
B. Cek Ranking: 2 Logic (Get Ranks SerpAPI, Check Rank View)
C. SEO Analysis: 1 Logic (SEO Analysis dengan AI)
D. Sistem Kuota: 3 Logic (Remaining Quota, Approve Quota, Payment Notification)
E. Payment & Checkout: 3 Logic (Create Session, Upload Proof, Start Payment)
F. WhatsApp Integration: 1 Logic (Send WhatsApp Direct)

LOGIC YANG TIDAK TERMASUK (Supporting/Admin):
- Dashboard queries (hanya query data)
- Admin CRUD operations
- History views (hanya query & grouping)
- Toggle, delete operations (operasi sederhana)
- Dashboard section routing
================================================================================
"""

