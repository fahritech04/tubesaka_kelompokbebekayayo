import pandas as pd
import time

def muat_data_menu(file_excel):
    """Data menu dari Excel sheet 'porsi' """
    df = pd.read_excel(file_excel, sheet_name='porsi ', header=None)
    
    kode_menu = ['bbk', 'aym', 'th', 'tp']
    baris_menu = df[df[0].isin(kode_menu)]
    
    daftar_menu = []
    for _, baris in baris_menu.iterrows():
        nama = str(baris[1]) if pd.notna(baris[1]) else "Unknown"
        jumlah = pd.to_numeric(baris[65], errors='coerce')
        if pd.notna(jumlah):
            daftar_menu.append({'nama': nama, 'jumlah': int(jumlah)})
    
    return daftar_menu

def cari_terlaris_iteratif(menu_list):
    """Cari menu terlaris : looping biasa"""
    mulai = time.perf_counter()
    
    terlaris = menu_list[0]
    for menu in menu_list[1:]:
        if menu['jumlah'] > terlaris['jumlah']:
            terlaris = menu
    
    durasi = time.perf_counter() - mulai
    return terlaris, durasi

def cari_terlaris_rekursif(menu_list, kiri=0, kanan=None):
    """Cari menu terlaris : divide & conquer"""
    if kanan is None:
        kanan = len(menu_list) - 1
    
    # Base case: satu elemen
    if kiri == kanan:
        return menu_list[kiri]
    
    # Divide: bagi dua
    tengah = (kiri + kanan) // 2
    
    # Conquer: rekursif kiri dan kanan
    max_kiri = cari_terlaris_rekursif(menu_list, kiri, tengah)
    max_kanan = cari_terlaris_rekursif(menu_list, tengah + 1, kanan)
    
    # Combine: bandingkan
    return max_kiri if max_kiri['jumlah'] > max_kanan['jumlah'] else max_kanan

def tampilkan_hasil(judul, menu_terlaris, durasi):
    """Tampilkan hasil pencarian dengan format rapi"""
    print("=" * 50)
    print(judul)
    print("=" * 50)
    print(f"Menu Terlaris  : {menu_terlaris['nama']}")
    print(f"Total Terjual  : {menu_terlaris['jumlah']} porsi")
    print(f"Waktu Eksekusi : {durasi:.8f} detik\n")

if __name__ == "__main__":
    # Muat data dari Excel
    print("Memuat data...")
    daftar_menu = muat_data_menu('databebek2024/jan24.xlsx')
    
    if not daftar_menu:
        print("ERROR: Data menu tidak ditemukan!")
        exit(1)
    
    # Simpan ke CSV
    pd.DataFrame(daftar_menu).to_csv('menu_terlaris.csv', index=False)
    print(f"✓ Data tersimpan: menu_terlaris.csv ({len(daftar_menu)} menu)\n")
    
    # Tampilkan semua menu
    print("Data Menu:")
    for menu in daftar_menu:
        print(f"  {menu['nama']}: {menu['jumlah']} porsi")
    print()
    
    # Algoritma 1: Iteratif
    terlaris, waktu = cari_terlaris_iteratif(daftar_menu)
    tampilkan_hasil("ALGORITMA ITERATIF (Loop)", terlaris, waktu)
    
    # Algoritma 2: Rekursif
    mulai = time.perf_counter()
    terlaris = cari_terlaris_rekursif(daftar_menu)
    waktu = time.perf_counter() - mulai
    tampilkan_hasil("ALGORITMA REKURSIF (Divide & Conquer)", terlaris, waktu)