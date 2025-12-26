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

def ukur_waktu(func, *args, runs=100):
    """Ukur waktu rata-rata dari multiple runs - untuk benchmark"""
    import time
    waktu_list = []
    for _ in range(runs):
        start = time.perf_counter()
        result = func(*args)
        waktu_list.append((time.perf_counter() - start) * 1000)  # ms
    return result, sum(waktu_list) / len(waktu_list)

def bikin_data_random(size, tipe='pendapatan'):
    """Generate random data untuk testing performance"""
    import random
    if tipe == 'pendapatan':
        return [{'tanggal': f'2024-01-{(i%28)+1:02d}', 'pendapatan': random.randint(100000, 1000000)} 
                for i in range(size)]
    elif tipe == 'menu':
        return [{'nama': f'Menu {i}', 'jumlah': random.randint(10, 500)} 
                for i in range(size)]
    return []

def benchmark_algo(func, data):
    """Quick benchmark - return execution time in ms"""
    import time
    start = time.perf_counter()
    func(data)
    return (time.perf_counter() - start) * 1000

def benchmark_simple(func):
    """Benchmark untuk fungsi tanpa parameter - return execution time in ms"""
    import time
    start = time.perf_counter()
    func()
    return (time.perf_counter() - start) * 1000

# Helper untuk test pencarian exact match (digunakan oleh pendapatan & menu)
def cari_exact_iteratif(data, target_key, target_value):
    """Cari semua item dengan nilai exact match - iteratif"""
    return [item for item in data if item[target_key] == target_value] or None

def cari_exact_rekursif(data, target_key, target_value, idx=0, hasil=None):
    """Cari semua item dengan nilai exact match - rekursif"""
    if hasil is None:
        hasil = []
    if idx >= len(data):
        return hasil or None
    if data[idx][target_key] == target_value:
        hasil.append(data[idx])
    return cari_exact_rekursif(data, target_key, target_value, idx + 1, hasil)

def build_test_response(target, data, hasil_iter, hasil_rek, waktu_iter, waktu_rek, not_found_msg):
    """Build response untuk test pencarian"""
    if not hasil_iter or not hasil_rek:
        return {'target': target, 'total_data': len(data), 'found': False, 'message': not_found_msg}
    
    winner = 'Iteratif' if waktu_iter < waktu_rek else 'Rekursif'
    return {
        'target': target, 'total_data': len(data), 'found': True, 'jumlah_hasil': len(hasil_iter),
        'iteratif': {'hasil': hasil_iter, 'waktu_ms': waktu_iter, 'waktu_str': f'{waktu_iter:.4f} ms'},
        'rekursif': {'hasil': hasil_rek, 'waktu_ms': waktu_rek, 'waktu_str': f'{waktu_rek:.4f} ms'},
        'perbandingan': {
            'winner': winner,
            'selisih_persen': abs((waktu_rek - waktu_iter) / waktu_iter * 100),
            'lebih_cepat': f'{waktu_rek / waktu_iter:.2f}x' if waktu_iter < waktu_rek else f'{waktu_iter / waktu_rek:.2f}x'
        }
    }

# Helper untuk endpoint pencarian maksimum (pendapatan & menu)
def proses_pencarian_max(data_list, func_iter, func_rek, sort_key, response_keys):
    """Generic handler untuk pencarian maksimum iteratif vs rekursif"""
    if not data_list: return None
    
    data_sorted = sorted(data_list, key=lambda x: x[sort_key], reverse=True)
    tertinggi_it, waktu_it = hitung_waktu_algoritma(func_iter, data_list)
    tertinggi_rk, waktu_rk = hitung_waktu_algoritma(func_rek, data_list)
    
    return {
        'top10': data_sorted[:10],
        'iteratif': format_response_algoritma(tertinggi_it, waktu_it, response_keys),
        'rekursif': format_response_algoritma(tertinggi_rk, waktu_rk, response_keys)
    }

