function loadPendapatan() {
    showLoading();
    fetch('/api/pendapatan')
        .then(response => response.json())
        .then(data => {
            let html = '<div class="section-title">💰 Analisis Pendapatan Harian 2024</div>';
            
            // Top 10
            html += '<h3>Top 10 Pendapatan Tertinggi</h3>';
            html += '<div class="top-list">';
            data.top10.forEach((item, idx) => {
                html += `<div class="top-item">
                    <span class="top-item-rank">#${idx + 1}</span>
                    <span class="top-item-name">${item.tanggal}</span>
                    <span class="top-item-value">Rp ${item.pendapatan.toLocaleString('id-ID')}</span>
                </div>`;
            });
            html += '</div>';
            
            // Algorithm Results
            html += '<h3>Perbandingan Algoritma</h3>';
            html += '<div class="algorithm-results">';
            html += `<div class="algo-card">
                <h3>🔄 Algoritma Iteratif</h3>
                <p>Tanggal: <strong>${data.iteratif.tanggal}</strong></p>
                <div class="value">Rp ${data.iteratif.pendapatan.toLocaleString('id-ID')}</div>
                <div class="time">Waktu: ${data.iteratif.waktu} detik</div>
            </div>`;
            
            html += `<div class="algo-card">
                <h3>🌳 Algoritma Rekursif (D&C)</h3>
                <p>Tanggal: <strong>${data.rekursif.tanggal}</strong></p>
                <div class="value">Rp ${data.rekursif.pendapatan.toLocaleString('id-ID')}</div>
                <div class="time">Waktu: ${data.rekursif.waktu} detik</div>
            </div>`;
            html += '</div>';
            
            // Statistics
            html += '<h3>Statistik Pendapatan</h3>';
            html += '<div class="statistik">';
            html += `<div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <h4>Total Hari</h4>
                <div class="stat-value">${data.statistik.total_hari}</div>
            </div>`;
            html += `<div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <h4>Total Pendapatan</h4>
                <div class="stat-value">Rp ${(data.statistik.total_pendapatan / 1000000).toFixed(1)}M</div>
            </div>`;
            html += `<div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h4>Rata-rata Harian</h4>
                <div class="stat-value">Rp ${data.statistik.rata_rata.toLocaleString('id-ID')}</div>
            </div>`;
            html += `<div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <h4>Selisih (Tertinggi - Terendah)</h4>
                <div class="stat-value">Rp ${(data.statistik.tertinggi - data.statistik.terendah).toLocaleString('id-ID')}</div>
            </div>`;
            html += '</div>';
            
            document.getElementById('content').innerHTML = html;
        })
        .catch(err => {
            document.getElementById('content').innerHTML = '<div class="error">Error: ' + err.message + '</div>';
        });
}

function loadMenu() {
    showLoading();
    fetch('/api/menu')
        .then(response => response.json())
        .then(data => {
            let html = '<div class="section-title">🍗 Menu Terlaris Tahun 2024</div>';
            
            // Top 10
            html += '<h3>Top 10 Menu Terlaris</h3>';
            html += '<div class="top-list">';
            data.top10.forEach((item, idx) => {
                html += `<div class="top-item">
                    <span class="top-item-rank">#${idx + 1}</span>
                    <span class="top-item-name">${item.nama}</span>
                    <span class="top-item-value">${item.jumlah.toLocaleString('id-ID')} porsi</span>
                </div>`;
            });
            html += '</div>';
            
            // Algorithm Results
            html += '<h3>Perbandingan Algoritma</h3>';
            html += '<div class="algorithm-results">';
            html += `<div class="algo-card">
                <h3>🔄 Algoritma Iteratif</h3>
                <p>Menu: <strong>${data.iteratif.nama}</strong></p>
                <div class="value">${data.iteratif.jumlah.toLocaleString('id-ID')} porsi</div>
                <div class="time">Waktu: ${data.iteratif.waktu} detik</div>
            </div>`;
            
            html += `<div class="algo-card">
                <h3>🌳 Algoritma Rekursif (D&C)</h3>
                <p>Menu: <strong>${data.rekursif.nama}</strong></p>
                <div class="value">${data.rekursif.jumlah.toLocaleString('id-ID')} porsi</div>
                <div class="time">Waktu: ${data.rekursif.waktu} detik</div>
            </div>`;
            html += '</div>';
            
            // Statistics
            html += '<h3>Statistik Penjualan</h3>';
            html += '<div class="statistik">';
            html += `<div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <h4>Total Menu</h4>
                <div class="stat-value">${data.total_menu}</div>
            </div>`;
            html += `<div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <h4>Total Penjualan</h4>
                <div class="stat-value">${data.total_penjualan.toLocaleString('id-ID')}</div>
            </div>`;
            html += `<div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h4>Rata-rata per Menu</h4>
                <div class="stat-value">${Math.round(data.total_penjualan / data.total_menu).toLocaleString('id-ID')}</div>
            </div>`;
            html += '</div>';
            
            document.getElementById('content').innerHTML = html;
        })
        .catch(err => {
            document.getElementById('content').innerHTML = '<div class="error">Error: ' + err.message + '</div>';
        });
}

