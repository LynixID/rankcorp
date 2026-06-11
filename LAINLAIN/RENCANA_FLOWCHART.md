# RENCANA FLOWCHART DIAGRAM - SISTEM RANK CHECKER

## ANALISIS SISTEM

Berdasarkan analisis menyeluruh sistem, flowchart akan fokus pada **algoritma dan logika proses** yang kompleks, berbeda dengan Activity Diagram yang fokus pada interaksi antar aktor.

---

## FLOWCHART YANG AKAN DIBUAT

### 1. **FLOWCHART: PROSES REGISTRASI & VERIFIKASI OTP**
**Fokus**: Algoritma validasi data, generate OTP, dan verifikasi

**Alur Proses**:
- START
- Input: username, email, whatsapp, password, confirm_password
- Validasi: Username sudah digunakan? → Ya: Error, END | Tidak: Lanjut
- Validasi: Email sudah digunakan? → Ya: Error, END | Tidak: Lanjut
- Validasi: Format WhatsApp (startswith '62')? → Tidak: Error, END | Ya: Lanjut
- Validasi: password == confirm_password? → Tidak: Error, END | Ya: Lanjut
- Generate OTP: random(100000-999999)
- Simpan data ke session (pending_user)
- Kirim OTP via WhatsApp API
- Input: OTP dari user
- Verifikasi: input_otp == session OTP? → Tidak: Error, ulang input | Ya: Lanjut
- Cek: User sudah ada? → Ya: Warning, redirect login | Tidak: Lanjut
- Buat User baru
- Buat UserStatus (status='guest', total_quota=3, used_quota=0)
- Hapus session
- Redirect ke login
- END

**Kriteria**: ✅ Algoritma validasi kompleks, decision points banyak, penting untuk keamanan

---

### 2. **FLOWCHART: ALGORITMA CEK RANK & PENCARIAN DOMAIN**
**Fokus**: Algoritma pencarian domain di hasil SerpAPI dengan loop iterasi

**Alur Proses**:
- START
- Input: keyword, domain, hl, gl, google_domain, num
- Cek: UserStatus ada? → Tidak: Error, END | Ya: Lanjut
- Cek: remaining_quota > 0? → Tidak: Error, END | Ya: Lanjut
- Ambil konfigurasi SerpAPI dari database (atau fallback)
- Build params: engine, q, google_domain, hl, gl, num, api_key
- Request GET ke SerpAPI
- Cek: Response sukses? → Tidak: Error, END | Ya: Lanjut
- Parse JSON response
- Inisialisasi: ranks = []
- Cek: "organic_results" ada? → Tidak: Return ranks (kosong) | Ya: Lanjut
- **LOOP**: For idx, result in enumerate(organic_results):
  - Ambil link dari result
  - Cek: domain in link? → Ya: Append {position: idx+1, link} ke ranks, Simpan RankResult ke DB | Tidak: Skip
- Update: used_quota += 1
- Return result_data (domain, keyword, total_found, ranks)
- END

**Kriteria**: ✅ Algoritma loop kompleks, iterasi data, pencarian pattern matching, core functionality

---

### 3. **FLOWCHART: ALGORITMA ANALISIS TREND RANKING**
**Fokus**: Perhitungan trend, stability, dan average rank dari rank history

**Alur Proses**:
- START
- Input: rank_history (array of {date, rank, url})
- Inisialisasi: trend = "tidak cukup data", stability = "tidak cukup data"
- Cek: len(rank_history) >= 2? → Tidak: avg_rank = rank_history[0]['rank'], Return | Ya: Lanjut
- Hitung: first_rank = rank_history[0]['rank']
- Hitung: last_rank = rank_history[-1]['rank']
- Hitung: rank_change = first_rank - last_rank
- Decision: rank_change > 0? → Ya: trend = "meningkat" | Tidak: Lanjut
- Decision: rank_change < 0? → Ya: trend = "menurun" | Tidak: trend = "stabil"
- Hitung: avg_rank = sum(rank_history[i]['rank']) / len(rank_history)
- **LOOP**: Hitung variance
  - rank_variance = sum((rank_history[i]['rank'] - avg_rank)²) / len(rank_history)