# Helper untuk endpoint relasi rekurensi
def proses_relasi_rekurensi(data, produk_list, tipe='homogen'):
    """Generic handler untuk relasi rekurensi homogen & nonhomogen"""
    if all(sum(data.get(p, [0])) == 0 for p in produk_list): 
        data = generate_data_dummy(data, produk_list)
    
    hasil = []
    for p in produk_list:
        d = data.get(p, [])
        if sum(d) == 0 or len(d) < 4: continue
        
        nilai_awal = [float(x) for x in d[:3]]
        
        if tipe == 'homogen':
            from app_relasi_rekurensi_homogen import hitung_koefisien, solve_iteratif, solve_matrix, solve_closed_form
            koef = hitung_koefisien(d)
            prediksi = {
                'iteratif': solve_iteratif(nilai_awal, koef, 12)[0],
                'matrix': solve_matrix(nilai_awal, koef, 12)[0],
                'closed': solve_closed_form(nilai_awal, koef, 12)[0]
            }
            rata_error = hitung_error_prediksi(d, lambda i: solve_iteratif(nilai_awal, koef, i)[0])
            hasil.append(format_hasil_prediksi(p, d, koef, nilai_awal, prediksi, rata_error))
        else:  # nonhomogen
            from app_relasi_rekurensi_nonhomogen import hitung_koef_nonhom, solve
            koef, nilai_f = hitung_koef_nonhom(d)
            prediksi = {
                'bulan_6': solve(nilai_awal, koef, nilai_f, 6, 'iteratif'),
                'bulan_12': solve(nilai_awal, koef, nilai_f, 12, 'iteratif')
            }
            rata_error = hitung_error_prediksi(d, lambda i: solve(nilai_awal, koef, nilai_f, i, 'iteratif'))
            is_nonhomogen = abs(sum(nilai_f[3:]))/(sum(d[3:])+0.1)*100 > 5
            extra = {
                'f_n': [f"{x:.0f}" for x in nilai_f[3:]],
                'status': 'VALID NON-HOMOGEN' if is_nonhomogen else 'Dominan HOMOGEN'
            }
            hasil.append(format_hasil_prediksi(p, d, koef, nilai_awal, prediksi, rata_error, extra))
    
    return hasil

# Helper untuk demo comparison
def jalankan_demo_pencarian(sizes, func_iter, func_rek):
    """Demo perbandingan pencarian maksimum"""
    results = []
    for size in sizes:
        data = bikin_data_random(size, 'pendapatan')
        _, waktu_iter = ukur_waktu(func_iter, data, runs=100)
        _, waktu_rek = ukur_waktu(func_rek, data, runs=100)
        overhead = (waktu_rek / waktu_iter - 1) * 100
        results.append({
            'size': size, 'iteratif': waktu_iter, 'rekursif': waktu_rek,
            'overhead': overhead, 'winner': 'Iteratif' if waktu_iter < waktu_rek else 'Rekursif'
        })
    return results

def jalankan_demo_relasi(ns, v, koef, func_iter, func_matrix, func_closed):
    """Demo perbandingan relasi rekurensi"""
    results = []
    for n in ns:
        _, waktu_iter = ukur_waktu(func_iter, v, koef, n, runs=50)
        _, waktu_matrix = ukur_waktu(func_matrix, v, koef, n, runs=50)
        _, waktu_closed = ukur_waktu(func_closed, v, koef, n, runs=50)
        times = {'Iteratif': waktu_iter, 'Matrix': waktu_matrix, 'Closed': waktu_closed}
        winner = min(times, key=times.get)
        results.append({
            'n': n, 'iteratif': waktu_iter, 'matrix': waktu_matrix,
            'closed': waktu_closed, 'winner': winner
        })
    return results

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

