# PENJELASAN HALAMAN SISTEM U-RANK

Dokumen ini berisi penjelasan singkat dan mudah dipahami untuk setiap halaman dalam sistem U-Rank.

---

## HALAMAN PUBLIK

### 1. Landing Pages

Landing Pages merupakan halaman pertama yang ditampilkan kepada pengunjung ketika mengakses website U-Rank. Halaman ini berfungsi untuk memberikan informasi awal mengenai sistem kepada pengunjung yang belum terdaftar. Halaman ini menampilkan deskripsi sistem U-Rank sebagai alat untuk mengecek ranking SEO website di Google secara real-time, keunggulan sistem meliputi akurasi data yang tinggi, update ranking real-time, dan kemampuan analisis mendalam. Selain itu, halaman ini juga menyediakan penjelasan mengenai cara kerja sistem serta call to action berupa tombol untuk mendaftar atau melakukan login.

---

### 2. Register (Daftar)

Halaman Register merupakan halaman pendaftaran untuk pengguna baru yang ingin menggunakan sistem U-Rank. Pada halaman ini, pengguna diminta untuk mengisi beberapa informasi yang terdiri dari username yang bersifat unik, email yang bersifat unik, nomor WhatsApp dengan format Indonesia (62xxx), password, dan konfirmasi password. Sistem akan melakukan validasi terhadap semua input yang dimasukkan pengguna. Apabila data valid, sistem akan menghasilkan kode OTP enam digit dan mengirimkannya ke nomor WhatsApp pengguna melalui integrasi Quods API. Setelah kode OTP berhasil dikirim, pengguna akan diarahkan ke halaman verifikasi OTP untuk menyelesaikan proses registrasi.

---

### 3. Login (Masuk)

Halaman Login merupakan halaman autentikasi yang digunakan oleh pengguna yang sudah memiliki akun untuk mengakses berbagai fitur dalam sistem U-Rank. Pada halaman ini, pengguna memasukkan username dan password yang telah didaftarkan sebelumnya. Sistem akan melakukan proses verifikasi kredensial yang dimasukkan terhadap data yang tersimpan di database. Apabila kredensial valid, sistem akan mengarahkan pengguna ke halaman dashboard utama. Apabila kredensial tidak valid, sistem akan menampilkan pesan error yang informatif kepada pengguna.

---

## HALAMAN USER

### 4. Halaman User - Dashboard Search Rank (Cek Ranking)

Halaman Dashboard Search Rank merupakan halaman utama yang digunakan oleh pengguna untuk melakukan pengecekan ranking website mereka di mesin pencari Google. Pada halaman ini, pengguna mengisi form yang berisi keyword atau kata kunci yang ingin dicek, domain website yang ingin diketahui rankingnya, serta region atau negara target pencarian dengan default Indonesia. Setelah form dikirimkan, sistem akan menggunakan integrasi SerpAPI untuk melakukan pencarian ranking website di Google Search Engine sesuai dengan parameter yang dimasukkan. Setiap pengecekan ranking akan mengurangi satu kuota dari akun pengguna. Hasil pengecekan yang diperoleh akan disimpan ke dalam database dan ditampilkan kepada pengguna dalam bentuk tabel yang memuat informasi posisi ranking, URL lengkap, title halaman, serta total jumlah hasil yang ditemukan.

---

### 5. Halaman User - Histori Search (Histori Pencarian)

Halaman Histori Search berfungsi untuk menampilkan ringkasan semua pengecekan ranking yang pernah dilakukan oleh pengguna selama menggunakan sistem. Informasi pada halaman ini disajikan dalam bentuk tabel yang menampilkan setiap kombinasi unik antara keyword dan domain yang pernah dicek, beserta dengan total jumlah pengecekan yang telah dilakukan untuk setiap kombinasi tersebut. Pada setiap baris dalam tabel, terdapat tombol "Detail" yang memungkinkan pengguna untuk melihat informasi lengkap mengenai pengecekan ranking untuk kombinasi keyword dan domain tertentu.

---

### 6. Halaman User - Detail Histori Search (Detail Histori Pencarian)