- Decision: rank_variance < 5? → Ya: stability = "stabil" | Tidak: stability = "fluktuatif"
- Return: {trend, stability, avg_rank}
- END

**Kriteria**: ✅ Algoritma statistik, perhitungan matematis, decision logic, penting untuk SEO Analysis

---

### 4. **FLOWCHART: ALGORITMA VALIDASI & PENGURANGAN KUOTA**
**Fokus**: Logika validasi kuota dan pengurangan kuota untuk berbagai aksi

**Alur Proses**:
- START
- Input: user, action_type, quota_cost
- Cek: UserStatus exists? → Tidak: Error, END | Ya: Lanjut
- Ambil: user_status = UserStatus.objects.get(user=user)
- Hitung: remaining = user_status.total_quota - user_status.used_quota
- Cek: remaining >= quota_cost? → Tidak: Error "Kuota tidak cukup", END | Ya: Lanjut
- Update: user_status.used_quota += quota_cost
- Save: user_status.save()
- Return: Success
- END

**Kriteria**: ✅ Business logic penting, validasi kritis, digunakan di banyak proses

---

### 5. **FLOWCHART: PROSES SEO ANALYSIS DENGAN AI**
**Fokus**: Algoritma routing model AI, perhitungan trend, dan call API

**Alur Proses**:
- START
- Input: keyword, domain, rank_history, model_choice
- Cek: UserStatus exists? → Tidak: Error, END | Ya: Lanjut
- Cek: status == 'premium'? → Tidak: Error "Premium only", END | Ya: Lanjut
- Validasi: keyword & domain ada? → Tidak: Error, END | Ya: Lanjut
- Validasi: model_choice valid? → Tidak: Error, END | Ya: Lanjut
- Ambil: model_config dari database
- Ambil: quota_cost dari model_config
- Cek: remaining_quota >= quota_cost? → Tidak: Error, END | Ya: Lanjut
- Hitung trend & stability (gunakan Flowchart #3)
- Build prompt dengan rank_history
- Decision: model_choice == "gemini"?
  - **Ya (Gemini)**:
    - URL = Gemini API endpoint
    - Headers = {X-goog-api-key: API_KEY}
    - Payload = {contents, generationConfig}
    - POST request ke Gemini API
  - **Tidak (OpenAI)**:
    - Decision: model_choice == "gpt-3.5-turbo"?
      - Ya: model = "gpt-3.5-turbo", max_tokens = 2500
      - Tidak: model = "gpt-4-1106-preview", max_tokens = 3000
    - URL = OpenAI API endpoint
    - Headers = {Authorization: Bearer API_KEY}
    - Payload = {model, messages, max_tokens, temperature}
    - POST request ke OpenAI API
- Cek: Response status == 200? → Tidak: Error, END | Ya: Lanjut
- Parse response (Gemini: candidates[0].content.parts[0].text | OpenAI: choices[0].message.content)
- Cek: analysis length > 50? → Tidak: Error, END | Ya: Lanjut
- Simpan: SeoAnalysis ke database
- Update: used_quota += quota_cost
- Return: {analysis, metadata}
- END

**Kriteria**: ✅ Algoritma routing kompleks, multiple API calls, decision branching, core feature premium

---

### 6. **FLOWCHART: PROSES PEMBELIAN KUOTA (MANUAL TRANSFER)**
**Fokus**: Algoritma checkout session management, upload bukti, dan approval flow

**Alur Proses**:
- START
- Input: package_id
- Cek: Active session exists? → Ya: Cek expired? → Tidak expired: Redirect upload | Expired: Lanjut | Tidak: Lanjut
- Ambil: package dari database
- Generate: session_id = UUID
- Hitung: expires_at = now + 2 hours
- Buat: CheckoutSession (user, package, session_id, expires_at, status='active')
- Redirect: Upload payment proof page
- Input: payment_proof (file)
- Validasi: Form valid? → Tidak: Error, ulang | Ya: Lanjut
- Buat: QuotaPurchase (user, package, payment_proof, status='pending')
- Update: CheckoutSession.status = 'completed'
- Return: Success message
- **ADMIN APPROVAL**:
  - Admin: Approve purchase
  - Update: QuotaPurchase.status = 'approved'
  - Ambil/Create: UserStatus
  - Update: total_quota += package.quota_amount
  - Update: status = 'premium' (jika belum)
  - Save: UserStatus
  - Return: Success
- END

**Kriteria**: ✅ Session management, state management, approval workflow, business logic penting

---

### 7. **FLOWCHART: PROSES PAYMENT CALLBACK (MIDTRANS)**
**Fokus**: Algoritma handling callback dari Midtrans, update status, dan notifikasi

**Alur Proses**:
- START
- Input: callback_data (JSON dari Midtrans)
- Parse: order_id, transaction_status, payment_type
- Cek: Transaction exists? → Tidak: Error 404, END | Ya: Lanjut
- Ambil: trx = Transaction.objects.get(order_id=order_id)
- Update: trx.transaction_status = status
- Update: trx.payment_type = payment_type
- Save: trx.save()
- Cek: status == "settlement"? → Tidak: Return success | Ya: Lanjut
- Ambil/Create: UserStatus
- Update: total_quota += trx.package.quota_amount
- Update: status = 'premium'
- Save: UserStatus
- Cek: User has WhatsApp? → Ya: Kirim notifikasi WhatsApp | Tidak: Skip
- Return: JSON success response
- END

**Kriteria**: ✅ Webhook handling, state update, notifikasi, integrasi payment gateway

---

## REKOMENDASI UNTUK LAPORAN

### **PRIORITAS TINGGI (WAJIB - 4 Flowchart)**:
1. ✅ **Flowchart Registrasi & Verifikasi OTP** - Proses autentikasi penting
2. ✅ **Flowchart Cek Rank & Pencarian Domain** - Core functionality sistem
3. ✅ **Flowchart Analisis Trend Ranking** - Algoritma statistik penting
4. ✅ **Flowchart SEO Analysis dengan AI** - Feature premium, algoritma kompleks

### **PRIORITAS MENENGAH (DISARANKAN - 2 Flowchart)**:
5. ✅ **Flowchart Validasi & Pengurangan Kuota** - Business logic kritis
6. ✅ **Flowchart Pembelian Kuota (Manual)** - Workflow pembayaran

### **PRIORITAS RENDAH (OPSIONAL - 1 Flowchart)**:
7. ⚠️ **Flowchart Payment Callback (Midtrans)** - Bisa digabung dengan #6 atau dijelaskan singkat

---

## FORMAT FLOWCHART

### **Simbol Standar**:
- **Oval**: Start/End
- **Rectangle**: Process/Action
- **Diamond**: Decision/Condition
- **Parallelogram**: Input/Output
- **Arrow**: Flow direction

### **Karakteristik**:
- **Vertikal** (top to bottom)
- **Ringkas & Efisien**: Fokus pada algoritma, tidak terlalu detail UI
- **Akurat**: Sesuai dengan kode aktual di views.py
- **Padat**: Menggabungkan proses terkait, menghindari redundansi

### **Teknologi**:
- Menggunakan **Mermaid.js** (sama seperti Activity Diagram)
- Format: `flowchart TD` (Top Down)
- Export PNG dengan margin 50px

---

## STATISTIK RENCANA

- **Total Flowchart**: 7 diagram
- **Prioritas Tinggi**: 4 diagram (wajib)
- **Prioritas Menengah**: 2 diagram (disarankan)
- **Prioritas Rendah**: 1 diagram (opsional)

---

## CATATAN PENTING

1. **Flowchart berbeda dengan Activity Diagram**:
   - Flowchart: Fokus algoritma/logika, decision points, loop
   - Activity Diagram: Fokus interaksi aktor, swimlanes

2. **Tidak perlu membuat flowchart untuk**:
   - Proses sederhana (Login, Logout)
   - CRUD operations sederhana
   - Proses yang sudah jelas dari Activity Diagram

3. **Fokus pada**:
   - Algoritma kompleks dengan loop
   - Decision logic yang banyak
   - Business logic penting
   - Integrasi dengan API eksternal

---

## IMPLEMENTASI

Setiap flowchart akan dibuat dalam file HTML terpisah dengan:
- Diagram Mermaid.js yang akurat
- Penjelasan singkat setelah diagram
- Tombol export PNG dengan margin 50px
- Styling konsisten dengan Activity Diagram

