# Analisis Usaha Bebek Bakar Ayayo 2024

Aplikasi web untuk menganalisis data penjualan usaha Bebek Bakar tahun 2024 menggunakan berbagai algoritma pencarian dan relasi rekurensi.

## Tentang Aplikasi

Aplikasi ini menganalisis:

- **Pendapatan Harian**: Mencari hari dengan pendapatan tertinggi
- **Menu Terlaris**: Produk paling laku sepanjang tahun
- **Relasi Rekurensi Homogen**: Prediksi penjualan menggunakan pola rekursif
- **Relasi Rekurensi Non-Homogen**: Prediksi dengan faktor eksternal
- **Analisis Performa**: Perbandingan kecepatan algoritma

## Struktur Proyek

```
tubes_aka/
├── databebek2024/           # Data Excel 12 bulan (jan24.xlsx - des24.xlsx)
├── app.py                   # Flask web server
├── app_pendapatan.py        # Modul analisis pendapatan
├── app_menuporsi_tahunan.py # Modul analisis menu
├── app_relasi_rekurensi_homogen.py
├── app_relasi_rekurensi_nonhomogen.py
├── config.py                # Konfigurasi & helper functions
├── static/                  # CSS & JavaScript
├── templates/               # HTML templates
└── requirements.txt
```

## Cara Instalasi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau manual:

```bash
pip install flask pandas openpyxl numpy
```

### 2. Jalankan Aplikasi

```bash
python app.py
```

### 3. Buka Browser

Akses aplikasi di: **http://127.0.0.1:5000**

## Algoritma yang Digunakan

### Pencarian Maksimum

- **Iteratif** - O(n): Scan linear untuk mencari nilai tertinggi
- **Rekursif (D&C)** - O(n): Divide & conquer untuk perbandingan

### Relasi Rekurensi

- **Iteratif** - O(n): Solusi step-by-step
- **Matrix Exponentiation** - O(k³ log n): Fast untuk n besar
- **Closed Form** - O(1): Solusi langsung menggunakan eigenvalue

## Fitur Utama

1. **Dashboard Interaktif**: Web interface yang user-friendly
2. **Perbandingan Algoritma**: Lihat perbedaan waktu eksekusi
3. **Statistik Lengkap**: Total, rata-rata, tertinggi, terendah
4. **Top 10 Ranking**: Menu dan pendapatan terbaik
5. **Prediksi Penjualan**: Menggunakan relasi rekurensi

## File Data

Aplikasi membaca dari folder `databebek2024/`:

- **12 file Excel** (jan24.xlsx sampai des24.xlsx)
- **Sheet `porsi`**: Data penjualan per menu
- **Sheet `sales`**: Data pendapatan harian

## Teknologi

- **Flask**: Web framework
- **Pandas**: Data processing
- **NumPy**: Komputasi numerik
- **JavaScript**: Frontend interaktivity

---

**Kelompok Bebekayayo - Tugas Besar AKA 2024**
