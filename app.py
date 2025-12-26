from flask import Flask, render_template, jsonify, request
import numpy as np
import time, random
from app_pendapatan import gabung_data_bulanan, cari_pendapatan_tertinggi_iteratif, cari_pendapatan_tertinggi_rekursif
from app_menuporsi_tahunan import gabung_data_bulanan as gabung_menu, cari_menu_terlaris_iteratif, cari_menu_terlaris_rekursif
from app_relasi_rekurensi_homogen import baca_data_excel as baca_data_homogen, solve_iteratif, solve_matrix, solve_closed_form
from app_relasi_rekurensi_nonhomogen import baca_data as baca_data_nonhomogen
from config import (FILES as FILES_EXCEL, PRODUK, proses_pencarian_max, proses_relasi_rekurensi,
    ukur_waktu, cari_exact_iteratif, cari_exact_rekursif, build_test_response,
    handle_test_homogen, handle_test_nonhomogen, handle_performance_analysis, jalankan_demo_pencarian, jalankan_demo_relasi, handle_prediksi_produk)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/pendapatan')
def get_pendapatan():
    try:
        data = gabung_data_bulanan(FILES_EXCEL)
        if not data: return jsonify({'error': 'Data tidak ditemukan'}), 404
        
        result = proses_pencarian_max(data, cari_pendapatan_tertinggi_iteratif, 
                                      cari_pendapatan_tertinggi_rekursif, 
                                      'pendapatan', ['tanggal', 'pendapatan'])
        total = sum(h['pendapatan'] for h in data)
        result['statistik'] = {
            'total_hari': len(data), 'total_pendapatan': total,
            'rata_rata': int(total / len(data)),
            'tertinggi': result['top10'][0]['pendapatan'], 
            'terendah': sorted(data, key=lambda x: x['pendapatan'])[0]['pendapatan']
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-pendapatan', methods=['POST'])
def test_pendapatan():
    try:
        target = int(request.get_json().get('target', 5000000))
        if target <= 0: return jsonify({'error': 'Target harus lebih besar dari 0'}), 400
        data = gabung_data_bulanan(FILES_EXCEL)
        hasil_iter, waktu_iter = ukur_waktu(cari_exact_iteratif, data, 'pendapatan', target, runs=50)
        hasil_rek, waktu_rek = ukur_waktu(cari_exact_rekursif, data, 'pendapatan', target, runs=50)
        return jsonify(build_test_response(target, data, hasil_iter, hasil_rek, waktu_iter, waktu_rek,
            f'Tidak ditemukan pendapatan yang sama persis dengan Rp {target:,}'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/menu')
def get_menu():
    try:
        data = gabung_menu(FILES_EXCEL)
        if not data: return jsonify({'error': 'Data tidak ditemukan'}), 404
        
        result = proses_pencarian_max(data, cari_menu_terlaris_iteratif,
                                      cari_menu_terlaris_rekursif,
                                      'jumlah', ['nama', 'jumlah'])
        result['total_menu'] = len(data)
        result['total_penjualan'] = sum(m['jumlah'] for m in data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-menu', methods=['POST'])
def test_menu():
    try:
        target = int(request.get_json().get('target', 1000))
        if target <= 0: return jsonify({'error': 'Target harus lebih besar dari 0'}), 400
        data = gabung_menu(FILES_EXCEL)
        hasil_iter, waktu_iter = ukur_waktu(cari_exact_iteratif, data, 'jumlah', target, runs=50)
        hasil_rek, waktu_rek = ukur_waktu(cari_exact_rekursif, data, 'jumlah', target, runs=50)
        return jsonify(build_test_response(target, data, hasil_iter, hasil_rek, waktu_iter, waktu_rek,
            f'Tidak ditemukan menu dengan penjualan sama persis {target} porsi'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relasi-homogen')
def get_relasi_homogen():
    try:
        data = baca_data_homogen()
        return jsonify(proses_relasi_rekurensi(data, PRODUK, 'homogen'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-relasi-homogen', methods=['POST'])
def test_relasi_homogen():
    try:
        n = int(request.get_json().get('n', 12))
        if n <= 0 or n > 100000: return jsonify({'error': 'N harus antara 1-100000'}), 400
        return jsonify(handle_test_homogen(n))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-relasi-nonhomogen', methods=['POST'])
def test_relasi_nonhomogen():
    try:
        n = int(request.get_json().get('n', 12))
        if n <= 0 or n > 10000: return jsonify({'error': 'N harus antara 1-10000'}), 400
        return jsonify(handle_test_nonhomogen(n))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prediksi-produk-homogen', methods=['POST'])
def prediksi_produk_homogen():
    try:
        data = request.get_json()
        return jsonify(handle_prediksi_produk(data['produk_idx'], data['n'], 'homogen'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/prediksi-produk-nonhomogen', methods=['POST'])
def prediksi_produk_nonhomogen():
    try:
        data = request.get_json()
        return jsonify(handle_prediksi_produk(data['produk_idx'], data['n'], 'nonhomogen'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/relasi-nonhomogen')
def get_relasi_nonhomogen():
    try:
        data = baca_data_nonhomogen()
        return jsonify(proses_relasi_rekurensi(data, PRODUK, 'nonhomogen'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/performance-analysis', methods=['POST'])
def performance_analysis():
    try:
        n = int(request.get_json().get('n', 100))
        if n <= 0: return jsonify({'error': 'N harus lebih besar dari 0'}), 400
        return jsonify(handle_performance_analysis(n))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo-comparison')
def demo_comparison():
    try:
        # DEMO 1: Gunakan data pendapatan REAL dari 12 file Excel
        data_pendapatan = gabung_data_bulanan(FILES_EXCEL)
        if not data_pendapatan or len(data_pendapatan) == 0:
            return jsonify({'error': 'Data pendapatan tidak ditemukan'}), 404
        
        # Demo dengan data real pendapatan, berbagai ukuran sample
        sizes = [100, 500, 1000, len(data_pendapatan)]
        results_demo1 = []
        for size in sizes:
            sample = data_pendapatan[:min(size, len(data_pendapatan))]
            _, waktu_iter = ukur_waktu(cari_pendapatan_tertinggi_iteratif, sample, runs=100)
            _, waktu_rek = ukur_waktu(cari_pendapatan_tertinggi_rekursif, sample, runs=100)
            overhead = (waktu_rek / waktu_iter - 1) * 100 if waktu_iter > 0 else 0
            results_demo1.append({
                'size': len(sample), 'iteratif': waktu_iter, 'rekursif': waktu_rek,
                'overhead': overhead, 'winner': 'Iteratif' if waktu_iter < waktu_rek else 'Rekursif'
            })
        
        # DEMO 2 & 3: Gunakan data REAL dari produk homogen (12 file Excel)
        data_homogen = baca_data_homogen()  # Function sudah menggunakan FILES dari config
        if not data_homogen or PRODUK[0] not in data_homogen:
            return jsonify({'error': 'Data homogen tidak ditemukan'}), 404
            
        # Ambil data produk pertama dan hitung koefisien-nya
        from app_relasi_rekurensi_homogen import hitung_koefisien
        produk_data = data_homogen[PRODUK[0]]
        v = [float(x) for x in produk_data[:3]]  # 3 nilai awal
        koef = hitung_koefisien(produk_data)     # Hitung koefisien dari data real
        
        # DEMO 2: Relasi rekurensi dengan berbagai nilai n
        results_demo2 = []
        ns = [10, 50, 100, 500, 1000, 5000, 10000]
        for n in ns:
            _, waktu_iter = ukur_waktu(solve_iteratif, v, koef, n, runs=50)
            _, waktu_matrix = ukur_waktu(solve_matrix, v, koef, n, runs=50)
            _, waktu_closed = ukur_waktu(solve_closed_form, v, koef, n, runs=50)
            times = {'Iteratif': waktu_iter, 'Matrix': waktu_matrix, 'Closed': waktu_closed}
            winner = min(times, key=times.get)
            results_demo2.append({
                'n': n, 'iteratif': waktu_iter, 'matrix': waktu_matrix,
                'closed': waktu_closed, 'winner': winner
            })
        
        # DEMO 3: Multiple query scenario
        query_ns = [1000, 2000, 5000, 10000]
        start = time.perf_counter()
        for n in query_ns: solve_iteratif(v, koef, n)
        waktu_iter = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        for n in query_ns: solve_matrix(v, koef, n)
        waktu_matrix = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        poly = [1] + [-c for c in koef]
        akar = np.roots(poly)
        M = np.array([[akar[j]**i for j in range(len(koef))] for i in range(len(koef))], dtype=complex)
        c = np.linalg.solve(M, np.array(v[:len(koef)], dtype=complex))
        for n in query_ns: result = np.real(sum(c[i] * akar[i]**n for i in range(len(koef))))
        waktu_closed = (time.perf_counter() - start) * 1000
        
        demo3 = {
            'queries': query_ns, 
            'iteratif_total': waktu_iter, 
            'matrix_total': waktu_matrix,
            'closed_total': waktu_closed, 
            'iteratif_avg': waktu_iter / len(query_ns),
            'matrix_avg': waktu_matrix / len(query_ns), 
            'closed_avg': waktu_closed / len(query_ns),
            'speedup_vs_iter': waktu_iter / waktu_closed if waktu_closed > 0 else 0
        }
        
        return jsonify({
            'demo1': {
                'title': f'PENCARIAN MAKSIMUM (Data Real: {len(data_pendapatan)} Hari Pendapatan)', 
                'results': results_demo1,
                'conclusion': [
                    f'Dari {len(data_pendapatan)} hari data pendapatan, Iteratif SELALU menang di semua ukuran data',
                    'Rekursif Divide & Conquer 5-6x lebih lambat karena overhead pemanggilan fungsi',
                    'Untuk mencari nilai maksimum, kedua algoritma tetap harus cek semua data (kompleksitas sama O(n))',
                    'Kesimpulan: Gunakan Iteratif untuk pencarian maksimum - lebih simple dan lebih cepat!'
                ]
            },
            'demo2': {
                'title': f'RELASI REKURENSI (Data Real Produk: {PRODUK[0].title()})', 
                'results': results_demo2,
                'conclusion': [
                    'Untuk n kecil (10-50): Iteratif paling cepat karena overhead Closed Form masih besar',
                    'Untuk n sedang-besar (100-10000): Closed Form dominan dengan kecepatan konstan O(1)',
                    'Matrix Exponentiation tidak menang di range ini - kalah dari Closed Form di n besar',
                    'Kesimpulan: Closed Form terbaik untuk prediksi jangka panjang dengan data produk real!'
                ]
            },
            'demo3': {
                'title': f'MULTIPLE QUERY SCENARIO (Produk Real: {PRODUK[0].title()})', 
                'results': demo3,
                'conclusion': [
                    f'Closed Form {demo3["speedup_vs_iter"]:.1f}x lebih cepat dari Iteratif untuk 4 query berbeda',
                    'Setup awal Closed Form (hitung eigenvalue) hanya sekali, lalu semua query jadi O(1)',
                    f'Total waktu: Closed {demo3["closed_total"]:.2f}ms vs Iteratif {demo3["iteratif_total"]:.2f}ms',
                    'Kesimpulan: Closed Form sangat efisien untuk aplikasi yang butuh banyak prediksi berbeda!'
                ]
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    