function loadHomogen() {
    showLoading();
    fetch('/api/relasi-homogen')
        .then(response => response.json())
        .then(data => {
            let html = '<div class="section-title">📊 Analisis Relasi Rekurensi Linier Homogen</div>';
            html += '<p style="color: #666; margin-bottom: 2rem;">Formula: T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3)</p>';
            
            data.forEach((produk, idx) => {
                html += `<div style="margin-bottom: 3rem; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">`;
                html += `<h3 style="color: #667eea; margin-bottom: 1rem;">Produk ${idx + 1}: ${produk.produk}</h3>`;
                
                html += `<div style="background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <p><strong>Koefisien:</strong> a=${produk.koef[0]}, b=${produk.koef[1]}, c=${produk.koef[2]}</p>
                    <p><strong>Jumlah Koefisien:</strong> ${produk.sum_koef}</p>
                    <p><strong>Data Awal (3 bulan):</strong> ${produk.data_awal.join(', ')}</p>
                </div>`;
                
                html += `<div style="background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <h4>Prediksi Bulan ke-12</h4>
                    <p>Metode Iteratif: <strong>${produk.prediksi.iteratif}</strong></p>
                    <p>Metode Matrix: <strong>${produk.prediksi.matrix}</strong></p>
                    <p>Metode Closed-Form: <strong>${produk.prediksi.closed}</strong></p>
                </div>`;
                
                html += `<div style="background: #fff3cd; padding: 1rem; border-radius: 5px;">
                    <p><strong>Rata-rata Error:</strong> ${produk.rata_rata_error}</p>
                </div>`;
                html += `</div>`;
            });
            
            document.getElementById('content').innerHTML = html;
        })
        .catch(err => {
            document.getElementById('content').innerHTML = '<div class="error">Error: ' + err.message + '</div>';
        });
}

function loadNonhomogen() {
    showLoading();
    fetch('/api/relasi-nonhomogen')
        .then(response => response.json())
        .then(data => {
            let html = '<div class="section-title">📈 Analisis Relasi Rekurensi Linier Non-Homogen</div>';
            html += '<p style="color: #666; margin-bottom: 2rem;">Formula: T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3) + f(n)</p>';
            
            data.forEach((produk, idx) => {
                html += `<div style="margin-bottom: 3rem; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">`;
                html += `<h3 style="color: #667eea; margin-bottom: 1rem;">Produk ${idx + 1}: ${produk.produk}</h3>`;
                
                html += `<div style="background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <p><strong>Koefisien Homogen:</strong> a=${produk.koef[0]}, b=${produk.koef[1]}, c=${produk.koef[2]}</p>
                    <p><strong>Jumlah Koefisien:</strong> ${produk.sum_koef}</p>
                    <p><strong>Data Awal:</strong> ${produk.data_awal.join(', ')}</p>
                    <p><strong>Non-homogen f(n):</strong> ${produk.f_n.join(', ')}</p>
                </div>`;
                
                html += `<div style="background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <h4>Prediksi</h4>
                    <p>Bulan ke-6: <strong>${produk.prediksi.bulan_6}</strong></p>
                    <p>Bulan ke-12: <strong>${produk.prediksi.bulan_12}</strong></p>
                </div>`;
                
                html += `<div style="background: #fff3cd; padding: 1rem; border-radius: 5px;">
                    <p><strong>Rata-rata Error:</strong> ${produk.rata_rata_error}</p>
                    <p><strong>Status:</strong> ${produk.status}</p>
                </div>`;
                html += `</div>`;
            });
            
            document.getElementById('content').innerHTML = html;
        })
        .catch(err => {
            document.getElementById('content').innerHTML = '<div class="error">Error: ' + err.message + '</div>';
        });
}

