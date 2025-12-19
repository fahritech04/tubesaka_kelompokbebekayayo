import time, pandas as pd, matplotlib.pyplot as plt, numpy as np
from tubesaka_kelompokbebekayayo.app_menuporsi_tahunan import gabung_data_bulanan, cari_menu_terlaris_iteratif, cari_menu_terlaris_rekursif
from app_pendapatan import cari_pendapatan_tertinggi_iteratif, cari_pendapatan_tertinggi_rekursif
from app_relasi_rekurensi_homogen import baca_data_excel, hitung_koefisien, solve_iteratif
from app_relasi_rekurensi_nonhomogen import baca_data, hitung_koef_nonhom, solve, PRODUK

bulan = ['jan','feb','mar','apr','mei','jun','jul','aug','sep','okt','nov','des']
files = [f'databebek2024/{b}24.xlsx' for b in bulan]

def ukur_waktu(data, fungsi, percobaan=50):
    ukuran = [50, min(100, len(data)), min(200, len(data)), len(data)]
    hasil_n, hasil_waktu = [], []
    for n in ukuran:
        if n > len(data): continue
        waktu_list = [(time.perf_counter() or fungsi(data[:n]) or time.perf_counter()) for _ in range(percobaan)]
        hasil_n.append(n)
        hasil_waktu.append(np.median([t for t in waktu_list if isinstance(t, (int, float))]) * 1000)
    return hasil_n, hasil_waktu

def plot_line(ax, x, y, title, label, color, style='o-'):
    ax.plot(x, y, style, color=color, linewidth=2.5, markersize=8, label=label)
    ax.set_xlabel('Bulan' if 'Bulan' in title else 'Ukuran Input (n)', fontweight='bold')
    ax.set_ylabel('Penjualan' if 'Bulan' in title else 'Waktu (ms)', fontweight='bold')
    ax.set_title(title, fontweight='bold', fontsize=10)
    ax.grid(True, alpha=0.3)
    if label: ax.legend()

def plot_bar(ax, x, y, title, xlabel, ylabel, color='#3498db'):
    if isinstance(x[0], str):
        ax.bar(range(len(x)), y, color=color)
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x, rotation=45, ha='right', fontsize=9)
    else:
        ax.barh(x, y, color=color)
        ax.invert_yaxis()
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold')
    ax.grid(axis='x' if isinstance(x[0], str) else 'x', alpha=0.3)

print("="*70)
print("MEMBUAT GRAFIK ANALISIS DARI SEMUA FILE")
print("="*70)

# Load data
data_menu = gabung_data_bulanan(files)
data_prod_hom = baca_data_excel()
data_prod_nonhom = baca_data()
df_pendapatan = pd.read_csv('pendapatan_harian_2024.csv')

