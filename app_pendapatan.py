import pandas as pd
import time

def baca_pendapatan_harian(file_excel):
    """Baca pendapatan harian dari sheet sales"""
    df = pd.read_excel(file_excel, sheet_name='sales', header=None)
    
    # Filter baris yang 'kas' (pendapatan harian)
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
    """Gabung pendapatan harian dari 12 file bulanan"""
    semua_data = []
    
    for file in daftar_file:
        try:
            print(f"  Membaca {file}...")
            data_bulan = baca_pendapatan_harian(file)
            semua_data.extend(data_bulan)
        except Exception as e:
            print(f"  ⚠ Error: {e}")
    
    return semua_data

def cari_pendapatan_tertinggi_iteratif(data):
    """Cari hari dengan pendapatan tertinggi menggunakan loop"""
    tertinggi = data[0]
    for hari in data[1:]:
        if hari['pendapatan'] > tertinggi['pendapatan']:
            tertinggi = hari
    return tertinggi

def cari_pendapatan_tertinggi_rekursif(data, kiri=0, kanan=None):
    """Cari hari dengan pendapatan tertinggi menggunakan divide & conquer"""
    if kanan is None:
        kanan = len(data) - 1
    
    if kiri == kanan:
        return data[kiri]
    
    tengah = (kiri + kanan) // 2
    tertinggi_kiri = cari_pendapatan_tertinggi_rekursif(data, kiri, tengah)
    tertinggi_kanan = cari_pendapatan_tertinggi_rekursif(data, tengah + 1, kanan)
    
    return tertinggi_kiri if tertinggi_kiri['pendapatan'] > tertinggi_kanan['pendapatan'] else tertinggi_kanan

def hitung_waktu_algoritma(fungsi_cari, data):
    """Hitung waktu eksekusi algoritma"""
    mulai = time.perf_counter()
    hasil = fungsi_cari(data)
    waktu = time.perf_counter() - mulai
    return hasil, waktu

def cetak_hasil(judul, hari_tertinggi, waktu):
    """Tampilkan hasil pencarian"""
    print("=" * 50)
    print(judul)
    print("=" * 50)
    print(f"Tanggal        : {hari_tertinggi['tanggal']}")
    print(f"Pendapatan     : Rp {hari_tertinggi['pendapatan']:,}")
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
    print("Memuat data pendapatan harian tahun 2024...")
    data_pendapatan = gabung_data_bulanan(file_excel)
    
    if not data_pendapatan:
        print("ERROR: Data pendapatan tidak ditemukan!")
        exit(1)
    
    # Urutkan berdasarkan pendapatan terbesar
    data_pendapatan_sorted = sorted(data_pendapatan, key=lambda x: x['pendapatan'], reverse=True)
    
    # Simpan hasil
    pd.DataFrame(data_pendapatan_sorted).to_csv('pendapatan_harian_2024.csv', index=False)
    print(f"✓ Tersimpan: pendapatan_harian_2024.csv ({len(data_pendapatan_sorted)} hari)\n")
    
    # Tampilkan top 10 hari dengan pendapatan tertinggi
    print("=" * 50)
    print("TOP 10 PENDAPATAN HARIAN TERTINGGI 2024")
    print("=" * 50)
    for i, hari in enumerate(data_pendapatan_sorted[:10], 1):
        print(f"{i:2d}. {hari['tanggal']} : Rp {hari['pendapatan']:>10,}")
    print()
    
    # Bandingkan 2 algoritma
    tertinggi, waktu = hitung_waktu_algoritma(cari_pendapatan_tertinggi_iteratif, data_pendapatan)
    cetak_hasil("ALGORITMA ITERATIF (Loop)", tertinggi, waktu)
    
    tertinggi, waktu = hitung_waktu_algoritma(cari_pendapatan_tertinggi_rekursif, data_pendapatan)
    cetak_hasil("ALGORITMA REKURSIF (Divide & Conquer)", tertinggi, waktu)
    
    # Statistik tambahan
    total_pendapatan = sum(h['pendapatan'] for h in data_pendapatan)
    rata_rata = total_pendapatan / len(data_pendapatan)
    
    print("=" * 50)
    print("STATISTIK PENDAPATAN 2024")
    print("=" * 50)
    print(f"Total Hari Operasional : {len(data_pendapatan)} hari")
    print(f"Total Pendapatan       : Rp {total_pendapatan:,}")
    print(f"Rata-rata Harian       : Rp {rata_rata:,.0f}")
    print(f"Pendapatan Tertinggi   : Rp {data_pendapatan_sorted[0]['pendapatan']:,}")
    print(f"Pendapatan Terendah    : Rp {data_pendapatan_sorted[-1]['pendapatan']:,}")
    print("=" * 50)