function showLoading() {
    document.getElementById('content').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Memuat data...</p>
        </div>
    `;
}

function loadPerformance() {
    let html = '<div class="section-title">⚡ Analisis Performa Algoritma</div>';
    
    html += `<div class="performance-form">
        <div class="form-group">
            <label for="input-n">Masukkan Nilai N (Ukuran Data Maksimal):</label>
            <input type="number" id="input-n" value="100000" min="1" max="10000000" placeholder="Contoh: 100000">
            <span class="helper-text">Minimal 1, Maksimal 10,000,000</span>
        </div>
        <button class="btn btn-primary" onclick="runPerformanceAnalysis()">🚀 Generate & Analisis</button>
    </div>`;
    
    html += '<div id="performance-results"></div>';
    
    document.getElementById('content').innerHTML = html;
}

function runPerformanceAnalysis() {
    const n = parseInt(document.getElementById('input-n').value);
    
    if (!n || n < 1) {
        alert('Masukkan nilai N yang valid (minimal 1)');
        return;
    }
    
    document.getElementById('performance-results').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Menganalisis performa dengan N = ${n.toLocaleString('id-ID')}...</p>
        </div>
    `;
    
    fetch('/api/performance-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ n: n })
    })
    .then(response => response.json())
    .then(data => {
        displayPerformanceResults(data);
    })
    .catch(err => {
        document.getElementById('performance-results').innerHTML = '<div class="error">Error: ' + err.message + '</div>';
    });
}

function displayPerformanceResults(data) {
    let html = '<h3>Hasil Analisis Performa</h3>';
    
    // Perbandingan Pendapatan
    html += '<div class="perf-section">';
    html += '<h4>📊 Algoritma Pencarian Pendapatan</h4>';
    html += createPerformanceChart('Pendapatan', data.sizes, 
        data.iteratif_pendapatan, data.rekursif_pendapatan);
    html += '<div class="perf-table">';
    html += '<table class="data-table">';
    html += '<thead><tr><th>Ukuran Data</th><th>Iteratif (ms)</th><th>Rekursif (ms)</th><th>Selisih</th></tr></thead>';
    html += '<tbody>';
    for (let i = 0; i < data.sizes.length; i++) {
        const it = data.iteratif_pendapatan[i];
        const rk = data.rekursif_pendapatan[i];
        const selisih = ((rk - it) / it * 100).toFixed(2);
        html += `<tr>
            <td>${data.sizes[i].toLocaleString('id-ID')}</td>
            <td>${it.toFixed(6)}</td>
            <td>${rk.toFixed(6)}</td>
            <td>${selisih}%</td>
        </tr>`;
    }
    html += '</tbody></table>';
    html += '</div></div>';
    
    // Perbandingan Menu
    html += '<div class="perf-section">';
    html += '<h4>🍗 Algoritma Pencarian Menu Terlaris</h4>';
    html += createPerformanceChart('Menu', data.sizes, 
        data.iteratif_menu, data.rekursif_menu);
    html += '<div class="perf-table">';
    html += '<table class="data-table">';
    html += '<thead><tr><th>Ukuran Data</th><th>Iteratif (ms)</th><th>Rekursif (ms)</th><th>Selisih</th></tr></thead>';
    html += '<tbody>';
    for (let i = 0; i < data.sizes.length; i++) {
        const it = data.iteratif_menu[i];
        const rk = data.rekursif_menu[i];
        const selisih = ((rk - it) / it * 100).toFixed(2);
        html += `<tr>
            <td>${data.sizes[i].toLocaleString('id-ID')}</td>
            <td>${it.toFixed(6)}</td>
            <td>${rk.toFixed(6)}</td>
            <td>${selisih}%</td>
        </tr>`;
    }
    html += '</tbody></table>';
    html += '</div></div>';
    
    // Perbandingan Relasi Homogen
    html += '<div class="perf-section">';
    html += '<h4>📈 Algoritma Relasi Rekurensi Homogen</h4>';
    html += createPerformanceChart('Homogen', data.sizes, 
        data.iteratif_homogen, data.matrix_homogen);
    html += '<div class="perf-table">';
    html += '<table class="data-table">';
    html += '<thead><tr><th>Ukuran Data</th><th>Iteratif (ms)</th><th>Matrix (ms)</th><th>Selisih</th></tr></thead>';
    html += '<tbody>';
    for (let i = 0; i < data.sizes.length; i++) {
        const it = data.iteratif_homogen[i];
        const m = data.matrix_homogen[i];
        const selisih = ((m - it) / it * 100).toFixed(2);
        html += `<tr>
            <td>${data.sizes[i].toLocaleString('id-ID')}</td>
            <td>${it.toFixed(6)}</td>
            <td>${m.toFixed(6)}</td>
            <td>${selisih}%</td>
        </tr>`;
    }
    html += '</tbody></table>';
    html += '</div></div>';
    
    // Kompleksitas
    html += '<div class="perf-section complexity">';
    html += '<h4>📐 Analisis Kompleksitas</h4>';
    html += `<div class="complexity-info">
        <div class="complexity-item">
            <h5>O(n) - Iteratif Pencarian</h5>
            <p>Linear: Waktu eksekusi bertambah seiring bertambahnya ukuran data secara proporsional</p>
        </div>
        <div class="complexity-item">
            <h5>O(n) - Rekursif Pencarian (Divide & Conquer)</h5>
            <p>Memiliki overhead rekursi lebih tinggi dibanding iteratif meski kompleksitas sama</p>
        </div>
        <div class="complexity-item">
            <h5>O(log n) - Matrix Exponentiation</h5>
            <p>Logaritmik: Lebih efisien untuk nilai n besar pada relasi rekurensi</p>
        </div>
    </div>`;
    html += '</div>';
    
    document.getElementById('performance-results').innerHTML = html;
}

