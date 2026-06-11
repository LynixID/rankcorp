/**
 * U-RANK Language Switcher
 * Supports: Bahasa Indonesia (id) & English (en)
 * Usage: add data-i18n="key" to any HTML element
 *        add data-i18n-placeholder="key" for input placeholders
 *        add data-i18n-title="key" for title attributes
 */

const TRANSLATIONS = {
  id: {
    // ===================== NAVBAR =====================
    nav_check_rank: "Cek Rank",
    nav_history: "Histori",
    nav_quota_label: "Kuota",
    nav_buy_quota: "Pembelian Kuota",
    nav_purchase_status: "Status Pembelian",
    nav_settings: "Pengaturan",
    nav_logout: "Logout",
    nav_menu: "Menu",
    nav_premium_badge: "Premium",
    nav_guest_badge: "Tamu",
    nav_lang_label: "ID",

    // ===================== LOGOUT MODAL =====================
    logout_modal_title: "Konfirmasi Logout",
    logout_modal_body: "Apakah Anda yakin ingin logout dari akun ini?",
    logout_modal_cancel: "Batal",
    logout_modal_confirm: "Logout",

    // ===================== LANDING PAGE =====================
    landing_title: "U-Rank - Pantau Ranking SEO Website Anda di Google Real-time",
    landing_nav_fitur: "Fitur",
    landing_nav_layanan: "Layanan",
    landing_nav_cara_kerja: "Cara Kerja",
    landing_nav_login: "Login",
    landing_nav_daftar: "Daftar Gratis",
    landing_hero_subtitle: "Pantau ranking SEO website Anda di Google dengan akurat dan real-time. Optimalkan strategi SEO dengan data yang tepat.",
    landing_hero_cta: "Mulai Gratis",
    landing_hero_learn: "Pelajari Lebih",
    landing_stat_akurat: "Akurat",
    landing_stat_verified: "Data Terverifikasi",
    landing_stat_instan: "Instan",
    landing_stat_update: "Update Ranking",
    landing_how_title: "Cara Kerja yang",
    landing_how_title_highlight: "Sederhana",
    landing_how_desc: "Dengan teknologi AI canggih, U-Rank memudahkan Anda untuk memantau dan menganalisis ranking website secara real-time. Proses yang cepat, akurat, dan mudah digunakan.",
    landing_step1_title: "Daftar & Login",
    landing_step1_desc: "Buat akun gratis dengan verifikasi OTP via WhatsApp",
    landing_step2_title: "Input Keyword & Domain",
    landing_step2_desc: "Masukkan keyword dan domain yang ingin Anda pantau",
    landing_step3_title: "Analisis & Optimasi",
    landing_step3_desc: "Dapatkan laporan ranking real-time dan optimalkan SEO Anda",
    landing_how_cta: "Coba Sekarang",
    landing_services_title: "Layanan",
    landing_services_title_highlight: "Unggulan",
    landing_services_subtitle: "Fitur-fitur canggih yang membantu Anda mengoptimalkan strategi SEO dengan lebih efektif",
    landing_service1_title: "Cek Ranking Real-time",
    landing_service1_desc: "Pantau posisi keyword dan domain website Anda di Google secara real-time dengan akurasi tinggi.",
    landing_service2_title: "Analisis SEO dengan AI",
    landing_service2_desc: "Dapatkan analisis mendalam menggunakan teknologi AI untuk optimasi SEO yang lebih baik.",
    landing_service3_title: "History & Trend",
    landing_service3_desc: "Lihat riwayat perubahan ranking dan analisis trend untuk strategi SEO jangka panjang.",
    landing_services_see_all: "Lihat Semua Fitur",
    landing_cta_title: "Siap Optimalkan SEO Anda?",
    landing_cta_desc: "Mulai pantau ranking website Anda sekarang dan dapatkan data akurat untuk strategi SEO yang lebih baik.",
    landing_cta_btn: "Daftar Gratis Sekarang",
    landing_footer_desc: "Alat monitoring ranking SEO real-time terdepan untuk membantu Anda menguasai hasil pencarian Google.",
    landing_footer_nav_title: "Navigasi",
    landing_footer_support_title: "Dukungan",
    landing_footer_help: "Pusat Bantuan",
    landing_footer_contact: "Kontak Kami",
    landing_footer_privacy: "Kebijakan Privasi",
    landing_footer_contact_title: "Hubungi Kami",
    landing_footer_copyright: "© 2025 U-Rank. Hak Cipta Dilindungi.",

    // ===================== LOGIN =====================
    login_title: "Masuk",
    login_subtitle: "Masuk ke akun Anda",
    login_username_placeholder: "Username Anda",
    login_remember: "Ingat Saya",
    login_forgot: "Lupa password?",
    login_btn: "Masuk",
    login_no_account: "Belum punya akun?",
    login_signup: "Daftar",

    // ===================== REGISTER =====================
    register_title: "Buat Akun",
    register_subtitle: "Daftar untuk memulai",
    register_username_placeholder: "Username Anda",
    register_email_placeholder: "Email Anda",
    register_btn: "Daftar",
    register_have_account: "Sudah punya akun?",
    register_signin: "Masuk",

    // ===================== VERIFY OTP =====================
    otp_title: "Verifikasi OTP",
    otp_subtitle: "Masukkan kode yang dikirim ke WhatsApp Anda",
    otp_label: "Kode OTP",
    otp_placeholder: "Masukkan 6 digit kode OTP",
    otp_btn: "Verifikasi",
    otp_resend: "Kirim ulang OTP",
    otp_back: "Kembali ke Registrasi",

    // ===================== SEARCH RANK =====================
    search_title: "Alat Profesional untuk",
    search_title_highlight: "Cek Ranking Website",
    search_title_suffix: "di Google",
    search_form_title: "Input Data Pencarian",
    search_history_label: "Histori Pencarian",
    search_history_show: "Tampilkan",
    search_history_placeholder: "Pilih histori pencarian...",
    search_keyword_label: "Kata Kunci",
    search_keyword_placeholder: "Contoh: harga laptop gaming 2024",
    search_domain_label: "Domain Target",
    search_domain_placeholder: "contoh: tokolaptop.com",
    search_serp_lang_label: "Bahasa SERP",
    search_country_label: "Negara",
    search_google_domain_label: "Google Domain",
    search_results_count_label: "Jumlah Hasil",
    search_btn: "Cek Rank Sekarang",
    search_result_title: "Hasil Pengecekan",
    search_result_domain: "Domain:",
    search_result_keyword: "Kata Kunci:",
    search_result_found: "Ditemukan di",
    search_result_position_from: "posisi dari",
    search_result_top: "hasil teratas.",
    search_col_position: "Posisi",
    search_col_url: "URL",
    search_not_found: "Domain tidak ditemukan dalam hasil pencarian.",
    search_not_found_hint: "Coba periksa kembali kata kunci atau domain Anda.",
    search_empty_title: "Siap untuk memulai?",
    search_empty_desc: "Masukkan detail pencarian Anda pada formulir di sebelah kiri.",
    search_modal_success: "Sukses!",
    search_modal_info: "Informasi",
    search_modal_warning: "Peringatan",
    search_modal_error: "Error!",
    search_modal_message: "Pesan",
    search_modal_close: "Tutup",

    // ===================== HISTORY SUMMARY =====================
    history_title: "Histori Pencarian SERP",
    history_col_keyword: "Kata Kunci",
    history_col_domain: "Domain",
    history_col_total: "Total Cek",
    history_col_action: "Aksi",
    history_empty: "Belum ada histori pencarian.",
    history_empty_sub: "Lakukan pengecekan rank pertama Anda!",
    history_cta: "Cek Rank Sekarang",

    // ===================== HISTORY DETAIL =====================
    history_detail_title: "Detail Performa Ranking",
    history_detail_keyword: "Kata Kunci:",
    history_detail_domain: "Domain:",
    history_detail_rank_trend: "Tren Ranking Historis",
    history_detail_rank_data: "Data Detail Ranking",
    history_detail_col_date: "Tanggal & Waktu",
    history_detail_col_url: "URL Hasil",
    history_detail_seo_analysis: "Analisa SEO",
    history_detail_analyze_btn: "Analisa SEO Website",
    history_detail_premium_hint: "Upgrade ke Premium untuk mengakses analisa SEO",
    history_detail_modal_title: "Konfirmasi Analisa SEO",
    history_detail_modal_body: "Analisa SEO akan menggunakan kuota dan memerlukan waktu beberapa detik. Lanjutkan analisa sekarang?",
    history_detail_modal_confirm: "Ya, Analisa",
    history_detail_empty: "Tidak ada data historis untuk kombinasi ini.",
    history_detail_empty_hint: "Pastikan Kata Kunci dan Domain sudah benar, atau lakukan pengecekan rank baru.",
    history_detail_back: "Kembali ke Ringkasan Histori",
    history_detail_proof_view: "Lihat",
    history_detail_proof_none: "Belum diunggah",

    // ===================== BUY QUOTA =====================
    quota_page_title: "Pilih Paket Pencarian",
    quota_page_title_highlight: "Terbaik",
    quota_page_title_suffix: "untuk Anda",
    quota_package_subtitle: "Solusi tepat untuk kebutuhan Anda.",
    quota_starting_from: "Mulai dari",
    quota_per_transaction: "per transaksi",
    quota_search_ultra: "Kuota Pencarian Ultra Cepat",
    quota_unlock_premium: "Buka Fitur Premium",
    quota_support: "Dukungan Penuh untuk SEO Lokal & Global",
    quota_integration: "Integrasi Mudah dengan Workflow Anda",
    quota_select_btn: "Pilih Paket Ini",
    quota_empty_title: "Ups! Belum Ada Paket Tersedia.",
    quota_empty_desc: "Kami sedang menyiapkan paket-paket terbaik untuk Anda. Silakan cek kembali nanti atau hubungi dukungan kami.",
    quota_modal_title: "Konfirmasi Pembelian",
    quota_modal_desc: "Anda akan diarahkan ke halaman pembayaran manual transfer bank.",
    quota_modal_info_title: "Informasi Penting:",
    quota_modal_info1: "• Sesi checkout berlaku selama 2 jam",
    quota_modal_info2: "• Pembayaran dilakukan via transfer bank manual",
    quota_modal_info3: "• Upload bukti transfer untuk konfirmasi",
    quota_modal_info4: "• Kuota akan ditambahkan setelah admin verifikasi",
    quota_modal_confirm: "Lanjutkan ke Pembayaran",
    quota_modal_cancel: "Batal",

    // ===================== PURCHASE STATUS =====================
    purchase_status_title: "Status Pembelian",
    purchase_status_col_date: "Tanggal",
    purchase_status_col_package: "Paket",
    purchase_status_col_price: "Harga",
    purchase_status_col_status: "Status",
    purchase_status_col_proof: "Bukti",
    purchase_status_col_action: "Aksi",
    purchase_status_pending: "Menunggu",
    purchase_status_approved: "Disetujui",
    purchase_status_rejected: "Ditolak",
    purchase_empty: "Belum ada riwayat pembelian.",
    purchase_empty_sub: "Mulai beli paket kuota untuk meningkatkan akun Anda",
    purchase_buy_btn: "Beli Paket Kuota",

    // ===================== UPLOAD PAYMENT =====================
    upload_title: "Upload Bukti Pembayaran",
    upload_subtitle: "Unggah bukti transfer Anda untuk konfirmasi pembayaran",
    upload_bank_info: "Informasi Rekening",
    upload_btn: "Upload Bukti Pembayaran",
    upload_cancel: "Batalkan & Kembali",

    // ===================== SEO ANALYSIS HISTORY =====================
    seo_history_title: "Riwayat Analisa SEO",
    seo_history_col_date: "Tanggal",
    seo_history_col_keyword: "Kata Kunci",
    seo_history_col_domain: "Domain",
    seo_history_col_model: "Model AI",
    seo_history_col_action: "Aksi",
    seo_history_empty: "Belum ada riwayat analisa SEO.",
    seo_history_view: "Lihat",

    // ===================== SEO ANALYSIS DETAIL =====================
    seo_detail_title: "Detail Analisa SEO",
    seo_detail_keyword: "Kata Kunci:",
    seo_detail_domain: "Domain:",
    seo_detail_model: "Model AI:",
    seo_detail_date: "Tanggal:",
    seo_detail_back: "Kembali",

    // ===================== DASHBOARD ADMIN =====================
    dashboard_title: "Dashboard Admin",
    dashboard_welcome: "Selamat Datang",
    dashboard_quota_used: "Kuota Digunakan",
    dashboard_quota_remaining: "Kuota Tersisa",
    dashboard_quota_total: "Total Kuota",
    dashboard_pending_approval: "Menunggu Persetujuan",
    dashboard_users: "Pengguna",
    dashboard_transactions: "Transaksi",
    dashboard_packages: "Paket",

    // ===================== DASHBOARD COMMON =====================
    dash_col_username: "Username",
    dash_col_email: "Email",
    dash_col_role: "Role",
    dash_col_status: "Status",
    dash_col_action: "Aksi",
    dash_col_date: "Tanggal",
    dash_col_amount: "Jumlah",
    dash_col_name: "Nama",
    dash_col_price: "Harga",
    dash_col_quota: "Kuota",
    dash_col_model: "Model",
    dash_btn_edit: "Edit",
    dash_btn_delete: "Hapus",
    dash_btn_approve: "Setujui",
    dash_btn_reject: "Tolak",
    dash_btn_add: "Tambah",
    dash_btn_save: "Simpan",
    dash_btn_cancel: "Batal",
    dash_btn_close: "Tutup",
    dash_search_placeholder: "Cari...",
    dash_empty: "Tidak ada data.",
    dash_premium: "Premium",
    dash_guest: "Tamu",
    dash_admin: "Admin",

    // ===================== UPDATE USER =====================
    update_user_title: "Edit Profil Pengguna",
    update_user_username: "Username",
    update_user_email: "Email",
    update_user_whatsapp: "Nomor WhatsApp",
    update_user_role: "Role",
    update_user_btn: "Simpan Perubahan",
    update_user_cancel: "Batal",
  },

  en: {
    // ===================== NAVBAR =====================
    nav_check_rank: "Check Rank",
    nav_history: "History",
    nav_quota_label: "Quota",
    nav_buy_quota: "Buy Quota",
    nav_purchase_status: "Purchase Status",
    nav_settings: "Settings",
    nav_logout: "Logout",
    nav_menu: "Menu",
    nav_premium_badge: "Premium",
    nav_guest_badge: "Guest",
    nav_lang_label: "EN",

    // ===================== LOGOUT MODAL =====================
    logout_modal_title: "Confirm Logout",
    logout_modal_body: "Are you sure you want to logout from this account?",
    logout_modal_cancel: "Cancel",
    logout_modal_confirm: "Logout",

    // ===================== LANDING PAGE =====================
    landing_title: "U-Rank - Monitor Your Website SEO Ranking on Google in Real-time",
    landing_nav_fitur: "Features",
    landing_nav_layanan: "Services",
    landing_nav_cara_kerja: "How It Works",
    landing_nav_login: "Login",
    landing_nav_daftar: "Sign Up Free",
    landing_hero_subtitle: "Monitor your website's SEO ranking on Google accurately and in real-time. Optimize your SEO strategy with the right data.",
    landing_hero_cta: "Get Started Free",
    landing_hero_learn: "Learn More",
    landing_stat_akurat: "Accurate",
    landing_stat_verified: "Verified Data",
    landing_stat_instan: "Instant",
    landing_stat_update: "Rank Update",
    landing_how_title: "A",
    landing_how_title_highlight: "Simple",
    landing_how_desc: "With advanced AI technology, U-Rank makes it easy for you to monitor and analyze website rankings in real-time. Fast, accurate, and easy to use.",
    landing_step1_title: "Sign Up & Login",
    landing_step1_desc: "Create a free account with OTP verification via WhatsApp",
    landing_step2_title: "Input Keyword & Domain",
    landing_step2_desc: "Enter the keyword and domain you want to monitor",
    landing_step3_title: "Analyze & Optimize",
    landing_step3_desc: "Get real-time ranking reports and optimize your SEO",
    landing_how_cta: "Try Now",
    landing_services_title: "Our",
    landing_services_title_highlight: "Features",
    landing_services_subtitle: "Advanced features that help you optimize your SEO strategy more effectively",
    landing_service1_title: "Real-time Rank Check",
    landing_service1_desc: "Monitor the position of your website keyword and domain on Google in real-time with high accuracy.",
    landing_service2_title: "AI-Powered SEO Analysis",
    landing_service2_desc: "Get in-depth analysis using AI technology for better SEO optimization.",
    landing_service3_title: "History & Trend",
    landing_service3_desc: "View ranking change history and trend analysis for long-term SEO strategy.",
    landing_services_see_all: "See All Features",
    landing_cta_title: "Ready to Optimize Your SEO?",
    landing_cta_desc: "Start monitoring your website ranking now and get accurate data for a better SEO strategy.",
    landing_cta_btn: "Sign Up Free Now",
    landing_footer_desc: "The leading real-time SEO ranking monitoring tool to help you dominate Google search results.",
    landing_footer_nav_title: "Navigation",
    landing_footer_support_title: "Support",
    landing_footer_help: "Help Center",
    landing_footer_contact: "Contact Us",
    landing_footer_privacy: "Privacy Policy",
    landing_footer_contact_title: "Contact Us",
    landing_footer_copyright: "© 2025 U-Rank. All Rights Reserved.",

    // ===================== LOGIN =====================
    login_title: "Welcome Back",
    login_subtitle: "Sign in to your account",
    login_username_placeholder: "Your username",
    login_remember: "Remember me",
    login_forgot: "Forgot password?",
    login_btn: "Sign In",
    login_no_account: "Don't have an account?",
    login_signup: "Sign up",

    // ===================== REGISTER =====================
    register_title: "Create Account",
    register_subtitle: "Sign up to get started",
    register_username_placeholder: "Your username",
    register_email_placeholder: "Your email",
    register_btn: "Sign Up",
    register_have_account: "Already have an account?",
    register_signin: "Sign in",

    // ===================== VERIFY OTP =====================
    otp_title: "OTP Verification",
    otp_subtitle: "Enter the code sent to your WhatsApp",
    otp_label: "OTP Code",
    otp_placeholder: "Enter 6-digit OTP code",
    otp_btn: "Verify",
    otp_resend: "Resend OTP",
    otp_back: "Back to Registration",

    // ===================== SEARCH RANK =====================
    search_title: "Professional Tool to",
    search_title_highlight: "Check Website Ranking",
    search_title_suffix: "on Google",
    search_form_title: "Search Input",
    search_history_label: "Search History",
    search_history_show: "Show",
    search_history_placeholder: "Select search history...",
    search_keyword_label: "Keyword",
    search_keyword_placeholder: "Example: best gaming laptop 2024",
    search_domain_label: "Target Domain",
    search_domain_placeholder: "example: tokolaptop.com",
    search_serp_lang_label: "SERP Language",
    search_country_label: "Country",
    search_google_domain_label: "Google Domain",
    search_results_count_label: "Number of Results",
    search_btn: "Check Rank Now",
    search_result_title: "Check Results",
    search_result_domain: "Domain:",
    search_result_keyword: "Keyword:",
    search_result_found: "Found at",
    search_result_position_from: "positions from",
    search_result_top: "top results.",
    search_col_position: "Position",
    search_col_url: "URL",
    search_not_found: "Domain not found in search results.",
    search_not_found_hint: "Please re-check your keyword or domain.",
    search_empty_title: "Ready to start?",
    search_empty_desc: "Enter your search details in the form on the left.",
    search_modal_success: "Success!",
    search_modal_info: "Information",
    search_modal_warning: "Warning",
    search_modal_error: "Error!",
    search_modal_message: "Message",
    search_modal_close: "Close",

    // ===================== HISTORY SUMMARY =====================
    history_title: "SERP Search History",
    history_col_keyword: "Keyword",
    history_col_domain: "Domain",
    history_col_total: "Total Checks",
    history_col_action: "Action",
    history_empty: "No search history yet.",
    history_empty_sub: "Do your first rank check!",
    history_cta: "Check Rank Now",

    // ===================== HISTORY DETAIL =====================
    history_detail_title: "Ranking Performance Detail",
    history_detail_keyword: "Keyword:",
    history_detail_domain: "Domain:",
    history_detail_rank_trend: "Historical Ranking Trend",
    history_detail_rank_data: "Ranking Detail Data",
    history_detail_col_date: "Date & Time",
    history_detail_col_url: "Result URL",
    history_detail_seo_analysis: "SEO Analysis",
    history_detail_analyze_btn: "Analyze SEO Website",
    history_detail_premium_hint: "Upgrade to Premium to access SEO analysis",
    history_detail_modal_title: "Confirm SEO Analysis",
    history_detail_modal_body: "SEO analysis will use quota and take a few seconds. Continue analysis now?",
    history_detail_modal_confirm: "Yes, Analyze",
    history_detail_empty: "No historical data for this combination.",
    history_detail_empty_hint: "Make sure the Keyword and Domain are correct, or do a new rank check.",
    history_detail_back: "Back to History Summary",
    history_detail_proof_view: "View",
    history_detail_proof_none: "Not uploaded yet",

    // ===================== BUY QUOTA =====================
    quota_page_title: "Choose the",
    quota_page_title_highlight: "Best",
    quota_page_title_suffix: "Search Package for You",
    quota_package_subtitle: "The right solution for your needs.",
    quota_starting_from: "Starting from",
    quota_per_transaction: "per transaction",
    quota_search_ultra: "Ultra-Fast Search Quota",
    quota_unlock_premium: "Unlock Premium Features",
    quota_support: "Full Support for Local & Global SEO",
    quota_integration: "Easy Integration with Your Workflow",
    quota_select_btn: "Choose This Package",
    quota_empty_title: "Oops! No Packages Available Yet.",
    quota_empty_desc: "We're preparing the best packages for you. Please check back later or contact our support.",
    quota_modal_title: "Purchase Confirmation",
    quota_modal_desc: "You will be redirected to the manual bank transfer payment page.",
    quota_modal_info_title: "Important Information:",
    quota_modal_info1: "• Checkout session is valid for 2 hours",
    quota_modal_info2: "• Payment is made via manual bank transfer",
    quota_modal_info3: "• Upload transfer proof for confirmation",
    quota_modal_info4: "• Quota will be added after admin verification",
    quota_modal_confirm: "Proceed to Payment",
    quota_modal_cancel: "Cancel",

    // ===================== PURCHASE STATUS =====================
    purchase_status_title: "Purchase Status",
    purchase_status_col_date: "Date",
    purchase_status_col_package: "Package",
    purchase_status_col_price: "Price",
    purchase_status_col_status: "Status",
    purchase_status_col_proof: "Proof",
    purchase_status_col_action: "Action",
    purchase_status_pending: "Pending",
    purchase_status_approved: "Approved",
    purchase_status_rejected: "Rejected",
    purchase_empty: "No purchase history yet.",
    purchase_empty_sub: "Start buying a quota package to upgrade your account",
    purchase_buy_btn: "Buy Quota Package",

    // ===================== UPLOAD PAYMENT =====================
    upload_title: "Upload Payment Proof",
    upload_subtitle: "Upload your transfer proof for payment confirmation",
    upload_bank_info: "Account Information",
    upload_btn: "Upload Payment Proof",
    upload_cancel: "Cancel & Go Back",

    // ===================== SEO ANALYSIS HISTORY =====================
    seo_history_title: "SEO Analysis History",
    seo_history_col_date: "Date",
    seo_history_col_keyword: "Keyword",
    seo_history_col_domain: "Domain",
    seo_history_col_model: "AI Model",
    seo_history_col_action: "Action",
    seo_history_empty: "No SEO analysis history yet.",
    seo_history_view: "View",

    // ===================== SEO ANALYSIS DETAIL =====================
    seo_detail_title: "SEO Analysis Detail",
    seo_detail_keyword: "Keyword:",
    seo_detail_domain: "Domain:",
    seo_detail_model: "AI Model:",
    seo_detail_date: "Date:",
    seo_detail_back: "Back",

    // ===================== DASHBOARD ADMIN =====================
    dashboard_title: "Admin Dashboard",
    dashboard_welcome: "Welcome",
    dashboard_quota_used: "Used Quota",
    dashboard_quota_remaining: "Remaining Quota",
    dashboard_quota_total: "Total Quota",
    dashboard_pending_approval: "Pending Approval",
    dashboard_users: "Users",
    dashboard_transactions: "Transactions",
    dashboard_packages: "Packages",

    // ===================== DASHBOARD COMMON =====================
    dash_col_username: "Username",
    dash_col_email: "Email",
    dash_col_role: "Role",
    dash_col_status: "Status",
    dash_col_action: "Action",
    dash_col_date: "Date",
    dash_col_amount: "Amount",
    dash_col_name: "Name",
    dash_col_price: "Price",
    dash_col_quota: "Quota",
    dash_col_model: "Model",
    dash_btn_edit: "Edit",
    dash_btn_delete: "Delete",
    dash_btn_approve: "Approve",
    dash_btn_reject: "Reject",
    dash_btn_add: "Add",
    dash_btn_save: "Save",
    dash_btn_cancel: "Cancel",
    dash_btn_close: "Close",
    dash_search_placeholder: "Search...",
    dash_empty: "No data available.",
    dash_premium: "Premium",
    dash_guest: "Guest",
    dash_admin: "Admin",

    // ===================== UPDATE USER =====================
    update_user_title: "Edit User Profile",
    update_user_username: "Username",
    update_user_email: "Email",
    update_user_whatsapp: "WhatsApp Number",
    update_user_role: "Role",
    update_user_btn: "Save Changes",
    update_user_cancel: "Cancel",
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// Core i18n Engine
// ─────────────────────────────────────────────────────────────────────────────

const LANG_KEY = "urank_language";

function getCurrentLang() {
  return localStorage.getItem(LANG_KEY) || "id";
}

function applyLanguage(lang) {
  if (!lang) lang = getCurrentLang();
  const t = TRANSLATIONS[lang] || TRANSLATIONS["id"];

  // Apply text content
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (t[key] !== undefined) {
      el.textContent = t[key];
    }
  });

  // Apply placeholder attributes
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (t[key] !== undefined) {
      el.placeholder = t[key];
    }
  });

  // Apply title attributes
  document.querySelectorAll("[data-i18n-title]").forEach((el) => {
    const key = el.getAttribute("data-i18n-title");
    if (t[key] !== undefined) {
      el.title = t[key];
    }
  });

  // Update html lang attribute
  document.documentElement.lang = lang === "en" ? "en" : "id";

  // Update active state of language buttons
  document.querySelectorAll(".lang-btn").forEach((btn) => {
    const btnLang = btn.getAttribute("data-lang");
    if (btnLang === lang) {
      btn.classList.add("lang-btn-active");
    } else {
      btn.classList.remove("lang-btn-active");
    }
  });

  // Store
  localStorage.setItem(LANG_KEY, lang);
}

function setLanguage(lang) {
  applyLanguage(lang);
  // Close lang dropdown if open
  const dd = document.getElementById("langDropdown");
  if (dd) dd.classList.add("hidden");
}

function toggleLangDropdown(e) {
  e.stopPropagation();
  const dd = document.getElementById("langDropdown");
  if (dd) dd.classList.toggle("hidden");
}

// Auto-apply on DOM ready
document.addEventListener("DOMContentLoaded", function () {
  applyLanguage(getCurrentLang());

  // Close lang dropdown on outside click
  document.addEventListener("click", function (e) {
    const dd = document.getElementById("langDropdown");
    const trigger = document.getElementById("langSwitcherBtn");
    if (dd && trigger && !trigger.contains(e.target) && !dd.contains(e.target)) {
      dd.classList.add("hidden");
    }
  });
});
