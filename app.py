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
    solve_iteratif, solve_matrix, solve_closed_form
)
from app_relasi_rekurensi_nonhomogen import (
    baca_data as baca_data_nonhomogen, hitung_koef_nonhom,
    solve
)
from config import BULAN, FILES as FILES_EXCEL, PRODUK, generate_data_dummy, hitung_error_prediksi, format_response_algoritma, format_hasil_prediksi

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/pendapatan')
def get_pendapatan():
    try:
        data_pendapatan = gabung_data_bulanan(FILES_EXCEL)
        if not data_pendapatan: return jsonify({'error': 'Data tidak ditemukan'}), 404
        
        data_sorted = sorted(data_pendapatan, key=lambda x: x['pendapatan'], reverse=True)
        tertinggi_it, waktu_it = hitung_waktu_algoritma(cari_pendapatan_tertinggi_iteratif, data_pendapatan)
        tertinggi_rk, waktu_rk = hitung_waktu_algoritma(cari_pendapatan_tertinggi_rekursif, data_pendapatan)
        total = sum(h['pendapatan'] for h in data_pendapatan)
        
        return jsonify({
            'top10': data_sorted[:10],
            'iteratif': format_response_algoritma(tertinggi_it, waktu_it, ['tanggal', 'pendapatan']),
            'rekursif': format_response_algoritma(tertinggi_rk, waktu_rk, ['tanggal', 'pendapatan']),
            'statistik': {
                'total_hari': len(data_pendapatan), 'total_pendapatan': total,
                'rata_rata': int(total / len(data_pendapatan)),
                'tertinggi': data_sorted[0]['pendapatan'], 'terendah': data_sorted[-1]['pendapatan']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/menu')
def get_menu():
    try:
        semua_menu = gabung_menu(FILES_EXCEL)
        if not semua_menu: return jsonify({'error': 'Data tidak ditemukan'}), 404
        
        semua_menu = sorted(semua_menu, key=lambda x: x['jumlah'], reverse=True)
        terlaris_it, waktu_it = hitung_waktu_algoritma(cari_menu_terlaris_iteratif, semua_menu)
        terlaris_rk, waktu_rk = hitung_waktu_algoritma(cari_menu_terlaris_rekursif, semua_menu)
        
        return jsonify({
            'top10': semua_menu[:10],
            'iteratif': format_response_algoritma(terlaris_it, waktu_it, ['nama', 'jumlah']),
            'rekursif': format_response_algoritma(terlaris_rk, waktu_rk, ['nama', 'jumlah']),
            'total_menu': len(semua_menu), 'total_penjualan': sum(m['jumlah'] for m in semua_menu)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relasi-homogen')
def get_relasi_homogen():
    try:
        data = baca_data_homogen()
        if all(sum(data.get(p, [0])) == 0 for p in PRODUK): data = generate_data_dummy(data, PRODUK)
        
        hasil = []
        for p in PRODUK:
            d = data.get(p, [])
            if sum(d) == 0 or len(d) < 4: continue
            
            nilai_awal = [float(x) for x in d[:3]]
            koef = hitung_koefisien(d)
            prediksi = {
                'iteratif': solve_iteratif(nilai_awal, koef, 12)[0],
                'matrix': solve_matrix(nilai_awal, koef, 12)[0],
                'closed': solve_closed_form(nilai_awal, koef, 12)[0]
            }
            rata_error = hitung_error_prediksi(d, lambda i: solve_iteratif(nilai_awal, koef, i)[0])
            hasil.append(format_hasil_prediksi(p, d, koef, nilai_awal, prediksi, rata_error))
        
        return jsonify(hasil)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relasi-nonhomogen')
def get_relasi_nonhomogen():
    try:
        data = baca_data_nonhomogen()
        if all(sum(data.get(p, [0])) == 0 for p in PRODUK): data = generate_data_dummy(data, PRODUK)
        
        hasil = []
        for p in PRODUK:
            d = data.get(p, [])
            if sum(d) == 0 or len(d) < 4: continue
            
            koef, nilai_f = hitung_koef_nonhom(d)
            nilai_awal = [float(x) for x in d[:3]]
            prediksi = {
                'bulan_6': solve(nilai_awal, koef, nilai_f, 6, 'iteratif'),
                'bulan_12': solve(nilai_awal, koef, nilai_f, 12, 'iteratif')
            }
            rata_error = hitung_error_prediksi(d, lambda i: solve(nilai_awal, koef, nilai_f, i, 'iteratif'))
            is_nonhomogen = abs(sum(nilai_f[3:]))/(sum(d[3:])+0.1)*100 > 5
            
            extra = {
                'f_n': [f"{x:.0f}" for x in nilai_f[3:]],
                'status': 'VALID NON-HOMOGEN' if is_nonhomogen else 'Dominan HOMOGEN'
            }
            hasil.append(format_hasil_prediksi(p, d, koef, nilai_awal, prediksi, rata_error, extra))
        
        return jsonify(hasil)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance-analysis', methods=['POST'])
def performance_analysis():
    try:
        n = int(request.get_json().get('n', 100))
        if n <= 0: return jsonify({'error': 'N harus lebih besar dari 0'}), 400
        
        sizes = [s for s in [1,10,20,50,100,500,1000,5000,10000,50000,100000] if s <= n]
        if n not in sizes: sizes.append(n)
        sizes.sort()
        
        hasil = {k: [] for k in ['sizes','iteratif_pendapatan','rekursif_pendapatan','iteratif_menu','rekursif_menu','matrix_homogen','iteratif_homogen','nonhomogen']}
        hasil['sizes'] = sizes
        
        benchmark = lambda f, *args: (lambda: (t := __import__('time').perf_counter(), f(*args), (__import__('time').perf_counter() - t) * 1000)[-1])()
        
        for size in sizes:
            data_pend = [{'tanggal': f'2024-01-{(i%28)+1:02d}', 'pendapatan': random.randint(100000, 5000000)} for i in range(size)]
            hasil['iteratif_pendapatan'].append(benchmark(cari_pendapatan_tertinggi_iteratif, data_pend))
            hasil['rekursif_pendapatan'].append(benchmark(cari_pendapatan_tertinggi_rekursif, data_pend))
            
            data_menu = [{'nama': f'Menu {i}', 'jumlah': random.randint(10, 500)} for i in range(size)]
            hasil['iteratif_menu'].append(benchmark(cari_menu_terlaris_iteratif, data_menu))
            hasil['rekursif_menu'].append(benchmark(cari_menu_terlaris_rekursif, data_menu))
            
            if size < 3:
                hasil['matrix_homogen'].append(0)
                hasil['iteratif_homogen'].append(0)
                hasil['nonhomogen'].append(0)
            else:
                nilai_awal = [random.uniform(500, 1000) for _ in range(3)]
                koef = [0.5, 0.3, 0.2]
                n_calc = min(size, 50)
                try:
                    hasil['iteratif_homogen'].append(benchmark(lambda: solve_iteratif(nilai_awal, koef, n_calc)))
                    hasil['matrix_homogen'].append(benchmark(lambda: solve_matrix(nilai_awal, koef, n_calc)))
                    nilai_f = [random.uniform(10, 100) for _ in range(size)]
                    hasil['nonhomogen'].append(benchmark(lambda: solve(nilai_awal, koef, nilai_f, n_calc, 'iteratif')))
                except:
                    hasil['iteratif_homogen'].append(0)
                    hasil['matrix_homogen'].append(0)
                    hasil['nonhomogen'].append(0)
        
        return jsonify(hasil)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    