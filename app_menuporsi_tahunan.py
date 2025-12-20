import pandas as pd
import time

def baca_menu_dari_excel(nama_file):
    df = pd.read_excel(nama_file, sheet_name='porsi ', header=None)
    hasil = []
    for _, baris in df[df[0].isin(['bbk', 'aym', 'th', 'tp'])].iterrows():
        jumlah = pd.to_numeric(baris[65], errors='coerce')
        if pd.notna(jumlah):
            hasil.append({'nama': str(baris[1]), 'jumlah': int(jumlah)})
    return hasil

def gabung_data_bulanan(daftar_file):
    total_per_menu = {}
    for file in daftar_file:
        try:
            for menu in baca_menu_dari_excel(file):
                total_per_menu[menu['nama']] = total_per_menu.get(menu['nama'], 0) + menu['jumlah']
        except: pass
    return [{'nama': k, 'jumlah': v} for k, v in total_per_menu.items()]

def cari_menu_terlaris_iteratif(daftar_menu):
    terlaris = daftar_menu[0]
    for menu in daftar_menu[1:]:
        if menu['jumlah'] > terlaris['jumlah']:
            terlaris = menu
    return terlaris

def cari_menu_terlaris_rekursif(daftar_menu, kiri=0, kanan=None):
    if kanan is None: kanan = len(daftar_menu) - 1
    if kiri == kanan: return daftar_menu[kiri]
    
    tengah = (kiri + kanan) // 2
    terlaris_kiri = cari_menu_terlaris_rekursif(daftar_menu, kiri, tengah)
    terlaris_kanan = cari_menu_terlaris_rekursif(daftar_menu, tengah + 1, kanan)
    return terlaris_kiri if terlaris_kiri['jumlah'] > terlaris_kanan['jumlah'] else terlaris_kanan

def hitung_waktu_algoritma(fungsi_cari, daftar_menu):
    mulai = time.perf_counter()
    hasil = fungsi_cari(daftar_menu)
    waktu = time.perf_counter() - mulai
    return hasil, waktu

def cetak_hasil(judul, menu_terlaris, waktu):
    print(f"{'='*50}\n{judul}\n{'='*50}")
    print(f"Menu Terlaris: {menu_terlaris['nama']}")
    print(f"Total Terjual: {menu_terlaris['jumlah']:,} porsi")
    print(f"Waktu        : {waktu:.8f} detik\n")

if __name__ == "__main__":
    bulan = ['jan','feb','mar','apr','mei','jun','jul','aug','sep','okt','nov','des']
    file_excel = [f'databebek2024/{b}24.xlsx' for b in bulan]
    
    semua_menu = gabung_data_bulanan(file_excel)
    if not semua_menu:
        print("ERROR: Data tidak ditemukan!")
        exit(1)
    
    semua_menu = sorted(semua_menu, key=lambda x: x['jumlah'], reverse=True)
    pd.DataFrame(semua_menu).to_csv('menu_terlaris_tahunan.csv', index=False)
    
    print("="*50)
    print("Top 10 Menu Terlaris Tahun 2024")
    print("="*50)
    for i, menu in enumerate(semua_menu[:10], 1):
        print(f"{i:2d}. {menu['nama']:<35} : {menu['jumlah']:>6,} porsi")
    print()
    
    terlaris, waktu = hitung_waktu_algoritma(cari_menu_terlaris_iteratif, semua_menu)
    cetak_hasil("Algoritma Iteratif", terlaris, waktu)
    
    terlaris, waktu = hitung_waktu_algoritma(cari_menu_terlaris_rekursif, semua_menu)
    cetak_hasil("Algoritma Rekursif (Divide & Conquer)", terlaris, waktu)
