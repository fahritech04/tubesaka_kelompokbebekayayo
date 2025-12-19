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
    def w(*a, **kw):
        s = time.perf_counter()
        r = f(*a, **kw)
        return r, time.perf_counter() - s
    return w

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
    def mm(A, B):
        return [[sum(A[i][m] * B[m][j] for m in range(len(A))) for j in range(len(A))] for i in range(len(A))]
    def mp(M, exp):
        res = [[1 if i == j else 0 for j in range(len(M))] for i in range(len(M))]
        base = [row[:] for row in M]
        while exp:
            if exp & 1: res = mm(res, base)
            base = mm(base, base)
            exp >>= 1
        return res
    C = [[koef[j] if i == 0 else (1 if i-1 == j else 0) for j in range(k)] for i in range(k)]
    M = mp(C, n - k + 1)
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
    print(f"\n{'='*80}\nRINGKASAN PENJUALAN\n{'='*80}\n")
    print(f"{'Produk':<30}{'Total':<12}{'Rata/Bln':<12}{'%':<8}{'Status'}")
    print("─" * 80)
    totals = {p: sum(data[p]) for p in PRODUK}
    gt = sum(totals.values())
    for p in sorted(PRODUK, key=lambda x: totals[x], reverse=True):
        t, pct = totals[p], (totals[p] / gt * 100 if gt else 0)
        status = "★★★" if pct >= 25 else ("★★" if pct >= 15 else ("★" if pct >= 5 else "☆"))
        print(f"{p:<30}{t:<11.0f}{t/12:<11.1f}{pct:<7.1f}%{status}")
    print("─" * 80)
    print(f"{'TOTAL':<30}{gt:<11.0f}{gt/12:<11.1f}{'100.0':<7}%\n")
    return totals

def beri_rekomendasi(totals):
    print(f"{'='*80}\n⬆ REKOMENDASI PRIORITAS\n{'='*80}\n")
    sorted_sales = sorted(totals.items(), key=lambda x: x[1])
    gt = sum(totals.values())
    for i, (p, t) in enumerate(sorted_sales, 1):
        pct = (t / gt * 100) if gt else 0
        pot = ((sorted_sales[-1][1] / t) - 1) * 100 if t else 0
        aksi = "URGENT: Kembangkan promosi" if pct < 5 else ("PENTING: Tingkatkan visibility" if pct < 15 else "MONITOR: Jaga kualitas")
        print(f"{i}. {p}\n   Penjualan: {t:.0f} ({pct:.1f}%) | Gap: +{pot:.0f}% | Aksi: {aksi}\n")

if __name__ == "__main__":
    print("="*80+"\nANALISIS KOMPLEKSITAS: RELASI REKURENSI LINIER HOMOGEN\nData: 12 Bulan (2024) - Per Produk\n"+"="*80)
    print("\nMemuat data dari Excel...")
    data = baca_data_excel()
    if all(sum(data[p]) == 0 for p in PRODUK):
        print("⚠ Menggunakan dummy data...")
        for i, p in enumerate(PRODUK): data[p] = [500 + j * (50 + i*20) for j in range(12)]
    print(f"✓ Data loaded: {len(PRODUK)} produk\n")
    
    totals = tampilkan_ringkasan(data)
    beri_rekomendasi(totals)
    print(f"{'='*80}\nANALISIS KOMPLEKSITAS PER PRODUK\n{'='*80}")
    
    for p in PRODUK:
        d = data[p]
        if sum(d) == 0 or len(d) < 4: continue
        v, k = [float(x) for x in d[:3]], hitung_koefisien(d)
        print(f"\n{'='*80}\nPRODUK: {p}\n{'='*80}")
        print(f"T(n) = {k[0]:.6f}*T(n-1) + {k[1]:.6f}*T(n-2) + {k[2]:.6f}*T(n-3)")
        print(f"∑Koef = {sum(k):.6f} | Data awal: [{d[0]:.0f}, {d[1]:.0f}, {d[2]:.0f}]\n")
        
        algos = {"Iteratif": solve_iteratif, "Matrix": solve_matrix, "Closed": solve_closed_form}
        for algo in algos:
            print(f"  {algo:<10}:", end="")
            for n in [6, 9, 12]:
                try:
                    res, _ = algos[algo](v, k, n)
                    print(f" T({n})={res:9.0f}", end="")
                except: print(f" T({n})={'ERROR':>9}", end="")
            print()
        
        print(f"\n  Validasi (Bulan 4-12):\n  {'Bln':<4}{'Aktual':<10}{'Pred':<10}{'Error%':<8}")
        err = 0
        for i in range(3, len(d)):
            pred, _ = solve_iteratif(v, k, i)
            actual = d[i]
            e = abs(pred - actual) / actual * 100 if actual else 0
            err += e
            print(f"  B{i+1:<3}{actual:<9.0f}{pred:<9.0f}{e:<7.1f}%")
        print(f"  Rata-rata Error: {err / max(1, len(d) - 3):.2f}%")