Halaman Detail Histori Search berfungsi untuk menampilkan informasi lengkap mengenai hasil pengecekan ranking untuk kombinasi keyword dan domain tertentu yang dipilih oleh pengguna dari halaman Histori Search. Halaman ini menyediakan beberapa fitur penting, yaitu grafik trend ranking yang memvisualisasikan perubahan ranking dari waktu ke waktu menggunakan library Chart.js, tabel detail yang berisi semua hasil pengecekan dengan sistem pagination sebanyak sepuluh data per halaman, tab khusus untuk analisis SEO menggunakan artificial intelligence yang hanya dapat diakses oleh pengguna dengan status Premium dengan pilihan model AI berupa Gemini, GPT-3.5, atau GPT-4, serta fitur export PDF yang memungkinkan pengguna untuk mengunduh hasil pengecekan sebagai dokumen PDF.

---

### 7. Halaman User - Analisis (Analisis SEO)

Fitur Analisis SEO merupakan fitur yang tersedia di dalam tab khusus pada halaman Detail Histori Search. Fitur ini memungkinkan pengguna untuk melakukan analisis SEO menggunakan teknologi artificial intelligence. Untuk menggunakan fitur ini, pengguna memilih model AI yang diinginkan di antara Gemini, GPT-3.5, atau GPT-4, kemudian mengklik tombol "Analisis SEO". Sistem akan melakukan validasi terhadap status Premium pengguna dan ketersediaan kuota sesuai dengan biaya yang ditetapkan untuk model AI yang dipilih. Setelah validasi berhasil, sistem akan menganalisis data ranking history pengguna dan mengirimkan request ke API AI yang dipilih. Hasil analisis yang diperoleh akan disimpan ke dalam database dan kuota pengguna akan dikurangi sesuai dengan biaya model AI yang digunakan. Tersedia tiga pilihan model AI dengan biaya yang berbeda, yaitu Gemini dengan biaya 3 kuota, GPT-3.5 dengan biaya 2 kuota, dan GPT-4 dengan biaya 5 kuota.

---

### 8. Halaman User - Detail Analisis

Halaman Detail Analisis berfungsi untuk menampilkan informasi lengkap mengenai hasil analisis SEO yang telah dilakukan oleh pengguna menggunakan fitur Analisis SEO. Halaman ini dapat diakses melalui halaman Histori Analisis dengan mengklik hasil analisis tertentu. Halaman ini menampilkan informasi dasar meliputi keyword yang dianalisis, domain yang dianalisis, model AI yang digunakan, serta tanggal dan waktu analisis dilakukan. Selain itu, halaman ini juga menampilkan hasil analisis yang mencakup ringkasan performa ranking, analisis trend ranking, penyebab perubahan ranking, rekomendasi perbaikan SEO yang dapat diterapkan, serta target ranking yang realistis.

---

### 9. Halaman User - Histori Analisis (Riwayat Analisis SEO)

Halaman Histori Analisis berfungsi untuk menampilkan daftar semua analisis SEO yang pernah dilakukan oleh pengguna selama menggunakan sistem U-Rank. Informasi pada halaman ini disajikan dalam bentuk tabel yang mencakup tanggal dan waktu analisis dilakukan, keyword yang dianalisis, domain yang dianalisis, serta model AI yang digunakan dalam proses analisis. Pada setiap baris dalam tabel, terdapat tombol "Lihat Detail" yang memungkinkan pengguna untuk mengakses halaman Detail Analisis untuk melihat hasil lengkap dari analisis tersebut.

---

### 10. Halaman User - Paket Kuota (Beli Kuota)