function createPerformanceChart(title, sizes, data1, data2) {
    const maxValue = Math.max(...data1, ...data2);
    const chartHeight = 300;
    const chartWidth = Math.max(sizes.length * 80, 600);
    
    let html = `<div class="perf-chart-container" style="overflow-x: auto;">
        <svg viewBox="0 0 ${chartWidth} ${chartHeight + 50}" width="100%" height="400" style="background: #f8f9fa; border-radius: 5px;">`;
    
    // Axes
    html += `<line x1="50" y1="${chartHeight}" x2="${chartWidth - 20}" y2="${chartHeight}" stroke="#999" stroke-width="2"/>`;
    html += `<line x1="50" y1="10" x2="50" y2="${chartHeight}" stroke="#999" stroke-width="2"/>`;
    
    // Grid lines
    for (let i = 0; i <= 5; i++) {
        const y = chartHeight - (i * chartHeight / 5);
        html += `<line x1="45" y1="${y}" x2="${chartWidth - 20}" y2="${y}" stroke="#e0e0e0" stroke-width="1" stroke-dasharray="5,5"/>`;
        html += `<text x="10" y="${y + 4}" font-size="12" text-anchor="end">${(maxValue / 5 * i).toFixed(2)}</text>`;
    }
    
    // Data points
    const barWidth = (chartWidth - 70) / (sizes.length * 2.5);
    const spacing = (chartWidth - 70) / sizes.length;
    
    for (let i = 0; i < sizes.length; i++) {
        const x = 50 + i * spacing + spacing / 2;
        const h1 = (data1[i] / maxValue) * chartHeight;
        const h2 = (data2[i] / maxValue) * chartHeight;
        
        // Bars
        html += `<rect x="${x - barWidth * 1.2}" y="${chartHeight - h1}" width="${barWidth}" height="${h1}" fill="#667eea" opacity="0.8"/>`;
        html += `<rect x="${x - barWidth * 0.2}" y="${chartHeight - h2}" width="${barWidth}" height="${h2}" fill="#764ba2" opacity="0.8"/>`;
        
        // Labels
        html += `<text x="${x}" y="${chartHeight + 20}" font-size="11" text-anchor="middle" fill="#333">${sizes[i]}</text>`;
    }
    
    // Legend
    html += `<rect x="${chartWidth - 180}" y="15" width="160" height="60" fill="white" stroke="#ccc" stroke-width="1" rx="3"/>`;
    html += `<rect x="${chartWidth - 170}" y="25" width="15" height="15" fill="#667eea" opacity="0.8"/>`;
    html += `<text x="${chartWidth - 150}" y="37" font-size="12">Algoritma 1</text>`;
    html += `<rect x="${chartWidth - 170}" y="50" width="15" height="15" fill="#764ba2" opacity="0.8"/>`;
    html += `<text x="${chartWidth - 150}" y="62" font-size="12">Algoritma 2</text>`;
    
    html += `</svg></div>`;
    
    return html;
}



// Load home page on startup
window.addEventListener('DOMContentLoaded', function() {
    document.getElementById('content').innerHTML = `
        <section class="hero">
            <h2>Selamat Datang</h2>
            <p>Platform analisis data penjualan usaha Bebek Bakar 2024</p>
            <div class="hero-buttons">
                <button class="btn btn-primary" onclick="loadPendapatan()">💰 Pendapatan</button>
                <button class="btn btn-secondary" onclick="loadMenu()">🍗 Menu Terlaris</button>
            </div>
            <br><br>
            <div class="hero-buttons">
                <button class="btn btn-primary" onclick="loadHomogen()">📊 Relasi Homogen</button>
                <button class="btn btn-secondary" onclick="loadNonhomogen()">📈 Relasi Non-Homogen</button>
            </div>
            <br><br>
            <div class="hero-buttons">
                <button class="btn btn-primary" onclick="loadPerformance()">⚡ Analisis Performa</button>
            </div>
        </section>
    `;
});
