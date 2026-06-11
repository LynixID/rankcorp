# PENJELASAN LOGIC CODE UTAMA - SISTEM RANK CHECKER (U-RANK)

Dokumen ini berisi penjelasan ringkas dan akurat untuk setiap logic utama dalam sistem Rank Checker.

---

## A. AUTHENTICATION & REGISTRATION

### LOGIC UTAMA 1: Generate OTP 6 Digit

Sistem menghasilkan kode OTP enam digit secara acak menggunakan fungsi `random.randint()` dengan rentang 100000 hingga 999999. OTP dikonversi menjadi string dan digunakan sebagai kode verifikasi yang dikirimkan ke pengguna melalui WhatsApp saat proses registrasi.

### LOGIC UTAMA 2: Register View dengan Validasi Lengkap

Sistem melakukan validasi keunikan username dan email, format nomor WhatsApp (harus diawali 62), serta kesesuaian password dengan konfirmasi. Apabila semua validasi berhasil, sistem menghasilkan OTP, menyimpan data ke session, dan mengirimkan OTP ke WhatsApp pengguna sebelum mengarahkan ke halaman verifikasi.

### LOGIC UTAMA 3: Verifikasi OTP dan Create User Baru

Sistem membandingkan OTP yang diinput dengan OTP di session. Jika sesuai, sistem membuat akun pengguna baru dengan role user, membuat UserStatus dengan status guest dan 3 kuota gratis, kemudian menghapus session dan mengarahkan ke halaman login.

### LOGIC UTAMA 4: Login View

Sistem memverifikasi kredensial username dan password menggunakan fungsi `authenticate()` dari Django. Jika valid, pengguna di-login dan diarahkan ke dashboard sesuai role, sedangkan jika tidak valid, sistem menampilkan pesan kesalahan.

---

## B. CEK RANKING

### LOGIC UTAMA 5: Get Ranks dari SerpAPI

Sistem mengambil konfigurasi API dari database atau menggunakan konfigurasi default, kemudian mengirimkan request HTTP GET ke SerpAPI dengan parameter pencarian. Respons JSON di-parse untuk mengekstrak hasil pencarian, lalu sistem melakukan iterasi untuk mencari URL yang mengandung domain target dan mengembalikan daftar posisi ranking beserta URL lengkap.

### LOGIC UTAMA 6: Check Rank View - Proses Pengecekan Ranking Utama

Sistem memvalidasi keberadaan UserStatus dan ketersediaan kuota, kemudian mengambil parameter pencarian dari form dan melakukan request ke SerpAPI. Hasil pencarian yang mengandung domain target disimpan ke database sebagai RankResult, kuota pengguna dikurangi satu, dan hasil ditampilkan beserta histori pengecekan sebelumnya.

---

## C. SEO ANALYSIS DENGAN AI

### LOGIC UTAMA 7: SEO Analysis dengan AI (Gemini/OpenAI)

Sistem memvalidasi status premium pengguna dan ketersediaan kuota sesuai biaya model AI yang dipilih. Sistem menganalisis data ranking history untuk menghitung tren dan stabilitas, membangun prompt analisis SEO, lalu melakukan routing ke Gemini API atau OpenAI API sesuai pilihan. Hasil analisis disimpan ke database, kuota dikurangi, dan hasil dikembalikan dalam format JSON.

---

## D. SISTEM KUOTA

### LOGIC UTAMA 8: Model Method - Remaining Quota Calculation

Metode ini menghitung sisa kuota dengan mengurangi total kuota dengan kuota yang sudah digunakan. Hasil perhitungan digunakan untuk validasi ketersediaan kuota sebelum pengguna melakukan aktivitas yang memerlukan kuota.

### LOGIC UTAMA 9: Approve Quota Purchase (Admin)

Administrator memvalidasi izin admin, kemudian sistem mengubah status pembelian menjadi approved dan menambahkan kuota sesuai paket yang dibeli ke total_quota pengguna. Proses ini memungkinkan pengguna menggunakan kuota setelah pembayaran diverifikasi.

### LOGIC UTAMA 10: Payment Notification Callback (Midtrans - Auto Approve)

Sistem menerima callback dari Midtrans, melakukan parsing data JSON, dan memperbarui status transaksi. Jika pembayaran berhasil (settlement), sistem secara otomatis menambahkan kuota, mengubah status pengguna menjadi premium, dan mengirimkan notifikasi WhatsApp tanpa intervensi manual administrator.

---

## E. PAYMENT & CHECKOUT

### LOGIC UTAMA 11: Create Checkout Session (Transfer Bank Manual)

Sistem mengecek apakah pengguna memiliki session aktif. Jika ada dan belum kadaluarsa, pengguna diarahkan ke halaman upload bukti. Jika tidak ada, sistem membuat session baru dengan UUID sebagai session ID dan waktu kadaluarsa dua jam, kemudian menyimpan ke database dengan status active.

### LOGIC UTAMA 12: Upload Payment Proof (Transfer Bank Manual)

Sistem memvalidasi keberadaan session checkout aktif yang belum kadaluarsa. Jika valid, file bukti pembayaran divalidasi dan disimpan, kemudian sistem membuat entitas QuotaPurchase dengan status pending dan mengubah status session menjadi completed. Pengguna diarahkan ke halaman status pembelian.

### LOGIC UTAMA 13: Start Payment Midtrans

Sistem menghasilkan order ID menggunakan UUID, membuat entitas Transaction dengan status pending, dan menginisialisasi klien Midtrans Snap. Sistem membangun payload transaksi dan mengirimkan request ke Midtrans API untuk menghasilkan Snap token, kemudian mengembalikan token beserta client key dalam format JSON untuk inisialisasi frontend.

---

## F. WHATSAPP INTEGRATION

### LOGIC UTAMA 14: Send WhatsApp Direct (OTP & Notifikasi)

Sistem membangun request HTTP dengan token autentikasi Bearer dan payload JSON berisi device key, nomor telepon, serta pesan yang akan dikirim. Sistem melakukan request POST ke API Quods, menangani respons untuk memverifikasi status pengiriman, dan mengembalikan hasil atau None jika terjadi kesalahan. Fungsi ini digunakan untuk mengirimkan OTP registrasi dan notifikasi konfirmasi pembayaran.

---

## RINGKASAN

Sistem Rank Checker (U-RANK) memiliki empat belas logic utama yang mencakup autentikasi dan registrasi dengan verifikasi OTP, pengecekan ranking melalui SerpAPI, analisis SEO berbasis AI, manajemen kuota dengan approval manual dan otomatis, serta proses pembayaran melalui transfer bank dan payment gateway. Semua logic dirancang untuk memastikan proses bisnis berjalan efisien dengan menjaga keamanan dan akurasi data melalui mekanisme validasi yang komprehensif.