Halaman Paket Kuota merupakan halaman yang digunakan oleh pengguna untuk membeli paket kuota tambahan guna melanjutkan penggunaan berbagai fitur yang tersedia dalam sistem U-Rank. Halaman ini menampilkan daftar semua paket kuota yang tersedia untuk dibeli beserta informasi berupa nama paket, harga paket, jumlah kuota yang akan diterima, serta fitur Premium yang akan didapatkan. Ketika pengguna memilih paket yang diinginkan dan mengklik tombol "Pilih Paket Ini", sistem akan membuka modal checkout yang menampilkan detail paket yang dipilih dan memberikan opsi metode pembayaran berupa Transfer Bank atau Midtrans. Apabila pengguna memilih metode Transfer Bank, sistem akan membuat checkout session dengan batas waktu dua jam dan mengarahkan pengguna ke halaman upload bukti pembayaran. Apabila pengguna memilih metode Midtrans, sistem akan mengarahkan pengguna ke halaman pembayaran Midtrans.

---

### 11. Halaman User - Upload Bukti Pembayaran

Halaman Upload Bukti Pembayaran merupakan halaman yang digunakan oleh pengguna untuk mengunggah bukti pembayaran ketika melakukan pembelian paket kuota melalui metode transfer bank. Halaman ini menggunakan layout dua panel, di mana panel kiri menampilkan informasi pembayaran meliputi countdown timer apabila terdapat checkout session yang aktif, detail paket yang dibeli, nominal transfer yang merupakan penjumlahan antara harga paket dan ID pengguna sebagai nominal unik, serta informasi lengkap mengenai rekening bank tujuan. Panel kanan berisi form upload yang memungkinkan pengguna untuk mengunggah bukti pembayaran dengan cara drag and drop atau dengan mengklik area yang tersedia, dan sistem menyediakan fitur preview gambar sebelum submit. Format file yang dapat diunggah adalah JPG, PNG, atau GIF dengan ukuran maksimal 5MB. Setelah bukti pembayaran diunggah dan dikirimkan, sistem akan menyimpan bukti tersebut ke dalam database dan mengubah status pembelian menjadi "Menunggu" untuk menunggu proses verifikasi oleh administrator.

---

### 12. Halaman User - Histori Pembelian (Status Pembelian)

Halaman Histori Pembelian berfungsi untuk menampilkan riwayat semua pembelian paket kuota yang pernah dilakukan oleh pengguna. Informasi pada halaman ini disajikan dalam bentuk tabel yang mencakup tanggal dan waktu pembelian dilakukan, nama paket yang dibeli, harga paket yang dibayarkan, jumlah kuota yang akan diterima, link untuk melihat bukti pembayaran apabila sudah diunggah, serta status pembelian. Status pembelian memiliki tiga kemungkinan, yaitu "Menunggu" yang menunjukkan pembayaran masih menunggu proses verifikasi oleh administrator, "Disetujui" yang menunjukkan pembayaran telah diverifikasi dan kuota telah ditambahkan ke akun pengguna, serta "Ditolak" yang menunjukkan pembayaran ditolak oleh administrator dan tidak ada kuota yang ditambahkan.

---

## HALAMAN ADMIN

### 13. Halaman Admin - Dashboard

Halaman Admin Dashboard merupakan halaman utama yang memberikan gambaran menyeluruh mengenai kondisi dan aktivitas sistem U-Rank kepada administrator. Bagian atas halaman menampilkan empat kartu statistik yang memberikan ringkasan cepat mengenai kondisi sistem, meliputi total jumlah pengguna yang terdaftar dalam sistem, jumlah pembayaran yang telah disetujui, total pengecekan kata kunci yang telah dilakukan oleh semua pengguna, serta jumlah pembayaran yang masih menunggu verifikasi dari administrator. Selain itu, halaman ini juga menampilkan grafik tren yang memvisualisasikan aktivitas pengecekan kata kunci selama tiga puluh hari terakhir menggunakan library Chart.js, serta tabel yang menampilkan aktivitas pengecekan kata kunci terbaru yang mencakup informasi mengenai nama pengguna, keyword yang dicek, serta tanggal dan waktu pengecekan dilakukan.

---

### 14. Halaman Admin - Pengguna (User Management)

