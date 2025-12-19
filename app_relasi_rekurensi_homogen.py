import pandas as pd, time, numpy as np

BULAN = ['jan','feb','mar','apr','mei','jun','jul','aug','sep','okt','nov','des']
FILES = [f'databebek2024/{b}24.xlsx' for b in BULAN]
PRODUK = ['bebek bakar 1 ekor','bebek bakar 1/2 ekor','ayam bakar 1 ekor','ayam bakar 1/2 ekor']

def baca_data_excel():
    data_by_produk = {p: [] for p in PRODUK}
    for f in FILES:
        try:
            df = pd.read_excel(f, sheet_name='porsi ', header=None)
            for p in PRODUK:
                total = sum(pd.to_numeric(row[65], errors='coerce') for _, row in df[df[1]==p].iterrows() if pd.notna(row[65]))
                data_by_produk[p].append(int(total))
        except: 
            for p in PRODUK: data_by_produk[p].append(0)
    return data_by_produk

def timed(f):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        return result, time.perf_counter() - start
    return wrapper

@timed
def solve_iteratif(v, koef, n):
    T = v.copy()
    for i in range(len(koef), n + 1):
        T.append(sum(koef[j] * T[i - j - 1] for j in range(len(koef))))
    return T[n]

@timed
def solve_matrix(v, koef, n):
    k = len(koef)
    if n < k: return v[n]
    
    def matrix_mult(A, B):
        return [[sum(A[i][m] * B[m][j] for m in range(len(A))) for j in range(len(A))] for i in range(len(A))]
    
    def matrix_pow(M, exp):
        res = [[1 if i == j else 0 for j in range(len(M))] for i in range(len(M))]
        base = [row[:] for row in M]
        while exp:
            if exp & 1: res = matrix_mult(res, base)
            base = matrix_mult(base, base)
            exp >>= 1
        return res
    
    C = [[koef[j] if i == 0 else (1 if i-1 == j else 0) for j in range(k)] for i in range(k)]
    M = matrix_pow(C, n - k + 1)
    return sum(M[0][j] * v[k - 1 - j] for j in range(k))

@timed
def solve_closed_form(v, koef, n):
    k = len(koef)
    if n < k: return float(v[n])
    try:
        poly = [1] + [-c for c in koef[::-1]]
        akar = np.roots(poly)
        M = np.array([[akar[i]**j for i in range(k)] for j in range(k)], dtype=complex)
        c = np.linalg.solve(M, np.array(v[:k], dtype=complex))
        return np.real(sum(c[i] * akar[i]**n for i in range(k)))
    except: return float(v[0])

def hitung_koefisien(data):
    if len(data) < 4: return [0.5, 0.3, 0.2]
    try:
        A = np.array([[data[n-1], data[n-2], data[n-3]] for n in range(3, len(data))])
        koef, _, _, _ = np.linalg.lstsq(A, np.array(data[3:]), rcond=None)
        return list(koef)
    except: return [0.5, 0.3, 0.2]

def tampilkan_ringkasan(data):
    totals = {p: sum(data[p]) for p in PRODUK}
    gt = sum(totals.values())
    
    print(f"\n{'='*80}\nRINGKASAN PENJUALAN\n{'='*80}\n")
    print(f"{'Produk':<30}{'Total':<12}{'Rata/Bln':<12}{'%':<8}")
    print("─" * 80)
    
    for p in sorted(PRODUK, key=lambda x: totals[x], reverse=True):
        t = totals[p]
        pct = (t / gt * 100 if gt else 0)
        print(f"{p:<30}{t:<11.0f}{t/12:<11.1f}{pct:<7.1f}%")
    
    print("─" * 80)
    print(f"{'TOTAL':<30}{gt:<11.0f}{gt/12:<11.1f}{'100.0':<7}%\n")
    return totals

if __name__ == "__main__":
    print("="*80)
    print("ANALISIS KOMPLEKSITAS: RELASI REKURENSI LINIER HOMOGEN")
    print("="*80)
    
    data = baca_data_excel()
    if all(sum(data[p]) == 0 for p in PRODUK):
        for i, p in enumerate(PRODUK): 
            data[p] = [500 + j * (50 + i*20) for j in range(12)]
    
    totals = tampilkan_ringkasan(data)
    
    for p in PRODUK:
        d = data[p]
        if sum(d) == 0 or len(d) < 4: continue
        
        v = [float(x) for x in d[:3]]
        k = hitung_koefisien(d)
        
        print(f"\n{'='*80}")
        print(f"PRODUK: {p}")
        print(f"{'='*80}")
        print(f"T(n) = {k[0]:.6f}*T(n-1) + {k[1]:.6f}*T(n-2) + {k[2]:.6f}*T(n-3)")
        print(f"∑Koef = {sum(k):.6f} | Data awal: {[int(x) for x in d[:3]]}\n")
        
        algos = {"Iteratif": solve_iteratif, "Matrix": solve_matrix, "Closed": solve_closed_form}
        for algo in algos:
            print(f"  {algo:<10}:", end="")
            for n in [6, 9, 12]:
                try:
                    res, _ = algos[algo](v, k, n)
                    print(f" T({n})={res:9.0f}", end="")
                except: 
                    print(f" T({n})={'ERROR':>9}", end="")
            print()
        
        print(f"\n  {'Bln':<4}{'Aktual':<10}{'Pred':<10}{'Error%':<8}")
        err = 0
        for i in range(3, len(d)):
            pred, _ = solve_iteratif(v, k, i)
            e = abs(pred - d[i]) / d[i] * 100 if d[i] else 0
            err += e
            print(f"  B{i+1:<3}{d[i]:<9.0f}{pred:<9.0f}{e:<7.1f}%")
        
        print(f"  Rata-rata Error: {err / max(1, len(d) - 3):.2f}%")
