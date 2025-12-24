# Konfigurasi umum untuk aplikasi analisis data Bebek 2024

# Data Bulan dan File
BULAN = ['jan','feb','mar','apr','mei','jun','jul','aug','sep','okt','nov','des']
FILES = [f'databebek2024/{b}24.xlsx' for b in BULAN]

# Produk yang dianalisis
PRODUK = ['bebek bakar 1 ekor','bebek bakar 1/2 ekor','ayam bakar 1 ekor','ayam bakar 1/2 ekor']

# Sheet names Excel
SHEET_PORSI = 'porsi '
SHEET_SALES = 'sales'

# Column indices
COL_KODE = 0        # Kolom kode produk (bbk, aym, th, tp)
COL_NAMA = 1        # Kolom nama produk/jenis
COL_JUMLAH = 65     # Kolom jumlah porsi
COL_PENDAPATAN = 5  # Kolom pendapatan

# Filter kode produk
KODE_PRODUK = ['bbk', 'aym', 'th', 'tp']

# Helper functions untuk mengurangi duplikasi kode

def generate_data_dummy(data, produk_list):
    """Generate data dummy jika data kosong"""
    for i, produk in enumerate(produk_list):
        data[produk] = [500 + j * (50 + i*20) for j in range(12)]
    return data

def hitung_error_prediksi(data_aktual, prediksi_func, start_index=3):
    """Hitung rata-rata error prediksi"""
    errors = [abs(prediksi_func(i) - data_aktual[i]) / data_aktual[i] * 100 if data_aktual[i] else 0 
              for i in range(start_index, len(data_aktual))]
    return sum(errors) / len(errors) if errors else 0

def format_response_algoritma(tertinggi, waktu, keys):
    """Format response untuk hasil algoritma pencarian"""
    result = {k: tertinggi[k] for k in keys}
    result['waktu'] = f"{waktu:.8f}"
    return result

def format_hasil_prediksi(produk, data, koef, nilai_awal, prediksi, rata_error, extra=None):
    """Format hasil prediksi untuk response JSON"""
    hasil = {
        'produk': produk,
        'koef': [f"{c:.4f}" for c in koef] if len(koef) <= 3 else [f"{c:.6f}" for c in koef],
        'sum_koef': f"{sum(koef):.4f}" if len(koef) <= 3 else f"{sum(koef):.6f}",
        'data_awal': [int(x) for x in data[:3]],
        'prediksi': {k: f"{v:.0f}" for k, v in prediksi.items()},
        'rata_rata_error': f"{rata_error:.2f}%"
    }
    if extra: hasil.update(extra)
    return hasil

# Matrix operations - digunakan oleh homogen & nonhomogen
def kali_matrix(A, B):
    """Perkalian matriks - O(k³)"""
    return [[sum(A[i][m] * B[m][j] for m in range(len(A))) for j in range(len(A))] for i in range(len(A))]

def pangkat_matrix(M, pangkat):
    """Eksponen matriks cepat - O(k³ log pangkat)"""
    hasil = [[1 if i == j else 0 for j in range(len(M))] for i in range(len(M))]
    base = [row[:] for row in M]
    while pangkat:
        if pangkat & 1: hasil = kali_matrix(hasil, base)
        base = kali_matrix(base, base)
        pangkat >>= 1
    return hasil

# Timing decorator
def timed(f):
    """Decorator untuk mengukur waktu eksekusi"""
    import time
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        return result, time.perf_counter() - start
    return wrapper

def hitung_waktu_algoritma(fungsi_cari, data):
    """Wrapper untuk mengukur waktu eksekusi fungsi"""
    import time
    mulai = time.perf_counter()
    hasil = fungsi_cari(data)
    waktu = time.perf_counter() - mulai
    return hasil, waktu

# Data reading - centralized logic
def baca_data_produk(files, produk_list):
    """Baca data produk dari multiple Excel files"""
    import pandas as pd
    data_per_produk = {produk: [] for produk in produk_list}
    for file in files:
        try:
            df = pd.read_excel(file, sheet_name=SHEET_PORSI, header=None)
            for produk in produk_list:
                total = sum(pd.to_numeric(row[COL_JUMLAH], errors='coerce') 
                          for _, row in df[df[COL_NAMA]==produk].iterrows() 
                          if pd.notna(row[COL_JUMLAH]))
                data_per_produk[produk].append(int(total))
        except: 
            for produk in produk_list: data_per_produk[produk].append(0)
    return data_per_produk