Halaman User Management merupakan halaman yang digunakan oleh administrator untuk mengelola data dan status semua pengguna yang terdaftar dalam sistem U-Rank. Informasi pada halaman ini disajikan dalam bentuk tabel yang mencakup username, alamat email, nomor WhatsApp, role atau peran pengguna dalam sistem berupa user atau admin, tanggal bergabung, serta status akun apakah aktif atau nonaktif. Halaman ini dilengkapi dengan fitur search yang memungkinkan administrator untuk mencari pengguna berdasarkan username atau email. Fitur utama yang tersedia meliputi kemampuan untuk mengedit data pengguna berupa username, email, nomor WhatsApp, dan role, serta kemampuan untuk melakukan aktivasi atau deaktivasi akun pengguna.

---

### 15. Halaman Admin - Konfigurasi API (API Configuration)

Halaman Konfigurasi API merupakan halaman yang digunakan oleh administrator untuk mengelola dan menguji konfigurasi API yang digunakan oleh sistem untuk melakukan pengecekan ranking, terutama SerpAPI. Informasi konfigurasi yang dapat dikelola meliputi API key yang diperlukan untuk autentikasi, base URL atau endpoint API, max results atau jumlah maksimal hasil pencarian, timeout atau batas waktu maksimal untuk setiap request, serta status aktif atau nonaktif dari konfigurasi tersebut. Fitur utama yang tersedia meliputi kemampuan untuk mengedit parameter konfigurasi dan melakukan debug dengan mengklik tombol debug yang akan membuka popup berisi detail konfigurasi dan tombol "Test API" untuk menguji koneksi API. Pengujian API dilakukan menggunakan parameter default berupa keyword "serp api", domain "serpapi.com", dan region Indonesia. Hasil pengujian yang ditampilkan meliputi status berhasil atau gagal, waktu respon dalam milidetik, serta jumlah ranking yang berhasil ditemukan.

---

### 16. Halaman Admin - Paket Kuota (Quota Package Management)

Halaman Paket Kuota merupakan halaman yang digunakan oleh administrator untuk mengelola paket-paket kuota yang tersedia untuk dibeli oleh pengguna dalam sistem U-Rank. Informasi yang ditampilkan untuk setiap paket meliputi nama paket, harga paket dalam rupiah, jumlah kuota yang akan diterima pengguna ketika membeli paket tersebut, serta status apakah paket tersebut aktif atau nonaktif. Fitur utama yang tersedia meliputi kemampuan untuk menambah paket kuota baru dengan menentukan nama, harga, dan jumlah kuota, mengedit detail paket yang sudah ada berupa nama paket, harga, atau jumlah kuota, serta mengaktifkan atau menonaktifkan paket tanpa menghapus data paket tersebut.

---

### 17. Halaman Admin - Konfigurasi Model AI (AI Model Configuration)

Halaman Konfigurasi Model AI merupakan halaman yang digunakan oleh administrator untuk mengelola konfigurasi model-model artificial intelligence yang digunakan dalam fitur analisis SEO sistem U-Rank. Informasi konfigurasi yang dapat dikelola untuk setiap model AI meliputi nama model berupa Gemini, GPT-3.5, atau GPT-4, display name atau nama tampilan yang akan dilihat oleh pengguna, deskripsi model, quota cost atau biaya kuota yang dikenakan setiap kali analisis dilakukan, API key yang diperlukan untuk autentikasi ke layanan AI, base URL atau endpoint API dari penyedia layanan AI, serta status aktif atau nonaktif dari model tersebut. Fitur utama yang tersedia meliputi kemampuan untuk mengedit parameter konfigurasi dan mengaktifkan atau menonaktifkan model AI tanpa menghapus konfigurasi yang sudah ada.

---

### 18. Halaman Admin - Transfer Bank (Bank Transfer Management)

