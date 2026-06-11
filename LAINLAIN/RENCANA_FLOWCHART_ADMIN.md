# RENCANA DETAIL FLOWCHART ALUR ADMIN
## Sistem Rank Checker

---

## 📋 DAFTAR ISI

1. [Flowchart Utama (Entry Point Admin)](#1-flowchart-utama-entry-point-admin)
2. [Flowchart Dashboard Admin](#2-flowchart-dashboard-admin)
3. [Flowchart Manajemen User](#3-flowchart-manajemen-user)
4. [Flowchart Manajemen Pembayaran](#4-flowchart-manajemen-pembayaran)
5. [Flowchart Manajemen Paket Kuota](#5-flowchart-manajemen-paket-kuota)
6. [Flowchart Manajemen Transaksi](#6-flowchart-manajemen-transaksi)
7. [Flowchart Manajemen AI Model Config](#7-flowchart-manajemen-ai-model-config)
8. [Flowchart Manajemen API Config](#8-flowchart-manajemen-api-config)
9. [Struktur Visual & Notasi](#9-struktur-visual--notasi)

---

## 1. FLOWCHART UTAMA (ENTRY POINT ADMIN)

### Nama File: `FLOWCHART_ADMIN_MAIN.html`

### Alur:
```
START
  ↓
Admin Akses Sistem (/login)
  ↓
[Validasi Login]
  ↓ (Valid)
Cek Role User
  ↓ (role == 'admin' OR is_superuser == True)
Redirect ke Dashboard Admin (/dashboard)
  ↓
[Render Dashboard Admin]
  ↓
Admin Melihat Menu Dashboard:
  - Statistik Overview (cards)
  - Grafik Rank Checks (30 hari)
  - Recent Ranks (5 terakhir)
  - List Users (summary)
  - List Pembayaran Pending (summary)
  ↓
Admin Memilih Menu:
  ├─→ Dashboard Stats → [Flowchart 2a]
  ├─→ Manage Users → [Flowchart 3]
  ├─→ Manage Billing → [Flowchart 4]
  ├─→ Manage Quota Package → [Flowchart 5]
  ├─→ Manage Transaction → [Flowchart 6]
  ├─→ Manage AI Model Config → [Flowchart 7]
  ├─→ Manage API Config → [Flowchart 8]
  └─→ Logout → END
  ↓ (role != 'admin')
Redirect ke Dashboard User
  ↓
END
```

### Decision Points:
- **D1**: Apakah login valid? (Yes/No)
- **D2**: Apakah user role = admin atau superuser? (Yes/No)

### Proses Utama:
1. **Validasi Login**: Cek username & password
2. **Cek Role**: Verifikasi role admin atau superuser
3. **Load Dashboard**: 
   - Query statistik (total_users, total_pembayaran_sukses, total_rank, pending_billings)
   - Query grafik rank checks 30 hari terakhir (group by date, count)
   - Query recent ranks (5 terakhir dengan user info)
   - Query users list (all users, order by date_joined)
   - Query billing pending (QuotaPurchase dengan status='pending')

---

## 2. FLOWCHART DASHBOARD ADMIN

### 2a. Dashboard Overview Stats

### Nama File: `FLOWCHART_ADMIN_DASHBOARD_STATS.html`

### Alur:
```
START (dari Main Dashboard)
  ↓
Admin Klik "Statistik" atau akses /dashboard/section/stats
  ↓
[Validasi Akses]
  ↓ (Access Granted)
Query Database:
  - total_users = COUNT(CustomUser)
  - total_pembayaran_sukses = COUNT(QuotaPurchase WHERE status='approved')
  - total_rank = COUNT(RankResult)
  ↓
Render Template dashboard_stats.html
  ↓
Tampilkan Statistik Cards:
  ├─ Total Users
  ├─ Total Pembayaran Sukses
  └─ Total Rank Checks
  ↓
Admin Klik Back → Kembali ke Dashboard Main
  ↓
END
```

### 2b. Dashboard Grafik Rank Checks

### Nama File: `FLOWCHART_ADMIN_DASHBOARD_CHART.html`

### Alur:
```
START (dari Main Dashboard)
  ↓
Admin Melihat Grafik di Dashboard Main
  ↓
[Query Data 30 Hari Terakhir]
  ↓
Calculate:
  - thirty_days_ago = timezone.now() - timedelta(days=29)
  - Query RankResult WHERE checked_at >= thirty_days_ago
  - Group by DATE(checked_at)
  - COUNT(id) per hari
  ↓
Format Data untuk Chart.js:
  - dates[] = array tanggal (format: "YYYY-MM-DD")
  - counts[] = array jumlah checks per hari
  - datasets = [{label: "Jumlah Cek Harian", data: counts}]
  ↓
Render Chart.js di Dashboard
  ↓
Admin Bisa Interaksi:
  - Hover untuk detail
  - Zoom (jika diaktifkan)
  ↓
END
```

---

## 3. FLOWCHART MANAJEMEN USER

### Nama File: `FLOWCHART_ADMIN_MANAJEMEN_USER.html`

### Alur:
```
START (Admin klik "Manage Users" di Dashboard)
  ↓
Akses /dashboard/section/users
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query Users dari Database:
  - CustomUser.objects.all().order_by('-date_joined')
  - Pagination (10 per page)
  ↓
Render Template dashboard_users.html
  ↓
Tampilkan List Users (dengan Pagination):
  ├─ Username
  ├─ Email
  ├─ WhatsApp
  ├─ Role
  ├─ Date Joined
  ├─ Is Active
  └─ Actions (Edit, Delete, Activate/Deactivate)
  ↓
Admin Memilih Aksi:
  ├─→ Edit User → [Sub-flowchart 3a]
  ├─→ Delete User → [Sub-flowchart 3b]
  ├─→ Activate User → [Sub-flowchart 3c]
  ├─→ Deactivate User → [Sub-flowchart 3d]
  └─→ Back to Dashboard
  ↓
END
```

### 3a. Edit User

### Alur:
```
START (Admin klik "Edit" pada user)
  ↓
Akses /update-user/<user_id>/
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
[Method GET]
  ↓
Query User dari Database (get_object_or_404)
  ↓
Render Form Update User (update_user.html)
  ↓
Admin Mengisi Form:
  - Username (editable)
  - Email (editable)
  - WhatsApp (editable)
  - Role (dropdown: admin/user)
  ↓
Admin Submit Form
  ↓
[Method POST]
  ↓
[Validasi Input]
  ↓ (Valid)
Update User di Database:
  - user.username = POST['username']
  - user.email = POST['email']
  - user.whatsapp_number = POST['whatsapp']
  - user.role = POST['role']
  - user.save()
  ↓
Tampilkan Success Message
  ↓
Redirect ke Dashboard
  ↓
END
```

### 3b. Delete User

### Alur:
```
START (Admin klik "Delete" pada user)
  ↓
Akses /delete-user/<user_id>/
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query User dari Database (get_object_or_404)
  ↓
[Cascade Delete]
  ↓
Delete User:
  - CustomUser.objects.filter(id=user_id).delete()
  - (CASCADE: UserStatus, RankResult, QuotaPurchase, dll akan terhapus otomatis)
  ↓
Tampilkan Success Message: "User berhasil dihapus"
  ↓
Redirect ke Dashboard dengan ?section=users
  ↓
END
```

### 3c. Activate User

### Alur:
```
START (Admin klik "Activate" pada user)
  ↓
Akses /update-user-status/<user_id>/activate/
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query User dari Database (get_object_or_404)
  ↓
Update User Status:
  - user.is_active = True
  - user.save()
  ↓
Tampilkan Success Message: "{username} telah diaktifkan"
  ↓
Redirect ke Dashboard
  ↓
END
```

### 3d. Deactivate User

### Alur:
```
START (Admin klik "Deactivate" pada user)
  ↓
Akses /update-user-status/<user_id>/deactivate/
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query User dari Database (get_object_or_404)
  ↓
Update User Status:
  - user.is_active = False
  - user.save()
  ↓
Tampilkan Success Message: "{username} telah dinonaktifkan"
  ↓
Redirect ke Dashboard
  ↓
END
```

---

## 4. FLOWCHART MANAJEMEN PEMBAYARAN

### Nama File: `FLOWCHART_ADMIN_MANAJEMEN_PEMBAYARAN.html`

### Alur:
```
START (Admin klik "Manage Billing" di Dashboard)
  ↓
Akses /dashboard/section/billing
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query QuotaPurchase dari Database:
  - QuotaPurchase.objects.select_related('user', 'package')
  - Order by status, created_at
  - Pagination (10 per page)
  ↓
Render Template dashboard_billing_quota.html
  ↓
Tampilkan List Pembayaran:
  ├─ User Info (username, email)
  ├─ Package Info (name, price, quota_amount)
  ├─ Payment Proof (gambar)
  ├─ Status (pending/approved/rejected)
  ├─ Created At
  └─ Actions (Approve, Reject, View Detail)
  ↓
Admin Memilih Aksi:
  ├─→ Approve Pembayaran → [Sub-flowchart 4a]
  ├─→ Reject Pembayaran → [Sub-flowchart 4b]
  └─→ Back to Dashboard
  ↓
END
```

### 4a. Approve Pembayaran

### Alur:
```
START (Admin klik "Approve" pada pembayaran)
  ↓
Akses /approve-quota/<purchase_id>/
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query QuotaPurchase dari Database (get_object_or_404)
  ↓
Update Status Pembayaran:
  - purchase.status = 'approved'
  - purchase.save()
  ↓
Update UserStatus:
  - user_status = UserStatus.objects.get_or_create(id=purchase.user)
  - user_status.total_quota += purchase.package.quota_amount
  - (Jika belum ada UserStatus, create dengan default values)
  - user_status.save()
  ↓
[Opsional: Auto Upgrade ke Premium jika kuota cukup]
  ↓
Tampilkan Success Message: "Pembayaran paket '{package.name}' dari {username} berhasil disetujui"
  ↓
Redirect ke Dashboard
  ↓
END
```

### 4b. Reject Pembayaran

### Alur:
```
START (Admin klik "Reject" pada pembayaran)
  ↓
Akses /reject-quota/<purchase_id>/
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query QuotaPurchase dari Database (get_object_or_404)
  ↓
Update Status Pembayaran:
  - purchase.status = 'rejected'
  - purchase.save()
  ↓
[Note: Kuota TIDAK ditambahkan ke user]
  ↓
Tampilkan Success Message: "Pembayaran paket '{package.name}' dari {username} berhasil ditolak"
  ↓
Redirect ke Dashboard
  ↓
END
```

### 4c. View Payment Detail (Opsional Enhancement)

### Alur:
```
START (Admin klik "View Detail" pada pembayaran)
  ↓
Tampilkan Modal atau Page dengan Detail:
  ├─ User Info Lengkap
  ├─ Package Info Lengkap
  ├─ Payment Proof (full size image)
  ├─ Transaction Info
  └─ History Status Changes
  ↓
Admin Bisa:
  ├─ Approve dari detail
  ├─ Reject dari detail
  └─ Close detail
  ↓
END
```

---

## 5. FLOWCHART MANAJEMEN PAKET KUOTA

### Nama File: `FLOWCHART_ADMIN_MANAJEMEN_PAKET_KUOTA.html`

### Alur:
```
START (Admin klik "Manage Quota Package" di Dashboard)
  ↓
Akses /dashboard/section/quotapackage
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query QuotaPackage dari Database:
  - QuotaPackage.objects.all().order_by('id')
  - Pagination (10 per page)
  ↓
Render Template dashboard_quotapackage.html
  ↓
Tampilkan List Paket:
  ├─ Package Name
  ├─ Price (format: Rp)
  ├─ Quota Amount
  └─ Actions (Edit, Delete)
  ↓
Admin Memilih Aksi:
  ├─→ Add New Package → [Sub-flowchart 5a]
  ├─→ Edit Package → [Sub-flowchart 5b]
  ├─→ Delete Package → [Sub-flowchart 5c]
  └─→ Back to Dashboard
  ↓
END
```

### 5a. Add New Package

### Alur:
```
START (Admin klik "Add New Package")
  ↓
Tampilkan Form Modal atau Page
  ↓
Admin Mengisi Form:
  - Package Name (text input, required)
  - Price (number input, required, min: 0)
  - Quota Amount (number input, required, min: 1)
  ↓
Admin Submit Form
  ↓
Akses /add-quota-package/ (POST)
  ↓
[Validasi Input]
  ↓ (Valid)
Create QuotaPackage:
  - QuotaPackage.objects.create(
      name=POST['name'],
      price=POST['price'],
      quota_amount=POST['quota_amount']
    )
  ↓
Tampilkan Success Message
  ↓
Redirect ke Dashboard dengan ?section=quotapackage
  ↓
END
```

### 5b. Edit Package

### Alur:
```
START (Admin klik "Edit" pada package)
  ↓
Akses /update-quota-package/<package_id>/ (GET)
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query Package dari Database (get_object_or_404)
  ↓
Tampilkan Form dengan Data Existing
  ↓
Admin Edit Form:
  - Package Name (editable)
  - Price (editable)
  - Quota Amount (editable)
  ↓
Admin Submit Form
  ↓
[Method POST]
  ↓
[Validasi Input]
  ↓ (Valid)
Update Package di Database:
  - package.name = POST['name']
  - package.price = POST['price']
  - package.quota_amount = POST['quota_amount']
  - package.save()
  ↓
Tampilkan Success Message
  ↓
Redirect ke Dashboard
  ↓
END
```

### 5c. Delete Package

### Alur:
```
START (Admin klik "Delete" pada package)
  ↓
[Konfirmasi Delete]
  ↓ (Admin Confirm)
Akses /delete-quota-package/<package_id>/
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query Package dari Database (get_object_or_404)
  ↓
[Check Dependencies]
  ├─ Cek apakah ada QuotaPurchase yang menggunakan package ini
  └─ Cek apakah ada Transaction yang menggunakan package ini
  ↓
[Decision: Ada Dependencies?]
  ├─→ Yes: Tampilkan Warning "Package masih digunakan, tidak bisa dihapus"
  └─→ No: Lanjut Delete
  ↓ (No Dependencies)
Delete Package:
  - package.delete()
  ↓
Tampilkan Success Message
  ↓
Redirect ke Dashboard
  ↓
END
```

---

## 6. FLOWCHART MANAJEMEN TRANSAKSI

### Nama File: `FLOWCHART_ADMIN_MANAJEMEN_TRANSAKSI.html`

### Alur:
```
START (Admin klik "Manage Transaction" di Dashboard)
  ↓
Akses /dashboard/section/transaction
  ↓
[Validasi Akses Admin/Staff]
  ↓ (Access Granted)
Query Transaction dari Database:
  - Transaction.objects.select_related('user', 'package')
  - Order by created_at DESC
  - Pagination (10 per page)
  ↓
Render Template dashboard_payment_gateway.html
  ↓
Tampilkan List Transaksi:
  ├─ Order ID
  ├─ User Info (username, email)
  ├─ Package Info (name, price)
  ├─ Gross Amount (format: Rp)
  ├─ Transaction Status (pending/settlement/expire/cancel)
  ├─ Payment Type
  ├─ Created At
  └─ Actions (Delete, View Detail)
  ↓
Admin Memilih Aksi:
  ├─→ Delete Transaction → [Sub-flowchart 6a]
  ├─→ View Detail → [Sub-flowchart 6b]
  └─→ Filter by Status
  ↓
END
```

### 6a. Delete Transaction

### Alur:
```
START (Admin klik "Delete" pada transaksi)
  ↓
[Konfirmasi Delete]
  ↓ (Admin Confirm)
Akses /delete-transaction/<trx_id>/ (POST)
  ↓
[Validasi Akses Staff/Superuser]
  ↓ (Access Granted)
Query Transaction dari Database (get_object_or_404)
  ↓
[Check Status]
  ├─ Jika status = 'settlement': Warning "Transaksi sudah settlement, yakin hapus?"
  └─ Jika status = 'pending/expire/cancel': Bisa langsung delete
  ↓
[Decision: Admin Confirm Delete?]
  ├─→ Yes: Lanjut Delete
  └─→ No: Cancel, kembali ke list
  ↓ (Yes)
Delete Transaction:
  - transaction.delete()
  ↓
Tampilkan Success Message
  ↓
Redirect ke Dashboard
  ↓
END
```

### 6b. View Transaction Detail (Opsional)

### Alur:
```
START (Admin klik "View Detail" pada transaksi)
  ↓
Tampilkan Modal atau Page dengan Detail:
  ├─ Order ID
  ├─ User Info Lengkap
  ├─ Package Info Lengkap
  ├─ Gross Amount
  ├─ Transaction Status (dengan history)
  ├─ Payment Type
  ├─ Created At
  ├─ Midtrans Response (jika ada)
  └─ Related QuotaPurchase (jika ada)
  ↓
END
```

---

## 7. FLOWCHART MANAJEMEN AI MODEL CONFIG

### Nama File: `FLOWCHART_ADMIN_MANAJEMEN_AI_MODEL.html`

### Alur:
```
START (Admin klik "Manage AI Model Config" di Dashboard)
  ↓
Akses /dashboard/section/aimodelconfig
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query AiModelConfig dari Database:
  - AiModelConfig.objects.all().order_by('model_name')
  - Pagination (10 per page)
  ↓
Render Template dashboard_aimodelconfig.html
  ↓
Tampilkan List AI Models:
  ├─ Display Name
  ├─ Model Name (gemini, gpt-3.5-turbo, gpt-4-1106-preview)
  ├─ Description
  ├─ Quota Cost
  ├─ Is Active (badge)
  ├─ Created At
  └─ Actions (Edit, Delete, Toggle Active)
  ↓
Admin Memilih Aksi:
  ├─→ Add New Model → [Sub-flowchart 7a]
  ├─→ Edit Model → [Sub-flowchart 7b]
  ├─→ Delete Model → [Sub-flowchart 7c]
  ├─→ Toggle Active → [Sub-flowchart 7d]
  └─→ Back to Dashboard
  ↓
END
```

### 7a. Add New AI Model

### Alur:
```
START (Admin klik "Add New Model")
  ↓
Akses /add-ai-model-config/ (GET)
  ↓
Tampilkan Form
  ↓
Admin Mengisi Form:
  - Model Name (dropdown: gemini, gpt-3.5-turbo, gpt-4-1106-preview)
  - Display Name (text input, required)
  - Description (textarea, optional)
  - Quota Cost (number input, required, min: 1)
  - API Key (text input, optional, masked)
  - Is Active (checkbox, default: checked)
  ↓
Admin Submit Form
  ↓
[Method POST]
  ↓
[Validasi Input]
  ├─ Cek model_name unik (belum ada di database)
  └─ Validasi format model_name
  ↓
[Decision: Model Name Unik?]
  ├─→ No: Tampilkan Error "Model '{model_name}' sudah ada"
  └─→ Yes: Lanjut Create
  ↓ (Yes)
Create AiModelConfig:
  - AiModelConfig.objects.create(
      model_name=POST['model_name'],
      display_name=POST['display_name'],
      description=POST['description'],
      quota_cost=POST['quota_cost'],
      api_key=POST['api_key'] if POST['api_key'] else None,
      is_active=POST['is_active'] == 'on'
    )
  ↓
Tampilkan Success Message: "Model AI berhasil ditambahkan!"
  ↓
Redirect ke Dashboard
  ↓
END
```

### 7b. Edit AI Model

### Alur:
```
START (Admin klik "Edit" pada model)
  ↓
Akses /update-ai-model-config/<model_id>/ (GET)
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query Model dari Database (get_object_or_404)
  ↓
Tampilkan Form dengan Data Existing
  ↓
Admin Edit Form:
  - Model Name (readonly atau editable dengan validasi)
  - Display Name (editable)
  - Description (editable)
  - Quota Cost (editable)
  - API Key (editable, masked, placeholder: "Kosongkan jika tidak ingin diubah")
  - Is Active (checkbox, editable)
  ↓
Admin Submit Form
  ↓
[Method POST]
  ↓
[Validasi Input]
  ├─ Jika model_name diubah: Cek unik (kecuali model ini sendiri)
  └─ Validasi format
  ↓
[Decision: Model Name Valid?]
  ├─→ No: Tampilkan Error
  └─→ Yes: Lanjut Update
  ↓ (Yes)
Update Model di Database:
  - model.model_name = POST['model_name']
  - model.display_name = POST['display_name']
  - model.description = POST['description']
  - model.quota_cost = POST['quota_cost']
  - model.is_active = POST['is_active'] == 'on'
  - (Update API key hanya jika diisi)
  - if POST['api_key']:
  -   model.api_key = POST['api_key']
  - model.save()
  ↓
Tampilkan Success Message: "Model AI berhasil diupdate!"
  ↓
Redirect ke Dashboard
  ↓
END
```

### 7c. Delete AI Model

### Alur:
```
START (Admin klik "Delete" pada model)
  ↓
[Konfirmasi Delete]
  ↓ (Admin Confirm)
Akses /delete-ai-model-config/<model_id>/ (POST)
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query Model dari Database (get_object_or_404)
  ↓
[Check Dependencies]
  ├─ Cek apakah ada SeoAnalysis yang menggunakan model ini
  └─ Tampilkan warning jika ada dependencies
  ↓
[Decision: Ada Dependencies?]
  ├─→ Yes: Tampilkan Warning "Model masih digunakan, yakin hapus?"
  └─→ No: Lanjut Delete
  ↓ (Admin Confirm)
Delete Model:
  - model_name = model.display_name (untuk message)
  - model.delete()
  ↓
Tampilkan Success Message: "Model AI '{model_name}' berhasil dihapus!"
  ↓
Redirect ke Dashboard
  ↓
END
```

### 7d. Toggle Active AI Model (Opsional - bisa via Edit)

### Alur:
```
START (Admin klik Toggle Switch "Is Active")
  ↓
AJAX POST ke endpoint toggle (jika ada) atau Edit
  ↓
Query Model dari Database
  ↓
Toggle Status:
  - model.is_active = not model.is_active
  - model.save()
  ↓
Return JSON Response:
  - success: true
  - is_active: model.is_active
  - message: "Status model berhasil diubah"
  ↓
Update UI tanpa reload
  ↓
END
```

---

## 8. FLOWCHART MANAJEMEN API CONFIG

### Nama File: `FLOWCHART_ADMIN_MANAJEMEN_API_CONFIG.html`

### Alur:
```
START (Admin klik "Manage API Config" di Dashboard)
  ↓
Akses /dashboard/section/apiconfig
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query ApiConfig dari Database:
  - ApiConfig.objects.all().order_by('api_name')
  ↓
Render Template dashboard_apiconfig.html
  ↓
Tampilkan List API Configs:
  ├─ API Name (SerpAPI, Google Search API, Bing Search API)
  ├─ API Key (masked: ****)
  ├─ Base URL
  ├─ Max Results
  ├─ Timeout (seconds)
  ├─ Is Active (toggle switch)
  ├─ Description
  ├─ Created At
  └─ Actions (Edit, Toggle Active)
  ↓
Admin Memilih Aksi:
  ├─→ Edit API Config → [Sub-flowchart 8a]
  ├─→ Toggle Active → [Sub-flowchart 8b]
  └─→ Back to Dashboard
  ↓
END
```

### 8a. Edit API Config

### Alur:
```
START (Admin klik "Edit" pada API config)
  ↓
Akses /admin/api-config/<config_id>/update/ (GET)
  ↓
[Validasi Akses Staff/Superuser]
  ↓ (Access Granted)
Query ApiConfig dari Database (get_object_or_404)
  ↓
Tampilkan Form Modal atau Page
  ↓
Admin Edit Form:
  - API Name (readonly - tidak bisa diubah)
  - API Key (text input, masked, editable)
  - Base URL (text input, editable)
  - Max Results (number input, editable, min: 1, max: 100)
  - Timeout (number input, editable, min: 1, max: 300)
  - Description (textarea, editable)
  - Is Active (checkbox atau toggle, editable)
  ↓
Admin Submit Form
  ↓
AJAX POST ke /admin/api-config/<config_id>/update/
  ↓
[Method POST]
  ↓
[Validasi Input]
  ├─ Validasi URL format (base_url)
  ├─ Validasi number ranges (max_results, timeout)
  └─ Sanitize API key
  ↓
Update ApiConfig di Database:
  - config.api_key = POST['api_key']
  - config.base_url = POST['base_url']
  - config.max_results = int(POST['max_results'])
  - config.timeout = int(POST['timeout'])
  - config.description = POST['description']
  - config.is_active = POST.get('is_active', False) == 'on' or True
  - config.save()
  ↓
Return JSON Response:
  - success: true
  - message: "API configuration {api_name} updated successfully"
  ↓
Tampilkan Success Message (toast)
  ↓
Update UI tanpa reload (jika AJAX)
  ↓
END
```

### 8b. Toggle Active API Config

### Alur:
```
START (Admin klik Toggle Switch "Is Active")
  ↓
AJAX POST ke /admin/api-config/<config_id>/toggle/
  ↓
[Validasi Akses Staff/Superuser]
  ↓ (Access Granted)
Query ApiConfig dari Database (get_object_or_404)
  ↓
Toggle Status:
  - config.is_active = not config.is_active
  - config.save()
  ↓
Return JSON Response:
  - success: true
  - message: "Status API {api_name} berhasil diubah"
  - is_active: config.is_active
  ↓
Update UI Toggle Switch tanpa reload
  ↓
Tampilkan Toast Notification
  ↓
END
```

### 8c. Test API Connection (Opsional Enhancement)

### Alur:
```
START (Admin klik "Test Connection" pada API config)
  ↓
AJAX POST ke /admin/api-config/<config_id>/test/
  ↓
[Validasi Akses Admin]
  ↓ (Access Granted)
Query ApiConfig dari Database
  ↓
[Decision: API Name?]
  ├─→ serpapi: Test dengan request sederhana ke SerpAPI
  ├─→ google_search: Test dengan request ke Google Search API
  └─→ bing_search: Test dengan request ke Bing Search API
  ↓
Test API Connection:
  - Buat request test ke API
  - Cek response status
  - Cek error messages
  ↓
Return JSON Response:
  - success: true/false
  - status_code: HTTP status
  - message: "Connection successful" atau error message
  - response_time: milliseconds
  ↓
Tampilkan Test Result:
  ├─ Green badge jika success
  ├─ Red badge jika failed
  └─ Error details jika ada
  ↓
END
```

---

## 9. STRUKTUR VISUAL & NOTASI

### Simbol yang Digunakan:

1. **Start/End**: Oval (Terminator)
   - Label: "START" atau "END"

2. **Process**: Rectangle
   - Label: Aksi atau proses yang dilakukan
   - Contoh: "Query User dari Database"

3. **Decision**: Diamond
   - Label: Pertanyaan atau kondisi
   - Contoh: "Apakah login valid?"
   - Output: "Yes" / "No" atau "Valid" / "Invalid"

4. **Input/Output**: Parallelogram
   - Label: Input dari user atau output ke user
   - Contoh: "Admin Mengisi Form"

5. **Connector**: Circle
   - Label: Penghubung ke flowchart lain
   - Contoh: "[Flowchart 4a]"

6. **Predefined Process**: Rectangle dengan garis ganda
   - Label: Proses yang sudah didefinisikan di tempat lain
   - Contoh: "[Validasi Akses Admin]"

### Warna yang Disarankan:

- **Start/End**: Hijau (#10b981)
- **Process**: Biru (#3b82f6)
- **Decision**: Kuning (#f59e0b)
- **Error Path**: Merah (#ef4444)
- **Success Path**: Hijau (#10b981)
- **Warning**: Orange (#f97316)

### Format HTML:

- Gunakan library flowchart.js atau mermaid.js
- Atau gunakan diagram HTML dengan CSS styling
- Konsisten dengan flowchart yang sudah ada (FLOWCHART_*.html)

### Penjelasan Tambahan:

Setiap flowchart utama harus memiliki:
1. **Header**: Judul flowchart
2. **Legend**: Penjelasan simbol yang digunakan
3. **Decision Points**: Semua decision points dijelaskan
4. **Error Handling**: Path error ditampilkan dengan jelas
5. **Integration Points**: Integrasi dengan sistem eksternal (WhatsApp, API) ditandai
6. **Database Operations**: Query database ditandai dengan jelas
7. **Ending**: Setiap flowchart berakhir dengan jelas (END atau redirect)

---

## 10. PRIORITAS IMPLEMENTASI

### Phase 1 (High Priority):
1. ✅ Flowchart Utama (Entry Point Admin)
2. ✅ Flowchart Dashboard Admin (Stats & Chart)
3. ✅ Flowchart Manajemen User (CRUD)
4. ✅ Flowchart Manajemen Pembayaran (Approve/Reject)

### Phase 2 (Medium Priority):
5. ✅ Flowchart Manajemen Paket Kuota (CRUD)
6. ✅ Flowchart Manajemen Transaksi (View & Delete)

### Phase 3 (Low Priority - Enhancement):
7. ✅ Flowchart Manajemen AI Model Config (CRUD & Toggle)
8. ✅ Flowchart Manajemen API Config (Update & Toggle)
9. ⚠️ Flowchart Test API Connection (Opsional)

---

## 11. CATATAN PENTING

1. **Validasi Akses**: Setiap flowchart harus dimulai dengan validasi akses admin/superuser
2. **Error Handling**: Semua error path harus ditampilkan (database error, validation error, dll)
3. **Database Cascade**: Perhatikan CASCADE delete pada model (CustomUser → UserStatus, RankResult, dll)
4. **WhatsApp Notification**: Tandai jika ada notifikasi WhatsApp (saat approve pembayaran)
5. **Pagination**: Semua list view menggunakan pagination (10 per page)
6. **AJAX vs Full Page**: Bedakan operasi AJAX (Toggle, Update) dengan full page (Create, Delete)
7. **Success Messages**: Setiap operasi sukses harus menampilkan message dan redirect
8. **Consistency**: Gunakan format dan styling yang sama dengan flowchart yang sudah ada

---

**Total Flowchart yang Akan Dibuat: 8-9 file HTML**

