import pandas as pd
from config import SHEET_PORSI, COL_KODE, COL_NAMA, COL_JUMLAH, KODE_PRODUK, hitung_waktu_algoritma

def baca_menu_dari_excel(nama_file):
    df = pd.read_excel(nama_file, sheet_name=SHEET_PORSI, header=None)
    hasil = []
    for _, baris in df[df[COL_KODE].isin(KODE_PRODUK)].iterrows():
        jumlah = pd.to_numeric(baris[COL_JUMLAH], errors='coerce')
        if pd.notna(jumlah):
            hasil.append({'nama': str(baris[COL_NAMA]), 'jumlah': int(jumlah)})
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
    # Cari menu terlaris dengan algoritma iteratif - O(n)
    terlaris = daftar_menu[0]
    for menu in daftar_menu[1:]:
        if menu['jumlah'] > terlaris['jumlah']:
            terlaris = menu
    return terlaris

def cari_menu_terlaris_rekursif(daftar_menu, kiri=0, kanan=None):
    # Cari menu terlaris dengan divide & conquer - O(n) waktu, O(log n) ruang
    if kanan is None: kanan = len(daftar_menu) - 1
    if kiri == kanan: return daftar_menu[kiri]
    
    tengah = (kiri + kanan) // 2
    terlaris_kiri = cari_menu_terlaris_rekursif(daftar_menu, kiri, tengah)
    terlaris_kanan = cari_menu_terlaris_rekursif(daftar_menu, tengah + 1, kanan)
    return terlaris_kiri if terlaris_kiri['jumlah'] > terlaris_kanan['jumlah'] else terlaris_kanan

def cetak_hasil(judul, menu_terlaris, waktu):
    print(f"{'='*50}\n{judul}\n{'='*50}")
    print(f"Menu Terlaris: {menu_terlaris['nama']}")
    print(f"Total Terjual: {menu_terlaris['jumlah']:,} porsi")
    print(f"Waktu        : {waktu:.8f} detik\n")
