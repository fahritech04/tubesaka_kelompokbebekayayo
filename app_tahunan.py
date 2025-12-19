import pandas as pd
import time

def baca_menu_dari_excel(nama_file):
    """Baca data menu dari satu file Excel"""
    df = pd.read_excel(nama_file, sheet_name='porsi ', header=None)
    
    kode_menu = ['bbk', 'aym', 'th', 'tp']
    baris_menu = df[df[0].isin(kode_menu)]
    
    hasil = []
    for _, baris in baris_menu.iterrows():
        nama = str(baris[1]) if pd.notna(baris[1]) else "Unknown"
        jumlah = pd.to_numeric(baris[65], errors='coerce')
        if pd.notna(jumlah):
            hasil.append({'nama': nama, 'jumlah': int(jumlah)})
    
    return hasil

def gabung_data_bulanan(daftar_file):
    """Gabung penjualan menu dari 12 file bulanan"""
    total_per_menu = {}
    
    for file in daftar_file:
        try:
            print(f"  Membaca {file}...")
            menu_bulan_ini = baca_menu_dari_excel(file)
            
            for menu in menu_bulan_ini:
                nama = menu['nama']
                if nama in total_per_menu:
                    total_per_menu[nama] += menu['jumlah']
                else:
                    total_per_menu[nama] = menu['jumlah']
        except Exception as e:
            print(f"  ⚠ Error: {e}")
    
    return [{'nama': nama, 'jumlah': jumlah} for nama, jumlah in total_per_menu.items()]

def cari_menu_terlaris_iteratif(daftar_menu):
    """Cari menu terlaris pakai loop biasa"""
    mulai = time.perf_counter()
    
    terlaris = daftar_menu[0]
    for menu in daftar_menu[1:]:
        if menu['jumlah'] > terlaris['jumlah']:
            terlaris = menu
    
    waktu = time.perf_counter() - mulai
    return terlaris, waktu

def cari_menu_terlaris_rekursif(daftar_menu, kiri=0, kanan=None):
    """Cari menu terlaris pakai divide & conquer"""
    if kanan is None:
        kanan = len(daftar_menu) - 1
    
    if kiri == kanan:
        return daftar_menu[kiri]
    
    tengah = (kiri + kanan) // 2
    terlaris_kiri = cari_menu_terlaris_rekursif(daftar_menu, kiri, tengah)
    terlaris_kanan = cari_menu_terlaris_rekursif(daftar_menu, tengah + 1, kanan)
    
    return terlaris_kiri if terlaris_kiri['jumlah'] > terlaris_kanan['jumlah'] else terlaris_kanan

def hitung_waktu_algoritma(fungsi_cari, daftar_menu):
    """Hitung waktu eksekusi algoritma pencarian"""
    mulai = time.perf_counter()
    hasil = fungsi_cari(daftar_menu)
    waktu = time.perf_counter() - mulai
    return hasil, waktu

def cetak_hasil(judul, menu_terlaris, waktu):
    """Tampilkan hasil pencarian"""
    print("=" * 50)
    print(judul)
    print("=" * 50)
    print(f"Menu Terlaris  : {menu_terlaris['nama']}")
    print(f"Total Terjual  : {menu_terlaris['jumlah']:,} porsi")
    print(f"Waktu Eksekusi : {waktu:.8f} detik\n")

if __name__ == "__main__":
    # File Excel untuk 12 bulan
    file_excel = [
        'databebek2024/jan24.xlsx', 'databebek2024/feb24.xlsx', 'databebek2024/mar24.xlsx',
        'databebek2024/apr24.xlsx', 'databebek2024/mei24.xlsx', 'databebek2024/jun24.xlsx',
        'databebek2024/jul24.xlsx', 'databebek2024/aug24.xlsx', 'databebek2024/sep24.xlsx',
        'databebek2024/okt24.xlsx', 'databebek2024/nov24.xlsx', 'databebek2024/des24.xlsx'
    ]
    
    # Gabungkan data dari 12 bulan
    print("Memuat data tahun 2024...")
    semua_menu = gabung_data_bulanan(file_excel)
    
    if not semua_menu:
        print("ERROR: Data tidak ditemukan!")
        exit(1)
    
    # Urutkan dari terbesar
    semua_menu = sorted(semua_menu, key=lambda x: x['jumlah'], reverse=True)
    
    # Simpan hasil
    pd.DataFrame(semua_menu).to_csv('menu_terlaris_tahunan.csv', index=False)
    print(f"✓ Tersimpan: menu_terlaris_tahunan.csv ({len(semua_menu)} menu)\n")
    
    # Tampilkan top 10
    print("=" * 50)
    print("TOP 10 MENU TERLARIS TAHUN 2024")
    print("=" * 50)
    for i, menu in enumerate(semua_menu[:10], 1):
        print(f"{i:2d}. {menu['nama']:<35} : {menu['jumlah']:>6,} porsi")
    print()
    
    # Bandingkan 2 algoritma
    terlaris, waktu = cari_menu_terlaris_iteratif(semua_menu)
    cetak_hasil("ALGORITMA ITERATIF (Loop)", terlaris, waktu)
    
    terlaris, waktu = hitung_waktu_algoritma(cari_menu_terlaris_rekursif, semua_menu)
    cetak_hasil("ALGORITMA REKURSIF (Divide & Conquer)", terlaris, waktu)
