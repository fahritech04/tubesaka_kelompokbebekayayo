// Helper: Render top list items
function renderTopList(items, displayKey, valueKey, valueFormat = 'text') {
    return items.map((item, idx) => {
        let value = item[valueKey];
        if (valueFormat === 'rupiah') value = `Rp ${value.toLocaleString('id-ID')}`;
        else if (valueFormat === 'porsi') value = `${value.toLocaleString('id-ID')} porsi`;
        return `<div class="top-item">
            <span class="top-item-rank">#${idx + 1}</span>
            <span class="top-item-name">${item[displayKey]}</span>
            <span class="top-item-value">${value}</span>
        </div>`;
    }).join('');
}

// Helper: Render stat cards
function renderStatCards(stats) {
    const colors = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
    ];
    
    return stats.map((stat, idx) => `<div class="stat-card" style="background: ${colors[idx % 4]};">
        <h4>${stat.label}</h4>
        <div class="stat-value">${stat.value}</div>
    </div>`).join('');
}

// Generic load function
function loadData(endpoint, renderer) {
    showLoading();
    fetch(`/api/${endpoint}`)
        .then(r => r.json())
        .then(data => document.getElementById('content').innerHTML = renderer(data))
        .catch(err => document.getElementById('content').innerHTML = `<div class="error">Error: ${err.message}</div>`);
}

function loadPendapatan() {
    loadData('pendapatan', data => {
        let html = '<div class="section-title">💰 Analisis Pendapatan Harian 2024</div>';
        html += '<h3>Top 10 Pendapatan Tertinggi</h3>';
        html += `<div class="top-list">${renderTopList(data.top10, 'tanggal', 'pendapatan', 'rupiah')}</div>`;
        
        html += '<h3>Perbandingan Algoritma</h3><div class="algorithm-results">';
        html += `<div class="algo-card"><h3>🔄 Iteratif</h3><p>Tanggal: <strong>${data.iteratif.tanggal}</strong></p>
            <div class="value">Rp ${data.iteratif.pendapatan.toLocaleString('id-ID')}</div>
            <div class="time">Waktu: ${data.iteratif.waktu} detik</div></div>`;
        html += `<div class="algo-card"><h3>🌳 Rekursif (D&C)</h3><p>Tanggal: <strong>${data.rekursif.tanggal}</strong></p>
            <div class="value">Rp ${data.rekursif.pendapatan.toLocaleString('id-ID')}</div>
            <div class="time">Waktu: ${data.rekursif.waktu} detik</div></div></div>`;
        
        html += '<h3>Statistik Pendapatan</h3><div class="statistik">';
        html += renderStatCards([
            {label: 'Total Hari', value: data.statistik.total_hari},
            {label: 'Total Pendapatan', value: `Rp ${(data.statistik.total_pendapatan / 1000000).toFixed(1)}M`},
            {label: 'Rata-rata Harian', value: `Rp ${data.statistik.rata_rata.toLocaleString('id-ID')}`},
            {label: 'Selisih', value: `Rp ${(data.statistik.tertinggi - data.statistik.terendah).toLocaleString('id-ID')}`}
        ]);
        html += '</div>';
        
        return html;
    });
}

function loadMenu() {
    loadData('menu', data => {
        let html = '<div class="section-title">🍗 Menu Terlaris Tahun 2024</div>';
        html += '<h3>Top 10 Menu Terlaris</h3>';
        html += `<div class="top-list">${renderTopList(data.top10, 'nama', 'jumlah', 'porsi')}</div>`;
        
        html += '<h3>Perbandingan Algoritma</h3><div class="algorithm-results">';
        html += `<div class="algo-card"><h3>🔄 Iteratif</h3><p>Menu: <strong>${data.iteratif.nama}</strong></p>
            <div class="value">${data.iteratif.jumlah.toLocaleString('id-ID')} porsi</div>
            <div class="time">Waktu: ${data.iteratif.waktu} detik</div></div>`;
        html += `<div class="algo-card"><h3>🌳 Rekursif (D&C)</h3><p>Menu: <strong>${data.rekursif.nama}</strong></p>
            <div class="value">${data.rekursif.jumlah.toLocaleString('id-ID')} porsi</div>
            <div class="time">Waktu: ${data.rekursif.waktu} detik</div></div></div>`;
        
        html += '<h3>Statistik Penjualan</h3><div class="statistik">';
        html += renderStatCards([
            {label: 'Total Menu', value: data.total_menu},
            {label: 'Total Penjualan', value: data.total_penjualan.toLocaleString('id-ID')},
            {label: 'Rata-rata per Menu', value: Math.round(data.total_penjualan / data.total_menu).toLocaleString('id-ID')}
        ]);
        html += '</div>';
        
        return html;
    });
}

