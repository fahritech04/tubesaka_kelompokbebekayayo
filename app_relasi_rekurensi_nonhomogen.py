import pandas as pd, time, numpy as np

BULAN = ['jan','feb','mar','apr','mei','jun','jul','aug','sep','okt','nov','des']
FILES = [f'databebek2024/{b}24.xlsx' for b in BULAN]
PRODUK = ['bebek bakar 1 ekor','bebek bakar 1/2 ekor','ayam bakar 1 ekor','ayam bakar 1/2 ekor']

def baca_data():
    data = {p: [] for p in PRODUK}
    for f in FILES:
        try:
            df = pd.read_excel(f, sheet_name='porsi ', header=None)
            for p in PRODUK:
                total = sum(pd.to_numeric(row[65], errors='coerce') for _, row in df[df[1]==p].iterrows() if pd.notna(row[65]))
                data[p].append(int(total))
        except: 
            for p in PRODUK: data[p].append(0)
    return data

def pred_hom(koef, T, i):
    return sum(koef[j]*T[i-j-1] for j in range(len(koef)))

def get_f_val(f_src, i):
    if f_src is None: return 0.0
    try: return float(f_src[i])
    except: return float(f_src[-1] if f_src else 0.0)

def solve(v, koef, f_src, n, method='iteratif'):
    k = len(koef)
    if n < k: return float(v[n])
    
    if method == 'iteratif':
        T = [float(x) for x in v]
        for i in range(k, n+1):
            T.append(pred_hom(koef, T, i) + get_f_val(f_src, i))
        return T[n]
    
    elif method == 'matrix':
        c = None
        if f_src and not callable(f_src):
            try: c = float(f_src[0]) if len(set(f_src))==1 else None
            except: c = None
        if c is None: return solve(v, koef, f_src, n, 'iteratif')
        
        def mm(A, B): 
            return [[sum(A[i][m]*B[m][j] for m in range(len(A))) for j in range(len(A))] for i in range(len(A))]
        
        def mp(M, e):
            res = [[1 if i==j else 0 for j in range(len(M))] for i in range(len(M))]
            b = [r[:] for r in M]
            while e: 
                if e&1: res = mm(res, b)
                b = mm(b, b)
                e >>= 1
            return res
        
        sz = k + 1
        C = [[0.]*sz for _ in range(sz)]
        for j in range(k): C[0][j] = koef[j]
        C[0][-1] = c
        for i in range(1, k): C[i][i-1] = 1.0
        C[-1][-1] = 1.0
        M = mp(C, n-k+1)
        return sum(M[0][j]*[v[k-1-j] for j in range(k)]+[1.0] for j in range(sz))
    
    else:  # closed-form
        try:
            poly = [1] + [-c for c in koef[::-1]]
            akar = np.roots(poly)
            M = np.array([[akar[i]**j for i in range(k)] for j in range(k)], dtype=complex)
            c = np.linalg.solve(M, np.array(v[:k], dtype=complex))
            return float(np.real(sum(c[i]*akar[i]**n for i in range(k))))
        except: return solve(v, koef, f_src, n, 'iteratif')

def hitung_koef_nonhom(data):
    if len(data) < 4: return [0.5, 0.3, 0.2], [0]*len(data)
    try:
        window = min(8, len(data))
        A = np.array([[data[n-1], data[n-2], data[n-3]] for n in range(3, window)])
        b = np.array(data[3:window])
        koef = list(np.linalg.lstsq(A, b, rcond=None)[0])
        f_n = [0.0 if i < 3 else float(data[i] - pred_hom(koef, data, i)) for i in range(len(data))]
        return koef, f_n
    except: return [0.5, 0.3, 0.2], [0]*len(data)

if __name__ == "__main__":
    print("="*80)
    print("Analisis - Relasi Rekurensi Linier Non-Homogen")
    print("="*80)
    
    data = baca_data()
    if all(sum(data[p])==0 for p in PRODUK):
        for i, p in enumerate(PRODUK): 
            data[p] = [500+j*(50+i*20) for j in range(12)]
    
    totals = {p: sum(data[p]) for p in PRODUK}
    gt = sum(totals.values())
    
    print(f"\n{'='*80}\n{'Produk':<30}{'Total':<12}{'Rata/Bln':<12}{'%':<8}\n{'-'*80}")
    for p in sorted(PRODUK, key=lambda x: totals[x], reverse=True):
        pct = (totals[p]/gt*100 if gt else 0)
        print(f"{p:<30}{totals[p]:<11.0f}{totals[p]/12:<11.1f}{pct:<7.1f}%")
    print(f"{'-'*80}\nTOTAL {gt:<20.0f}{gt/12:<11.1f}100.0%\n")
    
    print(f"{'='*80}\nAnalisis Per Produk: T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3) + f(n)\n{'='*80}")
    
    for p in PRODUK:
        d = data[p]
        if sum(d)==0 or len(d)<4: continue
        
        k, f_n = hitung_koef_nonhom(d)
        v = [float(x) for x in d[:3]]
        
        print(f"\n{'-'*80}\nProduk: {p}")
        print(f"Formula homogen: T(n) = {k[0]:.4f}·T(n-1) + {k[1]:.4f}·T(n-2) + {k[2]:.4f}·T(n-3)")
        print(f"f(n): {[f'{x:.0f}' for x in f_n[3:]]}")
        print(f"Sum Koef={sum(k):.4f} | Initial: {[int(x) for x in v]}")
        
        print(f"\n  {'Method':<10} T(6)      T(9)      T(12)")
        for method in ["iteratif", "matrix", "closed"]:
            res_str = f"  {method.capitalize():<10}"
            for n in [6, 9, 12]:
                try: res_str += f" {solve(v, k, f_n, n, method):8.0f}"
                except: res_str += f" {'ERR':>8}"
            print(res_str)
        
        print(f"\n  {'Bln':<4} {'Aktual':<10} {'Hom':<10} {'f(n)':<8} {'Pred':<10} {'Error%':<8}")
        print(f"  {'-'*68}")
        err_sum = 0
        for i in range(3, len(d)):
            hom_part = pred_hom(k, d, i)
            pred = solve(v, k, f_n, i, "iteratif")
            e = abs(pred-d[i])/d[i]*100 if d[i] else 0
            err_sum += e
            print(f"  B{i+1:<3} {d[i]:<9.0f} {hom_part:<9.0f} {f_n[i]:<7.0f} {pred:<9.0f} {e:<7.1f}%")
        print(f"\n  Rata-rata Error: {err_sum/max(1,len(d)-3):.2f}%")
        print(f"  Status: {'VALID NON-HOMOGEN' if abs(sum(f_n[3:]))/(sum(d[3:])+0.1)*100 > 5 else 'Dominan HOMOGEN'}")
