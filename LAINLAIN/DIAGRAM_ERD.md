# DIAGRAM ERD - SISTEM RANK CHECKER

## ENTITAS (Entities)

### 1. CustomUser
- **Primary Key**: id (dari AbstractUser)
- **Attributes**:
  - username, email, password (dari AbstractUser)
  - role (CharField: admin/user)
  - whatsapp_number (CharField, nullable)
  - otp_code (CharField, nullable)
  - date_joined, is_active, is_staff, is_superuser (dari AbstractUser)

### 2. UserStatus
- **Primary Key**: id (OneToOne dengan CustomUser)
- **Attributes**:
  - status (CharField: guest/premium)
  - total_quota (PositiveInteger)
  - used_quota (PositiveInteger)
  - start_date (DateTime)
  - created_at, updated_at (DateTime)

### 3. Billing
- **Primary Key**: user (OneToOne dengan CustomUser)
- **Attributes**:
  - status_pembayaran (Boolean)
  - bukti_pembayaran (ImageField)

### 4. RankResult
- **Primary Key**: id
- **Attributes**:
  - domain (CharField)
  - keyword (CharField)
  - rank (PositiveInteger)
  - url_result (URLField)
  - checked_at (DateTime)

### 5. SeoAnalysis
- **Primary Key**: id
- **Attributes**:
  - keyword (CharField)
  - domain (CharField)
  - analysis (TextField)
  - metadata (JSONField, nullable)
  - model_used (CharField)
  - created_at (DateTime)

### 6. QuotaPackage
- **Primary Key**: id
- **Attributes**:
  - name (CharField)
  - price (PositiveInteger)
  - quota_amount (PositiveInteger)

### 7. QuotaPurchase
- **Primary Key**: id
- **Attributes**:
  - payment_proof (ImageField, nullable)
  - status (CharField: pending/approved/rejected)
  - created_at (DateTime)

### 8. Transaction
- **Primary Key**: id
- **Attributes**:
  - order_id (CharField, unique)
  - gross_amount (Integer)
  - transaction_status (CharField)
  - payment_type (CharField, nullable)
  - created_at (DateTime)

### 9. CheckoutSession
- **Primary Key**: id
- **Attributes**:
  - session_id (CharField, unique)
  - status (CharField: active/expired/completed/cancelled)
  - expires_at (DateTime)
  - created_at, updated_at (DateTime)

### 10. AiModelConfig
- **Primary Key**: id
- **Attributes**:
  - model_name (CharField, unique)
  - display_name (CharField)
  - description (TextField)
  - quota_cost (PositiveInteger)
  - is_active (Boolean)
  - api_key (CharField, nullable)
  - created_at, updated_at (DateTime)

### 11. ApiConfig
- **Primary Key**: id
- **Attributes**:
  - api_name (CharField, unique)
  - api_key (CharField)
  - base_url (URLField)
  - max_results (PositiveInteger)
  - timeout (PositiveInteger)
  - is_active (Boolean)
  - description (TextField)
  - created_at, updated_at (DateTime)

---

## RELASI (Relationships)

### One-to-One (1:1)
1. **CustomUser ↔ UserStatus** (OneToOne)
   - Satu user memiliki satu status
   - Primary key UserStatus = Foreign key ke CustomUser

2. **CustomUser ↔ Billing** (OneToOne)
   - Satu user memiliki satu billing
   - Primary key Billing = Foreign key ke CustomUser

### One-to-Many (1:N)
3. **CustomUser → RankResult** (ForeignKey)
   - Satu user dapat memiliki banyak hasil rank check
   - on_delete: CASCADE

4. **CustomUser → SeoAnalysis** (ForeignKey)
   - Satu user dapat memiliki banyak analisis SEO
   - on_delete: CASCADE

5. **CustomUser → QuotaPurchase** (ForeignKey)
   - Satu user dapat memiliki banyak pembelian kuota
   - on_delete: CASCADE

6. **CustomUser → Transaction** (ForeignKey)
   - Satu user dapat memiliki banyak transaksi
   - on_delete: CASCADE

7. **CustomUser → CheckoutSession** (ForeignKey)
   - Satu user dapat memiliki banyak checkout session
   - on_delete: CASCADE

8. **QuotaPackage → QuotaPurchase** (ForeignKey)
   - Satu paket dapat dibeli oleh banyak user
   - on_delete: CASCADE

9. **QuotaPackage → Transaction** (ForeignKey)
   - Satu paket dapat digunakan dalam banyak transaksi
   - on_delete: CASCADE

10. **QuotaPackage → CheckoutSession** (ForeignKey)
    - Satu paket dapat digunakan dalam banyak checkout session
    - on_delete: CASCADE

### Independent Entities
11. **AiModelConfig** - Tidak ada relasi langsung
12. **ApiConfig** - Tidak ada relasi langsung

---

## STATISTIK
- **Total Entitas**: 11
- **Relasi One-to-One**: 2
- **Relasi One-to-Many**: 8
- **Independent Entities**: 2

---

## CATATAN
- **CASCADE Delete**: Semua relasi menggunakan CASCADE, artinya jika parent dihapus, child juga terhapus
- **Primary Key**: CustomUser menggunakan id dari AbstractUser (auto-increment)
- **Unique Constraints**: order_id (Transaction), session_id (CheckoutSession), model_name (AiModelConfig), api_name (ApiConfig)


