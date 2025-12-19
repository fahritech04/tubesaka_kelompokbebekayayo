# Analisis Relasi Rekurensi Linier Homogen pada Data Penjualan Produk

## Ringkasan Program

`app_relasi_rekurensi.py` adalah aplikasi untuk menganalisis pola penjualan produk menggunakan model relasi rekurensi linier homogen. Program membandingkan tiga metode komputasi yang berbeda dengan data historis 12 bulan untuk mengidentifikasi tren dan membuat prediksi akurat.

---

## Konsep Dasar

### Apa itu Relasi Rekurensi Linier Homogen?

Relasi rekurensi linier homogen menggambarkan suatu nilai berdasarkan nilai-nilai sebelumnya dengan pola tertentu. Bentuk umumnya adalah:

```
T(n) = a₁·T(n-1) + a₂·T(n-2) + ... + aₖ·T(n-k)
```

Dalam konteks penjualan, ini berarti jumlah penjualan bulan ke-n dipengaruhi oleh penjualan tiga bulan sebelumnya dengan bobot tertentu.

**Ciri-cirinya:**
- Linier: kombinasi langsung dari nilai-nilai sebelumnya
- Homogen: tidak ada nilai konstanta tambahan
- Koefisien bebas: nilai a₁, a₂, dst tidak perlu sama dengan 1

Contoh nyata: Jika penjualan bulan lalu 100 unit, dua bulan lalu 80 unit, dan tiga bulan lalu 60 unit, maka penjualan bulan ini bisa diprediksi sebagai 0.5×100 + 0.3×80 + 0.2×60 = 74 unit.

---

## Cara Kerja Program

### 1. Membaca Data dari Excel

Program membaca 12 file Excel (Januari-Desember 2024) dari folder `databebek2024/`. Setiap file berisi data penjualan per produk dalam sheet bernama `porsi`. Data diekstrak dari kolom 65 (jumlah) sesuai dengan nama produk yang dicari.

### 2. Menghitung Koefisien Otomatis

Dari 12 bulan data, program menggunakan metode **least squares** untuk mencari koefisien terbaik. Ini memastikan model yang dibuat meminimalkan perbedaan antara prediksi dan data aktual.

### 3. Menerapkan Tiga Metode Penyelesaian

Program menjalankan tiga algoritma berbeda untuk membandingkan efisiensi:

**a) Iteratif (O(n·k))** - Hitung satu per satu dari bulan awal hingga target
- Paling sederhana dan langsung dipahami
- Cocok untuk prediksi jangka pendek (< 100 bulan)
- Memori tumbuh seiring n yang diprediksi

**b) Matrix Exponentiation (O(k³·log n))** - Gunakan perkalian matrix dengan binary exponentiation
- Untuk prediksi jangka panjang (> 1000 bulan)
- Lebih canggih dan hemat waktu dengan n besar
- Memory usage tetap efisien

**c) Closed-Form (O(k³))** - Cari akar persamaan karakteristik dan hitung formula langsung
- Solusi analitik yang paling elegan
- Waktu konsisten tidak peduli berapa n
- Memory yang paling hemat

### 4. Validasi Hasil

Untuk memverifikasi akurasi model, program membandingkan prediksi dari ketiga metode terhadap data aktual bulan ke-4 sampai ke-12. Perbedaan dihitung sebagai persentase error.

---

## Struktur Output

Program menampilkan informasi dalam urutan berikut:

**1. Ringkasan Penjualan Per Produk**
- Total penjualan tahunan untuk setiap produk
- Rata-rata per bulan
- Persentase kontribusi terhadap total
- Status (sangat laku, cukup laku, dll)

**2. Rekomendasi Prioritas**
- Urutan produk berdasarkan volume penjualan
- Potensi peningkatan untuk setiap produk
- Aksi spesifik yang disarankan

**3. Analisis Per Produk**
Untuk masing-masing produk:
- Persamaan rekurensi yang terbentuk (koefisien)
- Prediksi penjualan untuk bulan 6, 9, dan 12 dari ketiga metode
- Tabel validasi dengan error percentage
- Rata-rata error overall

---

## Menggunakan Program

### Instalasi

Pastikan Python 3.8+ terinstal, lalu install dependencies:
```bash
pip install pandas numpy openpyxl
```

### Menjalankan

```bash
python app_relasi_rekurensi.py
```

Program otomatis membaca file Excel, menghitung koefisien, menjalankan analisis, dan menampilkan hasil lengkap di terminal.

### Mengubah Produk yang Dianalisis

Edit variabel `PRODUK` di bagian atas file dengan nama produk yang ingin dianalisis (harus sesuai dengan nama di Excel):

```python
PRODUK = ['bebek bakar 1 ekor', 'bebek bakar 1/2 ekor', 'ayam bakar 1 ekor']
```

---

## Interpretasi Hasil

### Koefisien Rekurensi

Koefisien yang ditampilkan menunjukkan pengaruh masing-masing bulan sebelumnya. Contoh:
```
T(n) = 0.5·T(n-1) + 0.3·T(n-2) + 0.2·T(n-3)
```

Artinya penjualan bulan ini dipengaruhi 50% dari bulan lalu, 30% dari dua bulan lalu, dan 20% dari tiga bulan lalu.

### Error Percentage

Error kecil (< 15%) menunjukkan model cukup akurat. Error besar mungkin karena:
- Variasi musiman yang tidak terprediksi
- Perubahan strategi bisnis mendadak
- Faktor eksternal (promosi, cuaca, dll)

### Pemilihan Metode

Dalam praktik, gunakan **Closed-Form** karena paling cepat dan elegan. Pilih **Iteratif** jika ingin pembelajaran lebih jelas tentang proses rekursi. Gunakan **Matrix** untuk keperluan research atau prediksi ekstrem.

---

## Penjelasan Teknis Singkat

**Least Squares:** Mencari koefisien yang membuat error keseluruhan paling kecil dengan meminimalkan jumlah kuadrat perbedaan antara prediksi dan data aktual.

**Companion Matrix:** Mengubah relasi rekurensi menjadi perkalian matrix sehingga bisa dikomputasi lebih efisien dengan teknik binary exponentiation.

**Persamaan Karakteristik:** Mengubah relasi rekurensi menjadi persamaan polinomial yang akarnya dapat digunakan untuk formula solusi langsung.

---

## Contoh Praktis

Jika program menunjukkan:
- Bebek bakar 1 ekor: 63% kontribusi, stabil
- Ayam bakar 1 ekor: 9% kontribusi, perlu promosi

Maka strategi bisnis bisa fokus pada:
1. Mempertahankan supply bebek bakar 1 ekor yang sudah top
2. Mengembangkan ayam bakar melalui promosi dan visibility lebih tinggi
3. Menggunakan prediksi untuk merencanakan inventory

---

## Catatan Penting

- Program mengasumsikan file Excel ada dan terstruktur benar
- Jika file tidak ditemukan, program menggunakan dummy data untuk demonstrasi
- Analisis membutuhkan minimal 4 data point untuk akurat
- Produk dengan penjualan 0 akan dilewati otomatis

---

**Versi:** 1.0 | **Status:** Siap Pakai | **Dibuat:** Desember 2025
