import time
import matplotlib.pyplot as plt
import numpy as np
from app_tahunan import gabung_data_bulanan, cari_menu_terlaris_iteratif, cari_menu_terlaris_rekursif

def ukur_waktu(data, fungsi):
    """Ukur waktu eksekusi dengan 500 percobaan"""
    data_besar = data * 20
    ukuran = [50, 100, 200, 300, 500, 700, 1000, len(data_besar)]
    hasil_n, hasil_waktu = [], []
    
    for n in ukuran:
        waktu = [time.perf_counter() or fungsi(data_besar[:n]) or time.perf_counter() 
                 for _ in range(500)]
        waktu = sorted([t for t in waktu if isinstance(t, (int, float))])
        buang = len(waktu) // 10
        rata = sum(waktu[buang:-buang]) / len(waktu[buang:-buang]) * 1000
        hasil_n.append(n)
        hasil_waktu.append(rata)
    
    return hasil_n, hasil_waktu

def buat_grafik(n, waktu_iter, waktu_rek):
    """Tampilkan 3 grafik sekaligus"""
    # Grafik 1: Iteratif
    plt.figure(1, figsize=(10, 6))
    plt.plot(n, waktu_iter, 's-', color='#3498db', linewidth=2.5, markersize=10, label='Iteratif')
    koef = np.polyfit(n, waktu_iter, 1)
    plt.plot(n, np.poly1d(koef)(n), '--', color='#3498db', alpha=0.6, linewidth=2, label='O(n)')
    plt.xlabel('Ukuran Input (n)', fontsize=13, fontweight='bold')
    plt.ylabel('Waktu Eksekusi (ms)', fontsize=13, fontweight='bold')
    plt.title('Running Time Iteratif', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    # Grafik 2: Rekursif
    plt.figure(2, figsize=(10, 6))
    plt.plot(n, waktu_rek, 'o-', color='#e74c3c', linewidth=2.5, markersize=10, label='Rekursif')
    koef = np.polyfit(n, waktu_rek, 1)
    plt.plot(n, np.poly1d(koef)(n), '--', color='#e74c3c', alpha=0.6, linewidth=2, label='O(n)')
    plt.xlabel('Ukuran Input (n)', fontsize=13, fontweight='bold')
    plt.ylabel('Waktu Eksekusi (ms)', fontsize=13, fontweight='bold')
    plt.title('Running Time Rekursif', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    # Grafik 3: Perbandingan
    plt.figure(3, figsize=(12, 7))
    plt.plot(n, waktu_iter, 's-', color='#3498db', linewidth=2.5, markersize=10, label='Iteratif')
    plt.plot(n, waktu_rek, 'o-', color='#e74c3c', linewidth=2.5, markersize=10, label='Rekursif')
    plt.fill_between(n, waktu_iter, waktu_rek, alpha=0.2, color='gray', label='Selisih')
    plt.xlabel('Ukuran Input (n)', fontsize=13, fontweight='bold')
    plt.ylabel('Waktu Eksekusi (ms)', fontsize=13, fontweight='bold')
    plt.title('Perbandingan: Iteratif vs Rekursif', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    # Tampilkan semua
    plt.show()

if __name__ == "__main__":
    print("=" * 60)
    print("ANALISIS KOMPLEKSITAS - Hasil dari app_tahunan.py")
    print("=" * 60)
    
    # Load data tahunan (sama seperti app_tahunan.py)
    files = [f'databebek2024/{b}24.xlsx' for b in ['jan','feb','mar','apr','mei','jun','jul','aug','sep','okt','nov','des']]
    print("\nMemuat data 12 bulan...")
    data = gabung_data_bulanan(files)
    print(f"✓ {len(data)} menu dimuat\n")
    
    # Ukur performa
    print("Mengukur performa algoritma...")
    n, waktu_iter = ukur_waktu(data, lambda d: cari_menu_terlaris_iteratif(d)[0])
    _, waktu_rek = ukur_waktu(data, cari_menu_terlaris_rekursif)
    
    # Tabel hasil
    print("\n" + "=" * 60)
    print(f"{'n':<8} {'Iteratif (ms)':<18} {'Rekursif (ms)':<18} {'Selisih'}")
    print("-" * 60)
    for i in range(len(n)):
        selisih = ((waktu_rek[i] - waktu_iter[i]) / waktu_iter[i] * 100)
        print(f"{n[i]:<8} {waktu_iter[i]:<18.6f} {waktu_rek[i]:<18.6f} {selisih:>+6.1f}%")
    print("=" * 60)
    
    # Tampilkan grafik
    print("\nMenampilkan 3 grafik sekaligus...")
    buat_grafik(n, waktu_iter, waktu_rek)
    
    # Kesimpulan
    overhead = ((waktu_rek[-1] - waktu_iter[-1]) / waktu_iter[-1] * 100)
    print(f"\nKESIMPULAN:")
    print(f"Iteratif : {waktu_iter[-1]:.6f} ms (O(n) waktu, O(1) ruang)")
    print(f"Rekursif : {waktu_rek[-1]:.6f} ms (O(n) waktu, O(log n) ruang)")
    print(f"Overhead : +{overhead:.1f}%")
    print("=" * 60)