Halaman Transfer Bank merupakan halaman yang digunakan oleh administrator untuk mengelola verifikasi pembayaran transfer bank yang dilakukan oleh pengguna ketika membeli paket kuota. Halaman ini menampilkan semua pembayaran yang memiliki status menunggu verifikasi, di mana untuk setiap pembayaran ditampilkan informasi berupa username pengguna yang melakukan pembelian, nama paket yang dibeli, nominal pembayaran yang harus diverifikasi, bukti pembayaran dalam bentuk gambar yang diunggah oleh pengguna, serta tanggal dan waktu kapan pembelian dilakukan. Administrator memiliki dua opsi utama dalam melakukan verifikasi pembayaran, yaitu approve atau menyetujui pembayaran yang akan menambahkan kuota sesuai paket yang dibeli ke akun pengguna, mengubah status pengguna menjadi Premium apabila sebelumnya berstatus Guest, mengupdate status pembelian menjadi "Disetujui", serta mengirimkan notifikasi melalui WhatsApp kepada pengguna, atau reject atau menolak pembayaran yang akan mengupdate status pembelian menjadi "Ditolak" dengan opsi untuk memberikan alasan penolakan.

---

## CATATAN PENTING

### Status User

Sistem U-Rank membedakan pengguna menjadi dua kategori status berdasarkan aktivitas pembelian mereka. Status pertama adalah Guest yang merupakan status default untuk pengguna baru yang baru saja melakukan registrasi dan belum pernah melakukan pembelian paket kuota. Pengguna dengan status Guest hanya dapat melakukan pengecekan ranking dasar dengan memanfaatkan tiga kuota gratis yang diberikan saat registrasi, namun tidak dapat mengakses fitur analisis SEO. Status kedua adalah Premium yang didapatkan oleh pengguna setelah mereka melakukan pembelian paket kuota dan pembayaran mereka telah disetujui oleh administrator. Pengguna dengan status Premium dapat menggunakan semua fitur yang tersedia dalam sistem, termasuk pengecekan ranking dan analisis SEO menggunakan artificial intelligence.

### Kuota

Kuota merupakan sistem pengukuran penggunaan layanan dalam sistem U-Rank yang menentukan seberapa banyak aktivitas yang dapat dilakukan oleh pengguna. Setiap aktivitas dalam sistem memiliki biaya kuota yang berbeda-beda. Untuk pengecekan ranking standar, sistem akan mengurangi satu kuota dari akun pengguna setiap kali pengecekan dilakukan. Untuk analisis SEO menggunakan artificial intelligence, biaya kuota yang dikenakan bervariasi sesuai dengan model AI yang dipilih, yaitu antara dua hingga lima kuota per analisis. Setiap pengguna baru yang melakukan registrasi akan secara otomatis menerima tiga kuota gratis yang dapat digunakan untuk pengecekan ranking dasar. Kuota akan bertambah ketika pengguna melakukan pembelian paket kuota dan pembayaran mereka telah diverifikasi dan disetujui oleh administrator sistem.

### Flow Pembayaran Transfer Bank

Proses pembayaran melalui transfer bank dalam sistem U-Rank mengikuti alur yang terstruktur untuk memastikan keamanan dan akurasi verifikasi. Proses dimulai ketika pengguna memilih paket kuota yang diinginkan dan memilih metode pembayaran transfer bank. Sistem kemudian akan membuat checkout session yang berlaku selama dua jam, di mana pengguna harus menyelesaikan pembayaran dalam waktu tersebut. Setelah checkout session dibuat, pengguna akan diarahkan ke halaman upload bukti pembayaran di mana mereka harus mengunggah screenshot atau foto bukti transfer bank mereka. Setelah bukti pembayaran diunggah, status pembelian akan berubah menjadi "Menunggu" dan menunggu proses verifikasi oleh administrator. Administrator akan memeriksa bukti pembayaran yang diunggah dan membandingkannya dengan informasi pembayaran yang seharusnya dilakukan. Apabila pembayaran disetujui, sistem akan secara otomatis menambahkan kuota ke akun pengguna sesuai dengan paket yang dibeli, mengubah status pengguna menjadi Premium, dan mengirimkan notifikasi konfirmasi melalui WhatsApp. Namun, apabila pembayaran ditolak, tidak ada kuota yang ditambahkan dan pengguna akan menerima notifikasi mengenai penolakan tersebut beserta alasan penolakan apabila diberikan oleh administrator.

---

**Dokumen ini dibuat untuk keperluan laporan sistem U-Rank.**
