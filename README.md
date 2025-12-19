# 📊 Analisis Algoritma Pencarian - Tugas Besar AKA

Proyek ini menganalisis perbandingan algoritma **Iteratif** vs **Rekursif (Divide & Conquer)** untuk mencari nilai maksimum dalam dataset.

## 📁 Struktur Folder

```
tubes_aka/
├── databebek2024/              # Data Excel 12 bulan (Jan-Des 2024)
│   ├── jan24.xlsx
│   ├── feb24.xlsx
│   └── ... (10 bulan lainnya)
│
├── hasil_grafik/               # Output grafik analisis kompleksitas
│   ├── grafik_iteratif.png
│   ├── grafik_rekursif.png
│   └── grafik_perbandingan.png
│
├── app.py                      # Analisis menu terlaris (1 bulan)
├── app_tahunan.py             # Analisis menu terlaris (12 bulan)
├── app_pendapatan.py          # Analisis pendapatan harian (12 bulan)
├── grafik_analisis.py         # Grafik kompleksitas algoritma
│
├── menu_terlaris.csv          # Output: menu terlaris bulanan
├── menu_terlaris_tahunan.csv  # Output: menu terlaris tahunan
├── pendapatan_harian_2024.csv # Output: pendapatan harian
│
└── README.md                   # Dokumentasi (file ini)
```

---

## 🎯 File Program dan Fungsinya

### 1. **app.py** - Menu Terlaris Bulanan

Menganalisis menu terlaris dari **1 file Excel** (contoh: Januari 2024)

**Sumber Data:**

- File: `databebek2024/jan24.xlsx`
- Sheet: `porsi`
- Kolom yang dibaca:
  - Kolom 0: Kode menu (`bbk`, `aym`, `th`, `tp`)
  - Kolom 1: Nama menu
  - Kolom 65: Total porsi terjual

**Output:**

- Menu terlaris: `bebek bakar 1 ekor` (1,396 porsi)
- File CSV: `menu_terlaris.csv`

---

### 2. **app_tahunan.py** - Menu Terlaris Tahunan

Menganalisis menu terlaris dari **12 file Excel** (Januari-Desember 2024)

**Sumber Data:**

- File: Semua file `databebek2024/*.xlsx` (12 bulan)
- Sheet: `porsi`
- Cara kerja: Menjumlahkan penjualan tiap menu dari 12 bulan

**Contoh:**

```
bebek bakar 1 ekor:
- Jan: 1,396 porsi
- Feb: 1,582 porsi
- ... (10 bulan lainnya)
- Total: 18,964 porsi  ← Menu terlaris!
```

**Output:**

- Menu terlaris tahunan: `bebek bakar 1 ekor` (18,964 porsi)
- Top 10 menu terlaris
- File CSV: `menu_terlaris_tahunan.csv`

---

### 3. **app_pendapatan.py** - Pendapatan Harian Tertinggi

Menganalisis hari dengan pendapatan tertinggi dari **12 file Excel**

**Sumber Data:**

- File: Semua file `databebek2024/*.xlsx` (12 bulan)
- Sheet: `sales`
- Cara kerja:
  1. Cari baris dengan kolom 1 = `"kas"` (pendapatan harian)
  2. Ambil tanggal dari kolom 0
  3. Ambil jumlah pendapatan dari kolom 5

**Contoh struktur data sheet sales:**

```
Kolom 0         | Kolom 1  | Kolom 5
----------------|----------|----------
2024-01-01      | kas      | 98,000
2024-01-02      | kas      | 58,000
2024-04-27      | kas      | 1,156,000  ← Pendapatan tertinggi!
```

**Statistik yang Dihitung:**

1. **Pendapatan Tertinggi**

   - Mencari nilai maksimum dari kolom 5 (pendapatan)
   - Hasil: **27 April 2024** dengan **Rp 1,156,000**

2. **Pendapatan Terendah**

   - Mencari nilai minimum dari kolom 5
   - Hasil: **Rp 2,200** (hari dengan pendapatan paling rendah)

3. **Rata-rata Harian**

   - Formula: `Total Pendapatan ÷ Jumlah Hari Operasional`
   - Hasil: **Rp 170,556** per hari

4. **Total Pendapatan**
   - Menjumlahkan semua pendapatan harian
   - Hasil: **Rp 60,547,500** (dari 355 hari operasional)

**Output:**

- Hari dengan pendapatan tertinggi: 27 April 2024 (Rp 1,156,000)
- Top 10 hari dengan pendapatan terbaik
- Statistik lengkap (total, rata-rata, max, min)
- File CSV: `pendapatan_harian_2024.csv`

---

### 4. **grafik_analisis.py** - Analisis Kompleksitas Algoritma

Membuat grafik perbandingan performa **Iteratif** vs **Rekursif**

**Cara Kerja:**

1. **Perbesar Data**: Duplikasi data 20x (58 menu → 1,160 menu)
2. **Ukur Waktu**: Test dengan ukuran input 50, 100, 150, ..., 1160
3. **Stabilitas**: 500 percobaan per ukuran, buang 10% outlier
4. **Grafik**: Visualisasi pertumbuhan waktu eksekusi

**Output:**

- `grafik_iteratif.png` - Grafik algoritma iteratif
- `grafik_rekursif.png` - Grafik algoritma rekursif
- `grafik_perbandingan.png` - Perbandingan keduanya

---

## ⚙️ Algoritma yang Digunakan

### 1. **Algoritma Iteratif (Loop)**

```python
def cari_maksimum_iteratif(data):
    maksimum = data[0]
    for item in data[1:]:
        if item['jumlah'] > maksimum['jumlah']:
            maksimum = item
    return maksimum
```

