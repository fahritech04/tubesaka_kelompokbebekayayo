import pandas as pd, numpy as np
from config import BULAN, FILES, PRODUK, SHEET_PORSI, COL_NAMA, COL_JUMLAH, baca_data_produk, timed, kali_matrix, pangkat_matrix

def baca_data_excel():
    return baca_data_produk(FILES, PRODUK)

@timed
def solve_iteratif(nilai_awal, koef, n):
    # Relasi rekurensi iteratif - O(n) waktu, O(n) ruang
    T = nilai_awal.copy()
    for i in range(len(koef), n + 1):
        T.append(sum(koef[j] * T[i - j - 1] for j in range(len(koef))))
    return T[n]

@timed
def solve_matrix(nilai_awal, koef, n):
    # Eksponen matriks - O(k³ log n) waktu, optimal untuk n besar
    jumlah_koef = len(koef)
    if n < jumlah_koef: return nilai_awal[n]
    
    C = [[koef[j] if i == 0 else (1 if i-1 == j else 0) for j in range(jumlah_koef)] for i in range(jumlah_koef)]
    M = pangkat_matrix(C, n - jumlah_koef + 1)
    return sum(M[0][j] * nilai_awal[jumlah_koef - 1 - j] for j in range(jumlah_koef))

@timed
def solve_closed_form(nilai_awal, koef, n):
    # Bentuk tertutup dengan nilai eigen - O(k³) inisialisasi, O(1) evaluasi per kueri
    jumlah_koef = len(koef)
    if n < jumlah_koef: return float(nilai_awal[n])
    try:
        # Characteristic polynomial: x^k - c1*x^(k-1) - c2*x^(k-2) - ... - ck = 0
        # Koef dalam urutan: [1, -c1, -c2, -c3] untuk numpy.roots
        poly = [1] + [-c for c in koef]
        akar = np.roots(poly)  # Nilai eigen (eigenvalues)
        
        # Vandermonde matrix untuk menyelesaikan konstanta
        # M[i][j] = λⱼⁱ (row i untuk n=i, column j untuk eigenvalue j)
        M = np.array([[akar[j]**i for j in range(jumlah_koef)] for i in range(jumlah_koef)], dtype=complex)
        konstanta = np.linalg.solve(M, np.array(nilai_awal[:jumlah_koef], dtype=complex))
        
        # Evaluasi: O(1)! Hanya perlu hitung akar^n
        return np.real(sum(konstanta[i] * akar[i]**n for i in range(jumlah_koef)))
    except: return float(nilai_awal[0])

def hitung_koefisien(data):
    if len(data) < 4: return [0.5, 0.3, 0.2]
    try:
        A = np.array([[data[n-1], data[n-2], data[n-3]] for n in range(3, len(data))])
        koef, _, _, _ = np.linalg.lstsq(A, np.array(data[3:]), rcond=None)
        return list(koef)
    except: return [0.5, 0.3, 0.2]

def tampilkan_ringkasan(data):
    total_per_produk = {produk: sum(data[produk]) for produk in PRODUK}
    grand_total = sum(total_per_produk.values())
    
    print(f"\n{'='*80}\nRingkasan Penjualan\n{'='*80}\n")
    print(f"{'Produk':<30}{'Total':<12}{'Rata/Bln':<12}{'%':<8}")
    print("-" * 80)
    
    for produk in sorted(PRODUK, key=lambda x: total_per_produk[x], reverse=True):
        total = total_per_produk[produk]
        persentase = (total / grand_total * 100 if grand_total else 0)
        print(f"{produk:<30}{total:<11.0f}{total/12:<11.1f}{persentase:<7.1f}%")
    
    print("-" * 80)
    print(f"{'TOTAL':<30}{grand_total:<11.0f}{grand_total/12:<11.1f}{'100.0':<7}%\n")
    return total_per_produk
