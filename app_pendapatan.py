import pandas as pd
import time

def baca_pendapatan_harian(file_excel):
    df = pd.read_excel(file_excel, sheet_name='sales', header=None)
    baris_kas = df[df[1].astype(str).str.lower() == 'kas']
    hasil = []
    for _, baris in baris_kas.iterrows():
        tanggal = baris[0]
        pendapatan = pd.to_numeric(baris[5], errors='coerce')
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
    tertinggi = data[0]
    for hari in data[1:]:
        if hari['pendapatan'] > tertinggi['pendapatan']:
            tertinggi = hari
    return tertinggi

def cari_pendapatan_tertinggi_rekursif(data, kiri=0, kanan=None):
    if kanan is None: kanan = len(data) - 1
    if kiri == kanan: return data[kiri]
    
    tengah = (kiri + kanan) // 2
    tertinggi_kiri = cari_pendapatan_tertinggi_rekursif(data, kiri, tengah)
    tertinggi_kanan = cari_pendapatan_tertinggi_rekursif(data, tengah + 1, kanan)
    return tertinggi_kiri if tertinggi_kiri['pendapatan'] > tertinggi_kanan['pendapatan'] else tertinggi_kanan

def hitung_waktu_algoritma(fungsi_cari, data):
    mulai = time.perf_counter()
    hasil = fungsi_cari(data)
    waktu = time.perf_counter() - mulai
    return hasil, waktu

def cetak_hasil(judul, hari_tertinggi, waktu):
    print(f"{'='*50}\n{judul}\n{'='*50}")
    print(f"Tanggal    : {hari_tertinggi['tanggal']}")
    print(f"Pendapatan : Rp {hari_tertinggi['pendapatan']:,}")
    print(f"Waktu      : {waktu:.8f} detik\n")

if __name__ == "__main__":
    bulan = ['jan','feb','mar','apr','mei','jun','jul','aug','sep','okt','nov','des']
    file_excel = [f'databebek2024/{b}24.xlsx' for b in bulan]
    
    data_pendapatan = gabung_data_bulanan(file_excel)
    if not data_pendapatan:
        print("ERROR: Data tidak ditemukan!")
        exit(1)
    
    data_pendapatan_sorted = sorted(data_pendapatan, key=lambda x: x['pendapatan'], reverse=True)
    pd.DataFrame(data_pendapatan_sorted).to_csv('pendapatan_harian_2024.csv', index=False)
    
    print("="*50)
    print("Top 10 Pendapatan Harian Tertinggi 2024")
    print("="*50)
    for i, hari in enumerate(data_pendapatan_sorted[:10], 1):
        print(f"{i:2d}. {hari['tanggal']} : Rp {hari['pendapatan']:>10,}")
    print()
    
    tertinggi, waktu = hitung_waktu_algoritma(cari_pendapatan_tertinggi_iteratif, data_pendapatan)
    cetak_hasil("Algoritma Iteratif", tertinggi, waktu)
    
    tertinggi, waktu = hitung_waktu_algoritma(cari_pendapatan_tertinggi_rekursif, data_pendapatan)
    cetak_hasil("Algoritma Rekursif (Divide & Conquer)", tertinggi, waktu)
    
    total = sum(h['pendapatan'] for h in data_pendapatan)
    print("="*50)
    print("Statistik Pendapatan 2024")
    print("="*50)
    print(f"Total Hari      : {len(data_pendapatan)} hari")
    print(f"Total Pendapatan: Rp {total:,}")
    print(f"Rata-rata/Hari  : Rp {total / len(data_pendapatan):,.0f}")
    print(f"Tertinggi       : Rp {data_pendapatan_sorted[0]['pendapatan']:,}")
    print(f"Terendah        : Rp {data_pendapatan_sorted[-1]['pendapatan']:,}")
    print("="*50)