# [1] Menu Tahunan
print("\n[1/6] Grafik Menu Tahunan...")
top_menu = sorted(data_menu, key=lambda x: x['jumlah'], reverse=True)[:10]
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
names, vals = [m['nama'][:20] for m in top_menu], [m['jumlah'] for m in top_menu]
plot_bar(axes[0], names, vals, 'Top 10 Menu Terlaris (2024)', 'Jumlah Porsi', 'Menu', '#3498db')
axes[1].pie(vals, labels=names, autopct='%1.1f%%', startangle=90)
axes[1].set_title('Proporsi Top 10 Menu', fontweight='bold')
plt.tight_layout()
plt.savefig('grafik_menu_tahunan.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ grafik_menu_tahunan.png")

# [2] Pendapatan
print("[2/6] Grafik Pendapatan...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
# Top 10
plot_bar(axes[0, 0], df_pendapatan.head(10)['tanggal'].tolist(), 
         df_pendapatan.head(10)['pendapatan'].tolist(), 'Top 10 Pendapatan Harian', 
         'Tanggal', 'Pendapatan (Rp)', '#e74c3c')
# Histogram
axes[0, 1].hist(df_pendapatan['pendapatan'], bins=30, color='#2ecc71', edgecolor='black', alpha=0.7)
axes[0, 1].set_xlabel('Pendapatan (Rp)', fontweight='bold')
axes[0, 1].set_ylabel('Frekuensi', fontweight='bold')
axes[0, 1].set_title('Distribusi Pendapatan Harian', fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3)
# Box plot
axes[1, 0].boxplot(df_pendapatan['pendapatan'], vert=True)
axes[1, 0].set_ylabel('Pendapatan (Rp)', fontweight='bold')
axes[1, 0].set_title('Box Plot Pendapatan', fontweight='bold')
axes[1, 0].grid(axis='y', alpha=0.3)
# Statistik
axes[1, 1].axis('off')
stats = f"Total Hari: {len(df_pendapatan)}\nTotal: Rp {df_pendapatan['pendapatan'].sum():,.0f}\nRata-rata: Rp {df_pendapatan['pendapatan'].mean():,.0f}\nMedian: Rp {df_pendapatan['pendapatan'].median():,.0f}\nMaksimal: Rp {df_pendapatan['pendapatan'].max():,.0f}\nMinimal: Rp {df_pendapatan['pendapatan'].min():,.0f}"
axes[1, 1].text(0.1, 0.5, stats, fontsize=11, family='monospace', verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.savefig('grafik_pendapatan.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ grafik_pendapatan.png")

# [3] Kompleksitas
print("[3/6] Grafik Kompleksitas Algoritma...")
n, waktu_iter = ukur_waktu(data_menu, cari_menu_terlaris_iteratif)
_, waktu_rek = ukur_waktu(data_menu, cari_menu_terlaris_rekursif)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
plot_line(axes[0], n, waktu_iter, 'Algoritma Iteratif: O(n)', 'Iteratif', '#3498db', 's-')
plot_line(axes[1], n, waktu_rek, 'Algoritma Rekursif: O(n)', 'Rekursif', '#e74c3c', 'o-')
axes[2].plot(n, waktu_iter, 's-', color='#3498db', linewidth=2.5, markersize=8, label='Iteratif')
axes[2].plot(n, waktu_rek, 'o-', color='#e74c3c', linewidth=2.5, markersize=8, label='Rekursif')
axes[2].fill_between(n, waktu_iter, waktu_rek, alpha=0.2, color='gray')
axes[2].set_xlabel('Ukuran Input (n)', fontweight='bold')
axes[2].set_ylabel('Waktu (ms)', fontweight='bold')
axes[2].set_title('Perbandingan: Iteratif vs Rekursif', fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('grafik_kompleksitas.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ grafik_kompleksitas.png")

# [4] Relasi Homogen
print("[4/6] Grafik Relasi Rekurensi Homogen...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for idx, produk in enumerate(PRODUK):
    d = data_prod_hom[produk]
    if sum(d) == 0: continue
    k, v = hitung_koefisien(d), [float(x) for x in d[:3]]
    pred = [d[i] if i < 3 else solve_iteratif(v, k, i)[0] for i in range(len(d))]
    plot_line(axes.flatten()[idx], list(range(1, len(d)+1)), d, produk[:25], 'Aktual', '#3498db', 'o-')
    axes.flatten()[idx].plot(range(1, len(d)+1), pred, 's--', color='gray', linewidth=2, markersize=6, label='Prediksi', alpha=0.7)
    axes.flatten()[idx].set_xticks(range(1, len(d)+1))
    axes.flatten()[idx].legend()
plt.tight_layout()
plt.savefig('grafik_relasi_homogen.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ grafik_relasi_homogen.png")

# [5] Relasi Non-Homogen
print("[5/6] Grafik Relasi Rekurensi Non-Homogen...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for idx, produk in enumerate(PRODUK):
    d = data_prod_nonhom[produk]
    if sum(d) == 0: continue
    k, f_n, v = hitung_koef_nonhom(d)[0], hitung_koef_nonhom(d)[1], [float(x) for x in d[:3]]
    pred = [solve(v, k, f_n, i, 'iteratif') for i in range(len(d))]
    plot_line(axes.flatten()[idx], list(range(1, len(d)+1)), d, produk[:25], 'Aktual', '#2ecc71', 'o-')
    axes.flatten()[idx].plot(range(1, len(d)+1), pred, 's--', color='gray', linewidth=2, markersize=6, label='Prediksi', alpha=0.7)
    axes.flatten()[idx].set_xticks(range(1, len(d)+1))
    axes.flatten()[idx].legend()
plt.tight_layout()
plt.savefig('grafik_relasi_nonhomogen.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ grafik_relasi_nonhomogen.png")

# [6] Ringkasan
print("[6/6] Grafik Ringkasan...")
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Top 5 Menu
top_5 = sorted(data_menu, key=lambda x: x['jumlah'], reverse=True)[:5]
ax1 = fig.add_subplot(gs[0, 0])
ax1.bar(range(len(top_5)), [m['jumlah'] for m in top_5], color='#3498db')
ax1.set_xticks(range(len(top_5)))
ax1.set_xticklabels([m['nama'][:12] for m in top_5], rotation=45, ha='right', fontsize=9)
ax1.set_ylabel('Porsi', fontweight='bold')
ax1.set_title('Top 5 Menu Terlaris', fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Statistik Pendapatan
ax2 = fig.add_subplot(gs[0, 1])
stats = [df_pendapatan['pendapatan'].mean(), df_pendapatan['pendapatan'].median(), 
         df_pendapatan['pendapatan'].max(), df_pendapatan['pendapatan'].min()]
ax2.bar(['Rata-rata', 'Median', 'Maksimal', 'Minimal'], stats, color=['#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'])
ax2.set_ylabel('Pendapatan (Rp)', fontweight='bold')
ax2.set_title('Statistik Pendapatan', fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Kompleksitas
ax3 = fig.add_subplot(gs[1, :])
ax3.plot(n, waktu_iter, 's-', label='Iteratif O(n)', linewidth=2.5, markersize=8, color='#3498db')
ax3.plot(n, waktu_rek, 'o-', label='Rekursif O(n)', linewidth=2.5, markersize=8, color='#e74c3c')
ax3.set_xlabel('Ukuran Input (n)', fontweight='bold')
ax3.set_ylabel('Waktu (ms)', fontweight='bold')
ax3.set_title('Perbandingan Kompleksitas Algoritma', fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Relasi Homogen
produk_utama = 'bebek bakar 1 ekor'
ax4 = fig.add_subplot(gs[2, 0])
d_hom = data_prod_hom[produk_utama]
k_hom = hitung_koefisien(d_hom)
v_hom = [float(x) for x in d_hom[:3]]
pred_hom = [d_hom[i] if i < 3 else solve_iteratif(v_hom, k_hom, i)[0] for i in range(len(d_hom))]
ax4.plot(range(1, len(d_hom)+1), d_hom, 'o-', label='Aktual', linewidth=2, markersize=7, color='#3498db')
ax4.plot(range(1, len(d_hom)+1), pred_hom, 's--', label='Prediksi', linewidth=2, markersize=5, color='#e74c3c', alpha=0.7)
ax4.set_xlabel('Bulan', fontweight='bold')
ax4.set_ylabel('Penjualan', fontweight='bold')
ax4.set_title('Relasi Rekurensi Homogen', fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)

# Relasi Non-Homogen
ax5 = fig.add_subplot(gs[2, 1])
d_nonhom = data_prod_nonhom[produk_utama]
k_nonhom, f_n_nonhom = hitung_koef_nonhom(d_nonhom)
v_nonhom = [float(x) for x in d_nonhom[:3]]
pred_nonhom = [solve(v_nonhom, k_nonhom, f_n_nonhom, i, 'iteratif') for i in range(len(d_nonhom))]
ax5.plot(range(1, len(d_nonhom)+1), d_nonhom, 'o-', label='Aktual', linewidth=2, markersize=7, color='#2ecc71')
ax5.plot(range(1, len(d_nonhom)+1), pred_nonhom, 's--', label='Prediksi', linewidth=2, markersize=5, color='#e74c3c', alpha=0.7)
ax5.set_xlabel('Bulan', fontweight='bold')
ax5.set_ylabel('Penjualan', fontweight='bold')
ax5.set_title('Relasi Rekurensi Non-Homogen', fontweight='bold')
ax5.legend()
ax5.grid(True, alpha=0.3)

plt.savefig('grafik_ringkasan.png', dpi=100, bbox_inches='tight')
plt.close()
print("✓ grafik_ringkasan.png")

print("\n" + "="*70)
print("✓ SEMUA GRAFIK BERHASIL DIBUAT!")
print("="*70)
print("\nGrafik yang tersimpan:")
print("  1. grafik_menu_tahunan.png      - Top 10 menu + proporsi")
print("  2. grafik_pendapatan.png        - Statistik & distribusi pendapatan")
print("  3. grafik_kompleksitas.png      - Perbandingan algoritma")
print("  4. grafik_relasi_homogen.png    - Prediksi relasi homogen")
print("  5. grafik_relasi_nonhomogen.png - Prediksi relasi non-homogen")
print("  6. grafik_ringkasan.png         - Ringkasan 6 grafik")
print("="*70)