- **Kompleksitas Waktu**: O(n)
- **Kompleksitas Ruang**: O(1)
- **Kelebihan**: Lebih cepat, efisien memori

### 2. **Algoritma Rekursif (Divide & Conquer)**

```python
def cari_maksimum_rekursif(data, kiri=0, kanan=None):
    if kiri == kanan:
        return data[kiri]

    tengah = (kiri + kanan) // 2
    maks_kiri = cari_maksimum_rekursif(data, kiri, tengah)
    maks_kanan = cari_maksimum_rekursif(data, tengah + 1, kanan)

    return maks_kiri if maks_kiri['jumlah'] > maks_kanan['jumlah'] else maks_kanan
```

- **Kompleksitas Waktu**: O(n)
- **Kompleksitas Ruang**: O(log n) - karena call stack
- **Kelebihan**: Pendekatan divide & conquer, cocok untuk paralel processing

---

## 📊 Hasil Analisis

### Menu Terlaris (Tahunan)

| Ranking | Menu                 | Total Terjual |
| ------- | -------------------- | ------------- |
| 1       | bebek bakar 1 ekor   | 18,964 porsi  |
| 2       | bebek goreng 1 ekor  | 11,964 porsi  |
| 3       | bebek bakar 1/2 ekor | 6,756 porsi   |

### Pendapatan Harian (Tahunan)

| Ranking | Tanggal       | Pendapatan   |
| ------- | ------------- | ------------ |
| 1       | 27 April 2024 | Rp 1,156,000 |
| 2       | 19 Juni 2024  | Rp 737,000   |
| 3       | 26 April 2024 | Rp 538,000   |

**Statistik Pendapatan 2024:**

- Total Hari Operasional: 355 hari
- Total Pendapatan: Rp 60,547,500
- Rata-rata Harian: Rp 170,556
- Pendapatan Tertinggi: Rp 1,156,000
- Pendapatan Terendah: Rp 2,200

### Performa Algoritma

- **Iteratif**: 0.075 ms (untuk 1,160 data)
- **Rekursif**: 0.493 ms (untuk 1,160 data)
- **Overhead Rekursif**: +552.9% (5.5x lebih lambat)

---

## 🚀 Cara Menjalankan

### Prerequisite

```bash
pip install pandas openpyxl matplotlib numpy
```

### Jalankan Program

1. **Analisis Menu Terlaris (Bulanan)**

```bash
python app.py
```

2. **Analisis Menu Terlaris (Tahunan)**

```bash
python app_tahunan.py
```

3. **Analisis Pendapatan Harian**

```bash
python app_pendapatan.py
```

4. **Buat Grafik Kompleksitas**

```bash
python grafik_analisis.py
```

---

## 📝 Penjelasan Detail Perhitungan Statistik

### A. Menu Terlaris

**Sumber**: Sheet `porsi`, Kolom 65 (Total Terjual)

Untuk menghitung menu terlaris tahunan:

```
Total = Σ (Penjualan Januari + Penjualan Februari + ... + Penjualan Desember)
```

Contoh: `bebek bakar 1 ekor`

- Januari: 1,396 porsi
- Februari: 1,582 porsi
- ... (10 bulan lainnya)
- **Total Tahunan: 18,964 porsi**

### B. Pendapatan Harian

**Sumber**: Sheet `sales`, baris dengan Kolom 1 = `"kas"`, ambil nilai Kolom 5

#### 1. Pendapatan Tertinggi

Mencari baris dengan nilai Kolom 5 paling besar:

```python
max(pendapatan_harian) = Rp 1,156,000 (27 April 2024)
```

#### 2. Pendapatan Terendah

Mencari baris dengan nilai Kolom 5 paling kecil:

```python
min(pendapatan_harian) = Rp 2,200
```

#### 3. Rata-rata Harian

```python
rata_rata = Total Pendapatan ÷ Jumlah Hari
         = Rp 60,547,500 ÷ 355 hari
         = Rp 170,556/hari
```

#### 4. Total Pendapatan

Menjumlahkan semua pendapatan harian dari 12 bulan:

```python
total = Σ (pendapatan_1 + pendapatan_2 + ... + pendapatan_355)
      = Rp 60,547,500
```

### C. Performa Algoritma

**Cara Pengukuran:**

1. Data diperbesar 20x (58 → 1,160 item)
2. Dijalankan 500 kali untuk tiap ukuran input
3. Buang 10% data outlier (50 terbesar & 50 terkecil)
4. Hitung rata-rata dari 400 percobaan sisanya

**Hasil:**

- Iteratif: 0.075 ms (lebih cepat)
- Rekursif: 0.493 ms (lebih lambat karena overhead function call)

---

## 🎓 Kesimpulan

1. **Menu Terlaris**: `bebek bakar 1 ekor` (18,964 porsi/tahun)
2. **Hari Terbaik**: 27 April 2024 (Rp 1,156,000)
3. **Algoritma Terbaik**: Iteratif (5.5x lebih cepat dari rekursif)
4. **Kompleksitas**: Kedua algoritma O(n), tapi iteratif lebih efisien dalam praktik

---

## 👨‍💻 Teknologi yang Digunakan

- **Python 3.10+**
- **Pandas**: Manipulasi data Excel
- **Matplotlib**: Visualisasi grafik
- **NumPy**: Perhitungan numerik
- **OpenPyXL**: Baca file .xlsx

---

## 📧 Kontak

Untuk pertanyaan atau feedback, silakan hubungi pembuat tugas besar ini.

---

**Dibuat untuk Tugas Besar Analisis Kompleksitas Algoritma**