function loadHomogen() {
    loadData('relasi-homogen', data => {
        let html = '<div class="section-title">📊 Relasi Rekurensi Linier Homogen</div>';
        html += '<p style="color: #666; margin-bottom: 2rem;">T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3)</p>';
        
        data.forEach((p, idx) => {
            html += `<div style="margin-bottom: 3rem; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
                <h3 style="color: #667eea;">Produk ${idx + 1}: ${p.produk}</h3>
                <div style="background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <p><strong>Koefisien:</strong> a=${p.koef[0]}, b=${p.koef[1]}, c=${p.koef[2]}</p>
                    <p><strong>∑Koef:</strong> ${p.sum_koef} | <strong>Data Awal:</strong> ${p.data_awal.join(', ')}</p>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <h4>Prediksi Bulan ke-12</h4>
                    <p>Iteratif: <strong>${p.prediksi.iteratif}</strong> | Matrix: <strong>${p.prediksi.matrix}</strong> | Closed: <strong>${p.prediksi.closed}</strong></p>
                </div>
                <div style="background: #fff3cd; padding: 1rem; border-radius: 5px;">
                    <p><strong>Rata-rata Error:</strong> ${p.rata_rata_error}</p>
                </div>
            </div>`;
        });
        
        return html;
    });
}

function loadNonhomogen() {
    loadData('relasi-nonhomogen', data => {
        let html = '<div class="section-title">📈 Relasi Rekurensi Non-Homogen</div>';
        html += '<p style="color: #666; margin-bottom: 2rem;">T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3) + f(n)</p>';
        
        data.forEach((p, idx) => {
            html += `<div style="margin-bottom: 3rem; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
                <h3 style="color: #667eea;">Produk ${idx + 1}: ${p.produk}</h3>
                <div style="background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <p><strong>Koef:</strong> a=${p.koef[0]}, b=${p.koef[1]}, c=${p.koef[2]} (∑=${p.sum_koef})</p>
                    <p><strong>Data:</strong> ${p.data_awal.join(', ')} | <strong>f(n):</strong> ${p.f_n.join(', ')}</p>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                    <p>Bulan 6: <strong>${p.prediksi.bulan_6}</strong> | Bulan 12: <strong>${p.prediksi.bulan_12}</strong></p>
                </div>
                <div style="background: #fff3cd; padding: 1rem; border-radius: 5px;">
                    <p><strong>Error:</strong> ${p.rata_rata_error} | <strong>Status:</strong> ${p.status}</p>
                </div>
            </div>`;
        });
        
        return html;
    });
}

function showLoading() {
    document.getElementById('content').innerHTML = '<div class="loading"><div class="spinner"></div><p>Memuat data...</p></div>';
}

function goHome() {
    document.getElementById('content').innerHTML = `
        <section class="hero">
            <h2>Selamat Datang</h2>
            <p>Platform analisis data penjualan usaha Bebek Bakar 2024</p>
            <div class="hero-buttons">
                <button class="btn btn-primary" onclick="loadPendapatan()">Pendapatan</button>
                <button class="btn btn-secondary" onclick="loadMenu()">Menu Terlaris</button>
            </div>
            <br><br>
            <div class="hero-buttons">
                <button class="btn btn-primary" onclick="loadHomogen()">Relasi Homogen</button>
                <button class="btn btn-secondary" onclick="loadNonhomogen()">Non-Homogen</button>
            </div>
            <br><br>
            <div class="hero-buttons">
                <button class="btn btn-primary" onclick="loadPerformance()">Analisis Performa</button>
            </div>
        </section>
    `;
}

function loadPerformance() {
    let html = '<div class="section-title">⚡ Analisis Performa Algoritma</div>';
    html += `<div class="performance-form">
        <div class="form-group">
            <label>Masukkan Nilai N (Ukuran Data Maksimal):</label>
            <input type="number" id="input-n" value="100000" min="1" max="10000000">
            <span class="helper-text">Minimal 1, Maksimal 10,000,000</span>
        </div>
        <button class="btn btn-primary" onclick="runPerformanceAnalysis()">🚀 Generate & Analisis</button>
    </div><div id="performance-results"></div>`;
    document.getElementById('content').innerHTML = html;
}

function runPerformanceAnalysis() {
    const n = parseInt(document.getElementById('input-n').value);
    if (!n || n < 1) return alert('Masukkan nilai N yang valid (minimal 1)');
    
    document.getElementById('performance-results').innerHTML = '<div class="loading"><div class="spinner"></div><p>Menganalisis dengan N = ' + n.toLocaleString('id-ID') + '...</p></div>';
    
    fetch('/api/performance-analysis', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({n})})
        .then(r => r.json())
        .then(displayPerformanceResults)
        .catch(err => document.getElementById('performance-results').innerHTML = `<div class="error">Error: ${err.message}</div>`);
}