# Test endpoint helpers
def handle_test_homogen(n):
    """Handler untuk test-relasi-homogen"""
    from app_relasi_rekurensi_homogen import solve_iteratif, solve_matrix, solve_closed_form
    v, koef = [500.0, 550.0, 600.0], [0.5, 0.3, 0.2]
    hasil_iter, waktu_iter = ukur_waktu(solve_iteratif, v, koef, n, runs=30)
    hasil_matrix, waktu_matrix = ukur_waktu(solve_matrix, v, koef, n, runs=30)
    hasil_closed, waktu_closed = ukur_waktu(solve_closed_form, v, koef, n, runs=30)
    times = {'Iteratif': waktu_iter, 'Matrix': waktu_matrix, 'Closed': waktu_closed}
    winner = min(times, key=times.get)
    return {
        'n': n, 'nilai_awal': v, 'koefisien': koef,
        'iteratif': {'hasil': hasil_iter[0], 'waktu_ms': waktu_iter, 'waktu_str': f'{waktu_iter:.4f} ms'},
        'matrix': {'hasil': hasil_matrix[0], 'waktu_ms': waktu_matrix, 'waktu_str': f'{waktu_matrix:.4f} ms'},
        'closed': {'hasil': hasil_closed[0], 'waktu_ms': waktu_closed, 'waktu_str': f'{waktu_closed:.4f} ms'},
        'perbandingan': {
            'winner': winner,
            'iteratif_vs_matrix': f'{waktu_iter / waktu_matrix:.2f}x' if waktu_matrix < waktu_iter else f'{waktu_matrix / waktu_iter:.2f}x',
            'iteratif_vs_closed': f'{waktu_iter / waktu_closed:.2f}x' if waktu_closed < waktu_iter else f'{waktu_closed / waktu_iter:.2f}x'
        }
    }

def handle_test_nonhomogen(n):
    """Handler untuk test-relasi-nonhomogen"""
    import random
    from app_relasi_rekurensi_nonhomogen import solve
    v, koef = [500.0, 550.0, 600.0], [0.5, 0.3, 0.2]
    nilai_f = [random.uniform(10, 100) for _ in range(n + 3)]
    hasil, waktu = ukur_waktu(solve, v, koef, nilai_f, n, 'iteratif', runs=30)
    return {
        'n': n, 'nilai_awal': v, 'koefisien': koef, 'f_samples': nilai_f[3:8],
        'hasil': {'nilai': hasil, 'waktu_ms': waktu, 'waktu_str': f'{waktu:.4f} ms'},
        'info': f'Prediksi bulan ke-{n} dengan faktor eksternal f(n)'
    }

def handle_prediksi_produk(produk_idx, n, tipe='homogen'):
    """Handler untuk prediksi produk individual dengan n dinamis"""
    from app_relasi_rekurensi_homogen import baca_data_excel
    data = baca_data_excel()
    
    produk = PRODUK[produk_idx]
    d = data.get(produk, [])
    if sum(d) == 0 or len(d) < 4:
        return {'error': 'Data tidak tersedia'}
    
    nilai_awal = [float(x) for x in d[:3]]
    
    if tipe == 'homogen':
        from app_relasi_rekurensi_homogen import hitung_koefisien, solve_iteratif, solve_matrix, solve_closed_form
        koef = hitung_koefisien(d)
        
        # Ukur waktu untuk perbandingan
        hasil_iter, waktu_iter = ukur_waktu(solve_iteratif, nilai_awal, koef, n, runs=30)
        hasil_matrix, waktu_matrix = ukur_waktu(solve_matrix, nilai_awal, koef, n, runs=30)
        hasil_closed, waktu_closed = ukur_waktu(solve_closed_form, nilai_awal, koef, n, runs=30)
        
        times = {'Iteratif': waktu_iter, 'Matrix': waktu_matrix, 'Closed': waktu_closed}
        winner = min(times, key=times.get)
        
        return {
            'produk': produk, 'n': n,
            'iteratif': {'hasil': f"{hasil_iter[0]:.0f}", 'waktu_ms': waktu_iter, 'waktu_str': f'{waktu_iter:.4f} ms'},
            'matrix': {'hasil': f"{hasil_matrix[0]:.0f}", 'waktu_ms': waktu_matrix, 'waktu_str': f'{waktu_matrix:.4f} ms'},
            'closed': {'hasil': f"{hasil_closed[0]:.0f}", 'waktu_ms': waktu_closed, 'waktu_str': f'{waktu_closed:.4f} ms'},
            'perbandingan': {
                'winner': winner,
                'iteratif_vs_matrix': f'{waktu_iter / waktu_matrix:.2f}x' if waktu_matrix < waktu_iter else f'{waktu_matrix / waktu_iter:.2f}x',
                'iteratif_vs_closed': f'{waktu_iter / waktu_closed:.2f}x' if waktu_closed < waktu_iter else f'{waktu_closed / waktu_iter:.2f}x'
            }
        }
    else:  # nonhomogen
        from app_relasi_rekurensi_nonhomogen import hitung_koef_nonhom, solve
        koef, nilai_f = hitung_koef_nonhom(d)
        hasil, waktu = ukur_waktu(solve, nilai_awal, koef, nilai_f, n, 'iteratif', runs=30)
        return {
            'produk': produk, 'n': n,
            'hasil': {'nilai': f"{hasil:.0f}", 'waktu_ms': waktu, 'waktu_str': f'{waktu:.4f} ms'}
        }

