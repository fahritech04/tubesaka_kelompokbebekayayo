import pandas as pd
from config import SHEET_SALES, COL_NAMA, COL_KODE, COL_PENDAPATAN, hitung_waktu_algoritma

def baca_pendapatan_harian(file_excel):
    df = pd.read_excel(file_excel, sheet_name=SHEET_SALES, header=None)
    baris_kas = df[df[COL_NAMA].astype(str).str.lower() == 'kas']
    hasil = []
    for _, baris in baris_kas.iterrows():
        tanggal = baris[COL_KODE]
        pendapatan = pd.to_numeric(baris[COL_PENDAPATAN], errors='coerce')
        if pd.notna(tanggal) and pd.notna(pendapatan) and pendapatan > 0:
            hasil.append({
                'tanggal': tanggal.strftime('%Y-%m-%d') if hasattr(tanggal, 'strftime') else str(tanggal),
                'pendapatan': int(pendapatan)
            })
    return hasil

def gabung_data_bulanan(daftar_file):
    semua_data = []
    for file in daftar_file:
        try:
            semua_data.extend(baca_pendapatan_harian(file))
        except: pass
    return semua_data

def cari_pendapatan_tertinggi_iteratif(data):
    # Cari pendapatan tertinggi dengan algoritma iteratif - O(n)
    tertinggi = data[0]
    for hari in data[1:]:
        if hari['pendapatan'] > tertinggi['pendapatan']:
            tertinggi = hari
    return tertinggi

def cari_pendapatan_tertinggi_rekursif(data, kiri=0, kanan=None):
    # Cari pendapatan tertinggi dengan divide & conquer - O(n) waktu, O(log n) ruang
    if kanan is None: kanan = len(data) - 1
    if kiri == kanan: return data[kiri]
    
    tengah = (kiri + kanan) // 2
    tertinggi_kiri = cari_pendapatan_tertinggi_rekursif(data, kiri, tengah)
    tertinggi_kanan = cari_pendapatan_tertinggi_rekursif(data, tengah + 1, kanan)
    return tertinggi_kiri if tertinggi_kiri['pendapatan'] > tertinggi_kanan['pendapatan'] else tertinggi_kanan

def cetak_hasil(judul, hari_tertinggi, waktu):
    print(f"{'='*50}\n{judul}\n{'='*50}")
    print(f"Tanggal    : {hari_tertinggi['tanggal']}")
    print(f"Pendapatan : Rp {hari_tertinggi['pendapatan']:,}")
    print(f"Waktu      : {waktu:.8f} detik\n")