function displayPerformanceResults(data) {
    let html = '<h3>Hasil Analisis Performa</h3>';
    
    html += renderPerfSection('📊 Pencarian Pendapatan', data, 'pendapatan', 'Iteratif', 'Rekursif (D&C)');
    html += renderPerfSection('🍗 Pencarian Menu Terlaris', data, 'menu', 'Iteratif', 'Rekursif (D&C)');
    html += renderPerfSection('📈 Relasi Homogen', data, 'homogen', 'Iteratif', 'Matrix Exponentiation');
    
    html += '<div class="perf-section complexity"><h4>📐 Analisis Kompleksitas</h4><div class="complexity-info">';
    html += '<div class="complexity-item"><h5>O(n) - Iteratif</h5><p>Linear: Waktu bertambah proporsional dengan data</p></div>';
    html += '<div class="complexity-item"><h5>O(n) - Rekursif D&C</h5><p>Overhead rekursi lebih tinggi meski kompleksitas sama</p></div>';
    html += '<div class="complexity-item"><h5>O(log n) - Matrix</h5><p>Logaritmik: Efisien untuk nilai n besar</p></div>';
    html += '</div></div>';
    
    document.getElementById('performance-results').innerHTML = html;
}

function renderPerfSection(title, data, type, label1, label2) {
    const typeMap = {
        'pendapatan': ['iteratif_pendapatan', 'rekursif_pendapatan'],
        'menu': ['iteratif_menu', 'rekursif_menu'],
        'homogen': ['iteratif_homogen', 'matrix_homogen']
    };
    const [key1, key2] = typeMap[type];
    
    let html = `<div class="perf-section"><h4>${title}</h4>`;
    html += createPerformanceChart(data.sizes, data[key1], data[key2], label1, label2);
    html += '<div class="perf-table"><table class="data-table"><thead><tr><th>Ukuran</th><th>' + label1 + ' (ms)</th><th>' + label2 + ' (ms)</th><th>Selisih</th></tr></thead><tbody>';
    
    for (let i = 0; i < data.sizes.length; i++) {
        const v1 = data[key1][i], v2 = data[key2][i];
        const diff = ((v2 - v1) / v1 * 100).toFixed(2);
        html += `<tr><td>${data.sizes[i].toLocaleString('id-ID')}</td><td>${v1.toFixed(6)}</td><td>${v2.toFixed(6)}</td><td>${diff}%</td></tr>`;
    }
    
    return html + '</tbody></table></div></div>';
}

function createPerformanceChart(sizes, data1, data2, label1, label2) {
    const maxVal = Math.max(...data1, ...data2);
    const h = 300, w = Math.max(sizes.length * 80, 600);
    let svg = `<div class="perf-chart-container" style="overflow-x: auto;">
        <svg viewBox="0 0 ${w} ${h + 50}" width="100%" height="400" style="background: #f8f9fa; border-radius: 5px;">`;
    
    // Axes
    svg += `<line x1="50" y1="${h}" x2="${w-20}" y2="${h}" stroke="#999" stroke-width="2"/>
            <line x1="50" y1="10" x2="50" y2="${h}" stroke="#999" stroke-width="2"/>`;
    
    // Grid
    for (let i = 0; i <= 5; i++) {
        const y = h - (i * h / 5);
        svg += `<line x1="45" y1="${y}" x2="${w-20}" y2="${y}" stroke="#e0e0e0" stroke-width="1" stroke-dasharray="5,5"/>
                <text x="10" y="${y+4}" font-size="12" text-anchor="end">${(maxVal/5*i).toFixed(2)}</text>`;
    }
    
    // Bars
    const bw = (w - 70) / (sizes.length * 2.5), sp = (w - 70) / sizes.length;
    for (let i = 0; i < sizes.length; i++) {
        const x = 50 + i * sp + sp / 2, h1 = (data1[i] / maxVal) * h, h2 = (data2[i] / maxVal) * h;
        svg += `<rect x="${x - bw * 1.2}" y="${h - h1}" width="${bw}" height="${h1}" fill="#667eea" opacity="0.8"/>
                <rect x="${x - bw * 0.2}" y="${h - h2}" width="${bw}" height="${h2}" fill="#764ba2" opacity="0.8"/>
                <text x="${x}" y="${h + 20}" font-size="11" text-anchor="middle" fill="#333">${sizes[i]}</text>`;
    }
    
    // Legend
    svg += `<rect x="${w-220}" y="15" width="200" height="60" fill="white" stroke="#ccc" stroke-width="1" rx="3"/>
            <rect x="${w-210}" y="25" width="15" height="15" fill="#667eea" opacity="0.8"/>
            <text x="${w-190}" y="37" font-size="12">${label1}</text>
            <rect x="${w-210}" y="50" width="15" height="15" fill="#764ba2" opacity="0.8"/>
            <text x="${w-190}" y="62" font-size="12">${label2}</text>
            </svg></div>`;
    
    return svg;
}

window.addEventListener('DOMContentLoaded', goHome);
