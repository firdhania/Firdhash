# 📊 E-Commerce Brazil Analytics Dashboard
Dashboard interaktif untuk menganalisis data E-Commerce Brazil (Olist Dataset) dengan fokus pada:
1. Hubungan waktu pengiriman dengan kepuasan pelanggan
2. Hubungan lokasi seller dengan volume penjualan

## 🚀 Demo
Akses dashboard online di: [(https://firdhash-dashbo.streamlit.app/)]

## 📋 Fitur Utama
### 1. Overview Dashboard
- Ringkasan metrik utama (Total Orders, Produk Terjual, Total Seller, Rata-rata Rating)
- Ringkasan performa pengiriman (Lebih Cepat, Tepat Waktu, Terlambat)
- Ringkasan performa seller per kota dan negara bagian

### 2. Analisis Pengiriman (Pertanyaan 1)
- Rata-rata rating per status pengiriman
- Distribusi rating (stacked bar chart & pie chart)
- Analisis rentang keterlambatan
- Uji statistik (T-Test & ANOVA)

### 3. Detail Rating Pelanggan
- Distribusi rating keseluruhan
- Boxplot rating per status pengiriman
- Statistik deskriptif lengkap

### 4. Analisis Seller (Pertanyaan 2)
- Top 10 kota dengan penjualan tertinggi
- Korelasi jumlah seller vs total penjualan
- Produktivitas seller per kota
- Top 5 negara bagian dengan penjualan tertinggi

### 5. Analisis Lokasi Geografis
- Proporsi penjualan per negara bagian (pie chart)
- Jumlah seller per negara bagian
- Data lengkap per negara bagian

### 6. Kesimpulan & Rekomendasi
- Ringkasan temuan utama
- Rekomendasi bisnis strategis
- Action items prioritas

## 🛠️ Teknologi yang Digunakan

- **Python 3.14.4**
- **Streamlit** - Framework dashboard interaktif
- **Pandas** - Manipulasi dan analisis data
- **NumPy** - Komputasi numerik
- **Matplotlib** - Visualisasi data dasar
- **Seaborn** - Visualisasi data statistik
- **SciPy** - Uji statistik (T-Test, ANOVA, korelasi)

## 📁 Struktur Proyek
FUNDAMENTAL ANALISIS DATA
└── data/
|   ├── customers.csv
|   ├── geolocation.csv
|   ├── order_items.csv
|   ├── order_payments.csv
|   ├── order_reviews.csv
|   ├── orders.csv
|   ├── product_category.csv
|   ├── products.csv
|   └── sellers.csv
└── venv
|   ├── etc
|   ├── Include
|   ├── Lib
|   ├── Scripts
|   ├── share
|   ├── .gitignore
|   ├── pyvenv.cfg
└── dashboard.py
└── README.md
└── requirements.txt
└── url.txt

## 🚀 Panduan Menjalankan Aplikasi
## 1. Clone Repositori
Langkah pertama, unduh proyek ini ke komputer lokal Anda menggunakan perintah berikut:
git clone https://github.com/firdhania/Firdhash.git

## 2. Mengaktifkan Virtual Environment
Sebelum menjalankan dashboard, harus dipastikan bahwa virtual enviroment sudah aktif dengan:
python -m venv venv
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\venv\Scripts\Activate.ps1

## 3. Instalasi Library
Instal semua dependensi yang dibutuhkan menggunakan pip:
pip install -r requirements.txt

## 4. Menjalankan Dashboard
Jalankan perintah berikut pada terminal di dalam direktori proyek:
streamlit run dashboard.py
atau
python -m streamlit run dashboard.py
Aplikasi akan secara otomatis terbuka di browser default Anda.


## 🛠️ Persyaratan Sistem
- Python 3.8 atau lebih baru
- Pip (Python package manager)
- Minimal RAM 4GB (disarankan 8GB untuk performa optimal)
- Koneksi internet (untuk pertama kali install library)

## 📦 Daftar Library yang Diperlukan
Buat file `requirements.txt` dengan isi berikut:
streamlit
pandas
numpy
matplotlib
seaborn
scipy
datetime