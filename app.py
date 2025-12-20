from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import time
import random
from app_pendapatan import (
    gabung_data_bulanan, cari_pendapatan_tertinggi_iteratif,
    cari_pendapatan_tertinggi_rekursif, hitung_waktu_algoritma
)
from app_menuporsi_tahunan import (
    gabung_data_bulanan as gabung_menu, cari_menu_terlaris_iteratif,
    cari_menu_terlaris_rekursif
)
from app_relasi_rekurensi_homogen import (
    baca_data_excel as baca_data_homogen, hitung_koefisien,
    solve_iteratif, solve_matrix, solve_closed_form,
    PRODUK as PRODUK_HOMOGEN
)
from app_relasi_rekurensi_nonhomogen import (
    baca_data as baca_data_nonhomogen, hitung_koef_nonhom,
    solve, PRODUK
)

app = Flask(__name__)

BULAN = ['jan','feb','mar','apr','mei','jun','jul','aug','sep','okt','nov','des']
FILES_EXCEL = [f'databebek2024/{b}24.xlsx' for b in BULAN]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/pendapatan')
def get_pendapatan():
    try:
        data_pendapatan = gabung_data_bulanan(FILES_EXCEL)
        if not data_pendapatan:
            return jsonify({'error': 'Data tidak ditemukan'}), 404
        
        data_sorted = sorted(data_pendapatan, key=lambda x: x['pendapatan'], reverse=True)
        
        # Hitung dengan kedua algoritma
        tertinggi_it, waktu_it = hitung_waktu_algoritma(cari_pendapatan_tertinggi_iteratif, data_pendapatan)
        tertinggi_rk, waktu_rk = hitung_waktu_algoritma(cari_pendapatan_tertinggi_rekursif, data_pendapatan)
        
        # Statistik
        total = sum(h['pendapatan'] for h in data_pendapatan)
        
        return jsonify({
            'top10': data_sorted[:10],
            'iteratif': {
                'tanggal': tertinggi_it['tanggal'],
                'pendapatan': tertinggi_it['pendapatan'],
                'waktu': f"{waktu_it:.8f}"
            },
            'rekursif': {
                'tanggal': tertinggi_rk['tanggal'],
                'pendapatan': tertinggi_rk['pendapatan'],
                'waktu': f"{waktu_rk:.8f}"
            },
            'statistik': {
                'total_hari': len(data_pendapatan),
                'total_pendapatan': total,
                'rata_rata': int(total / len(data_pendapatan)),
                'tertinggi': data_sorted[0]['pendapatan'],
                'terendah': data_sorted[-1]['pendapatan']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/menu')
def get_menu():
    try:
        semua_menu = gabung_menu(FILES_EXCEL)
        if not semua_menu:
            return jsonify({'error': 'Data tidak ditemukan'}), 404
        
        semua_menu = sorted(semua_menu, key=lambda x: x['jumlah'], reverse=True)
        
        # Hitung dengan kedua algoritma
        terlaris_it, waktu_it = hitung_waktu_algoritma(cari_menu_terlaris_iteratif, semua_menu)
        terlaris_rk, waktu_rk = hitung_waktu_algoritma(cari_menu_terlaris_rekursif, semua_menu)
        
        return jsonify({
            'top10': semua_menu[:10],
            'iteratif': {
                'nama': terlaris_it['nama'],
                'jumlah': terlaris_it['jumlah'],
                'waktu': f"{waktu_it:.8f}"
            },
            'rekursif': {
                'nama': terlaris_rk['nama'],
                'jumlah': terlaris_rk['jumlah'],
                'waktu': f"{waktu_rk:.8f}"
            },
            'total_menu': len(semua_menu),
            'total_penjualan': sum(m['jumlah'] for m in semua_menu)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relasi-homogen')
def get_relasi_homogen():
    try:
        data = baca_data_homogen()
        if all(sum(data.get(p, [0])) == 0 for p in PRODUK_HOMOGEN):
            for i, p in enumerate(PRODUK_HOMOGEN):
                data[p] = [500 + j * (50 + i*20) for j in range(12)]
        
        hasil = []
        for p in PRODUK_HOMOGEN:
            d = data.get(p, [])
            if sum(d) == 0 or len(d) < 4:
                continue
            
            v = [float(x) for x in d[:3]]
            k = hitung_koefisien(d)
            
            # Predict untuk bulan ke-12
            pred_12_it, _ = solve_iteratif(v, k, 12)
            pred_12_m, _ = solve_matrix(v, k, 12)
            pred_12_c, _ = solve_closed_form(v, k, 12)
            
            # Hitung error
            errors = []
            for i in range(3, len(d)):
                pred, _ = solve_iteratif(v, k, i)
                e = abs(pred - d[i]) / d[i] * 100 if d[i] else 0
                errors.append(e)
            
            hasil.append({
                'produk': p,
                'koef': [f"{c:.6f}" for c in k],
                'sum_koef': f"{sum(k):.6f}",
                'data_awal': [int(x) for x in d[:3]],
                'prediksi': {
                    'iteratif': f"{pred_12_it:.0f}",
                    'matrix': f"{pred_12_m:.0f}",
                    'closed': f"{pred_12_c:.0f}"
                },
                'rata_rata_error': f"{sum(errors) / len(errors) if errors else 0:.2f}%"
            })
        
        return jsonify(hasil)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relasi-nonhomogen')
def get_relasi_nonhomogen():
    try:
        data = baca_data_nonhomogen()
        if all(sum(data.get(p, [0])) == 0 for p in PRODUK):
            for i, p in enumerate(PRODUK):
                data[p] = [500 + j * (50 + i*20) for j in range(12)]
        
        hasil = []
        for p in PRODUK:
            d = data.get(p, [])
            if sum(d) == 0 or len(d) < 4:
                continue
            
            k, f_n = hitung_koef_nonhom(d)
            v = [float(x) for x in d[:3]]
            
            # Predict
            pred_6 = solve(v, k, f_n, 6, 'iteratif')
            pred_12 = solve(v, k, f_n, 12, 'iteratif')
            
            # Error
            errors = []
            for i in range(3, len(d)):
                pred = solve(v, k, f_n, i, "iteratif")
                e = abs(pred - d[i]) / d[i] * 100 if d[i] else 0
                errors.append(e)
            
            hasil.append({
                'produk': p,
                'koef': [f"{c:.4f}" for c in k],
                'sum_koef': f"{sum(k):.4f}",
                'data_awal': [int(x) for x in v],
                'f_n': [f"{x:.0f}" for x in f_n[3:]],
                'prediksi': {
                    'bulan_6': f"{pred_6:.0f}",
                    'bulan_12': f"{pred_12:.0f}"
                },
                'rata_rata_error': f"{sum(errors) / len(errors) if errors else 0:.2f}%",
                'status': 'VALID NON-HOMOGEN' if abs(sum(f_n[3:]))/(sum(d[3:])+0.1)*100 > 5 else 'Dominan HOMOGEN'
            })
        
        return jsonify(hasil)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance-analysis', methods=['POST'])
def performance_analysis():
    try:
        data = request.get_json()
        n = int(data.get('n', 100))
        
        if n <= 0:
            return jsonify({'error': 'N harus lebih besar dari 0'}), 400
        
        # Tentukan ukuran data yang akan dianalisis
        sizes = []
        for size in [1, 10, 20, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]:
            if size <= n:
                sizes.append(size)
        if n not in sizes:
            sizes.append(n)
        sizes.sort()
        
        hasil = {
            'sizes': sizes,
            'iteratif_pendapatan': [],
            'rekursif_pendapatan': [],
            'iteratif_menu': [],
            'rekursif_menu': [],
            'matrix_homogen': [],
            'iteratif_homogen': [],
            'nonhomogen': []
        }
        
        # Analisis untuk Pendapatan
        for size in sizes:
            data_pendapatan = [
                {'tanggal': f'2024-01-{(i%28)+1:02d}', 'pendapatan': random.randint(100000, 5000000)}
                for i in range(size)
            ]
            
            # Iteratif Pendapatan
            waktu_it = time.perf_counter()
            _ = cari_pendapatan_tertinggi_iteratif(data_pendapatan)
            waktu_it = (time.perf_counter() - waktu_it) * 1000  # Convert to ms
            hasil['iteratif_pendapatan'].append(waktu_it)
            
            # Rekursif Pendapatan
            waktu_rk = time.perf_counter()
            _ = cari_pendapatan_tertinggi_rekursif(data_pendapatan)
            waktu_rk = (time.perf_counter() - waktu_rk) * 1000
            hasil['rekursif_pendapatan'].append(waktu_rk)
        
        # Analisis untuk Menu
        for size in sizes:
            data_menu = [
                {'nama': f'Menu {i}', 'jumlah': random.randint(10, 500)}
                for i in range(size)
            ]
            
            # Iteratif Menu
            waktu_it = time.perf_counter()
            _ = cari_menu_terlaris_iteratif(data_menu)
            waktu_it = (time.perf_counter() - waktu_it) * 1000
            hasil['iteratif_menu'].append(waktu_it)
            
            # Rekursif Menu
            waktu_rk = time.perf_counter()
            _ = cari_menu_terlaris_rekursif(data_menu)
            waktu_rk = (time.perf_counter() - waktu_rk) * 1000
            hasil['rekursif_menu'].append(waktu_rk)
        
        # Analisis untuk Relasi Homogen
        for size in sizes:
            if size < 3:
                hasil['matrix_homogen'].append(0)
                hasil['iteratif_homogen'].append(0)
                continue
            
            v = [random.uniform(500, 1000) for _ in range(3)]
            k = [0.5, 0.3, 0.2]
            
            # Iteratif Homogen
            waktu = time.perf_counter()
            try:
                _, _ = solve_iteratif(v, k, min(size, 50))
            except:
                pass
            waktu = (time.perf_counter() - waktu) * 1000
            hasil['iteratif_homogen'].append(waktu)
            
            # Matrix Homogen
            waktu = time.perf_counter()
            try:
                _, _ = solve_matrix(v, k, min(size, 50))
            except:
                pass
            waktu = (time.perf_counter() - waktu) * 1000
            hasil['matrix_homogen'].append(waktu)
        
        # Analisis untuk Non-Homogen
        for size in sizes:
            if size < 3:
                hasil['nonhomogen'].append(0)
                continue
            
            v = [random.uniform(500, 1000) for _ in range(3)]
            k = [0.5, 0.3, 0.2]
            f_n = [random.uniform(10, 100) for _ in range(size)]
            
            waktu = time.perf_counter()
            try:
                _ = solve(v, k, f_n, min(size, 50), 'iteratif')
            except:
                pass
            waktu = (time.perf_counter() - waktu) * 1000
            hasil['nonhomogen'].append(waktu)
        
        return jsonify(hasil)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