def handle_performance_analysis(n):
    """Handler untuk performance-analysis endpoint"""
    import random
    from app_pendapatan import cari_pendapatan_tertinggi_iteratif, cari_pendapatan_tertinggi_rekursif
    from app_menuporsi_tahunan import cari_menu_terlaris_iteratif, cari_menu_terlaris_rekursif
    from app_relasi_rekurensi_homogen import solve_iteratif, solve_matrix
    from app_relasi_rekurensi_nonhomogen import solve
    
    sizes = [s for s in [1,10,20,50,100,500,1000,5000,10000,50000,100000] if s <= n]
    if n not in sizes: sizes.append(n)
    sizes.sort()
    
    hasil = {
        'sizes': sizes, 'iteratif_pendapatan': [], 'rekursif_pendapatan': [],
        'iteratif_menu': [], 'rekursif_menu': [],
        'iteratif_homogen': [], 'matrix_homogen': [], 'nonhomogen': []
    }
    
    for size in sizes:
        hasil['iteratif_pendapatan'].append(benchmark_algo(cari_pendapatan_tertinggi_iteratif, bikin_data_random(size, 'pendapatan')))
        hasil['rekursif_pendapatan'].append(benchmark_algo(cari_pendapatan_tertinggi_rekursif, bikin_data_random(size, 'pendapatan')))
        hasil['iteratif_menu'].append(benchmark_algo(cari_menu_terlaris_iteratif, bikin_data_random(size, 'menu')))
        hasil['rekursif_menu'].append(benchmark_algo(cari_menu_terlaris_rekursif, bikin_data_random(size, 'menu')))
        
        if size < 3:
            for key in ['matrix_homogen', 'iteratif_homogen', 'nonhomogen']: hasil[key].append(0)
        else:
            nilai_awal, koef = [random.uniform(500, 1000) for _ in range(3)], [0.5, 0.3, 0.2]
            n_calc = min(size, 10000)
            try:
                hasil['iteratif_homogen'].append(benchmark_simple(lambda: solve_iteratif(nilai_awal, koef, n_calc)))
                hasil['matrix_homogen'].append(benchmark_simple(lambda: solve_matrix(nilai_awal, koef, n_calc)))
                nilai_f = [random.uniform(10, 100) for _ in range(n_calc + 3)]
                hasil['nonhomogen'].append(benchmark_simple(lambda: solve(nilai_awal, koef, nilai_f, n_calc, 'iteratif')))
            except:
                for key in ['matrix_homogen', 'iteratif_homogen', 'nonhomogen']: hasil[key].append(0)
    return hasil
