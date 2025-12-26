import pandas as pd, numpy as np
from config import BULAN, FILES, PRODUK, SHEET_PORSI, COL_NAMA, COL_JUMLAH, baca_data_produk, kali_matrix, pangkat_matrix

def baca_data():
    return baca_data_produk(FILES, PRODUK)

def hitung_homogen(koef, T, i):
    return sum(koef[j]*T[i-j-1] for j in range(len(koef)))

def ambil_nilai_f(nilai_f, i):
    if nilai_f is None: return 0.0
    try: return float(nilai_f[i])
    except: return float(nilai_f[-1] if nilai_f else 0.0)

def solve(nilai_awal, koef, nilai_f, n, method='iteratif'):
    jumlah_koef = len(koef)
    if n < jumlah_koef: return float(nilai_awal[n])
    
    if method == 'iteratif':
        T = [float(x) for x in nilai_awal]
        for i in range(jumlah_koef, n+1):
            T.append(hitung_homogen(koef, T, i) + ambil_nilai_f(nilai_f, i))
        return T[n]
    
    elif method == 'matrix':
        konstanta = None
        if nilai_f and not callable(nilai_f):
            try: konstanta = float(nilai_f[0]) if len(set(nilai_f))==1 else None
            except: konstanta = None
        if konstanta is None: return solve(nilai_awal, koef, nilai_f, n, 'iteratif')
        
        ukuran = jumlah_koef + 1
        C = [[0.]*ukuran for _ in range(ukuran)]
        for j in range(jumlah_koef): C[0][j] = koef[j]
        C[0][-1] = konstanta
        for i in range(1, jumlah_koef): C[i][i-1] = 1.0
        C[-1][-1] = 1.0
        M = pangkat_matrix(C, n-jumlah_koef+1)
        return sum(M[0][j]*[nilai_awal[jumlah_koef-1-j] for j in range(jumlah_koef)]+[1.0] for j in range(ukuran))
    
    else:  # closed-form
        try:
            poly = [1] + [-c for c in koef[::-1]]
            akar = np.roots(poly)
            M = np.array([[akar[i]**j for i in range(jumlah_koef)] for j in range(jumlah_koef)], dtype=complex)
            konstanta = np.linalg.solve(M, np.array(nilai_awal[:jumlah_koef], dtype=complex))
            return float(np.real(sum(konstanta[i]*akar[i]**n for i in range(jumlah_koef))))
        except: return solve(nilai_awal, koef, nilai_f, n, 'iteratif')

def hitung_koef_nonhom(data):
    if len(data) < 4: return [0.5, 0.3, 0.2], [0]*len(data)
    try:
        # Gunakan SEMUA data untuk menghitung koefisien (bukan hanya 8)
        window = len(data)
        A = np.array([[data[n-1], data[n-2], data[n-3]] for n in range(3, window)])
        b = np.array(data[3:window])
        koef = list(np.linalg.lstsq(A, b, rcond=None)[0])
        nilai_f = [0.0 if i < 3 else float(data[i] - hitung_homogen(koef, data, i)) for i in range(len(data))]
        return koef, nilai_f
    except: return [0.5, 0.3, 0.2], [0]*len(data)
