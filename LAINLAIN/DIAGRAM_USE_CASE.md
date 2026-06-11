# DIAGRAM USE CASE - SISTEM RANK CHECKER

## AKTOR
1. **Guest** - Pengunjung belum login
2. **User** - Pengguna terdaftar (guest/premium)
3. **Admin** - Administrator sistem
4. **System** - Sistem eksternal (APIs)

---

## USE CASE

### GUEST
| UC | Use Case |
|---|---|
| 01 | Landing Page |
| 02 | Register → Verifikasi OTP |
| 03 | Login |

### USER
| UC | Use Case |
|---|---|
| 04 | Login / Logout |
| 05 | Dashboard |
| 06 | Cek Rank Website (History, Export PDF) |
| 08 | Analisis SEO dengan AI *(Premium only, History)* |
| 10 | Beli Kuota (Manual/Midtrans, Upload Bukti, Status) |

### ADMIN
| UC | Use Case |
|---|---|
| 13 | Dashboard Admin (Statistik, Grafik) |
| 14 | Manajemen User (CRUD, Toggle Status) |
| 15 | Manajemen Pembayaran (Approve/Reject, Transaksi) |
| 16 | Manajemen Paket Kuota (CRUD) |
| 17 | Manajemen AI Model (CRUD, Toggle) |
| 18 | Manajemen API Config (Update, Toggle) |

### SYSTEM
| UC | Use Case |
|---|---|
| - | Notifikasi & Callback (OTP, Payment, Quods, Midtrans) |
| 22 | Google Search (SerpAPI) |
| 23 | Analisis AI (Gemini/OpenAI API) |

---

## DIAGRAM USE CASE

```
┌─────────────────────────────────────────┐
│         SISTEM RANK CHECKER             │
└─────────────────────────────────────────┘

┌──────────┐
│  Guest   │───► UC-01: Landing Page
│          │───► UC-02: Register → OTP
│          │───► UC-03: Login
└──────────┘

┌──────────┐
│  User    │───► UC-04: Login/Logout
│          │───► UC-05: Dashboard
│          │───► UC-06: Cek Rank (History)
│          │───► UC-08: Analisis SEO (Premium, History)
│          │───► UC-10: Beli Kuota (Upload Bukti, Status)
└──────────┘

┌──────────┐
│  Admin   │───► UC-13: Dashboard & Statistik
│          │───► UC-14: Manajemen User
│          │───► UC-15: Manajemen Pembayaran
│          │───► UC-16: Manajemen Paket
│          │───► UC-17: Manajemen AI Model
│          │───► UC-18: Manajemen API Config
└──────────┘

┌──────────┐
│ System   │───► Notifikasi & Callback (OTP, Payment)
│          │───► UC-22: Google Search (SerpAPI)
│          │───► UC-23: Analisis AI (Gemini/OpenAI)
└──────────┘
```

---

## STATISTIK
- **Aktor**: 4 (Guest, User, Admin, System)
- **Use Case**: 16
  - Guest: 3 | User: 5 | Admin: 6 | System: 3

---

## CATATAN
- **Premium Only**: UC-08 (Analisis SEO) hanya untuk user premium
- **Kuota**: Cek rank (-1 kuota), Analisis SEO (-2 sampai -5 kuota sesuai model)
- **Pembayaran**: Manual (butuh approval) atau Midtrans (otomatis)

