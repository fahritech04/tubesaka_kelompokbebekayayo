// Configuration
const CONFIG = {
  colors: ["linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)", "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"],
  chartColors: { primary: "#667eea", secondary: "#764ba2" },
  styles: {
    produkCard: "margin-bottom: 3rem; padding: 1.5rem; background: #f8f9fa; border-radius: 10px;",
    produkTitle: "color: #667eea;",
    infoBox: "background: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;",
    warningBox: "background: #fff3cd; padding: 1rem; border-radius: 5px;",
    subtitle: "color: #666; margin-bottom: 2rem;",
  },
};

// Helpers
const fmt = {
  id: (n) => n.toLocaleString("id-ID"),
  rupiah: (n) => `Rp ${fmt.id(n)}`,
  porsi: (n) => `${fmt.id(n)} porsi`,
};

const DOM = {
  content: () => document.getElementById("content"),
  setContent: (html) => (DOM.content().innerHTML = html),
  setResults: (html) => (document.getElementById("performance-results").innerHTML = html),
};

// HTML Builders
const HTML = {
  section: (title, subtitle = "") => `<div class="section-title">${title}</div>${subtitle ? `<p style="${CONFIG.styles.subtitle}">${subtitle}</p>` : ""}`,
  infoBox: (content) => `<div style="${CONFIG.styles.infoBox}">${content}</div>`,
  warningBox: (content) => `<div style="${CONFIG.styles.warningBox}">${content}</div>`,
  produkCard: (idx, title, content) => `<div style="${CONFIG.styles.produkCard}"><h3 style="${CONFIG.styles.produkTitle}">Produk ${idx + 1}: ${title}</h3>${content}</div>`,
  koefInfo: (koef, sumKoef, dataAwal) => `<p><strong>Koefisien:</strong> a=${koef[0]}, b=${koef[1]}, c=${koef[2]}</p><p><strong>∑Koef:</strong> ${sumKoef} | <strong>Data Awal:</strong> ${dataAwal.join(", ")}</p>`,
};

function renderTopList(items, displayKey, valueKey, valueFormat = "text") {
  return items
    .map(
      (item, idx) => `<div class="top-item">
        <span class="top-item-rank">#${idx + 1}</span>
        <span class="top-item-name">${item[displayKey]}</span>
        <span class="top-item-value">${fmt[valueFormat] ? fmt[valueFormat](item[valueKey]) : item[valueKey]}</span>
    </div>`
    )
    .join("");
}

function renderStatCards(stats) {
  return stats.map((stat, idx) => `<div class="stat-card" style="background: ${CONFIG.colors[idx % 4]};"><h4>${stat.label}</h4><div class="stat-value">${stat.value}</div></div>`).join("");
}

function renderAlgoComparison(data, label, valueKey, valueFormat) {
  return `<h3>Perbandingan Algoritma</h3><div class="algorithm-results">
    <div class="algo-card"><h3>Iteratif</h3><p>${label}: <strong>${data.iteratif[label.toLowerCase()]}</strong></p>
        <div class="value">${fmt[valueFormat](data.iteratif[valueKey])}</div>
        <div class="time">Waktu: ${data.iteratif.waktu} detik</div></div>
    <div class="algo-card"><h3>Rekursif (D&C)</h3><p>${label}: <strong>${data.rekursif[label.toLowerCase()]}</strong></p>
        <div class="value">${fmt[valueFormat](data.rekursif[valueKey])}</div>
        <div class="time">Waktu: ${data.rekursif.waktu} detik</div></div></div>`;
}

function loadData(endpoint, renderer) {
  showLoading();
  fetch(`/api/${endpoint}`)
    .then((r) => r.json())
    .then((data) => DOM.setContent(renderer(data)))
    .catch((err) => DOM.setContent(`<div class="error">Error: ${err.message}</div>`));
}

function loadPendapatan() {
  loadData("pendapatan", (data) => {
    const s = data.statistik;
    return `${HTML.section("Analisis Pendapatan Harian 2024")}
      <h3>Top 10 Pendapatan Tertinggi</h3>
      <div class="top-list">${renderTopList(data.top10, "tanggal", "pendapatan", "rupiah")}</div>
      ${renderAlgoComparison(data, "Tanggal", "pendapatan", "rupiah")}
      <h3>Statistik Pendapatan</h3><div class="statistik">${renderStatCards([
        { label: "Total Hari", value: s.total_hari },
        { label: "Total Pendapatan", value: fmt.rupiah(s.total_pendapatan) },
        { label: "Rata-rata Harian", value: fmt.rupiah(s.rata_rata) },
      ])}</div>`;
  });
}

function loadMenu() {
  loadData("menu", (data) => {
    return `${HTML.section("Menu Terlaris Tahun 2024")}
      <h3>Top 10 Menu Terlaris</h3>
      <div class="top-list">${renderTopList(data.top10, "nama", "jumlah", "porsi")}</div>
      ${renderAlgoComparison(data, "Menu", "jumlah", "porsi")}
      <h3>Statistik Penjualan</h3><div class="statistik">${renderStatCards([
        { label: "Total Menu", value: data.total_menu },
        { label: "Total Penjualan", value: fmt.id(data.total_penjualan) },
        { label: "Rata-rata per Menu", value: fmt.id(Math.round(data.total_penjualan / data.total_menu)) },
      ])}</div>`;
  });
}

function renderRelasiProduk(data, isHomogen) {
  return data
    .map((p, idx) => {
      const info = isHomogen
        ? HTML.infoBox(HTML.koefInfo(p.koef, p.sum_koef, p.data_awal))
        : HTML.infoBox(`<p><strong>Koef:</strong> a=${p.koef[0]}, b=${p.koef[1]}, c=${p.koef[2]} (∑=${p.sum_koef})</p><p><strong>Data:</strong> ${p.data_awal.join(", ")} | <strong>f(n):</strong> ${p.f_n.join(", ")}</p>`);

      const prediksi = isHomogen
        ? HTML.infoBox(`<h4>Prediksi Bulan ke-12</h4><p>Iteratif: <strong>${p.prediksi.iteratif}</strong> | Matrix: <strong>${p.prediksi.matrix}</strong> | Closed: <strong>${p.prediksi.closed}</strong></p>`)
        : HTML.infoBox(`<p>Bulan 6: <strong>${p.prediksi.bulan_6}</strong> | Bulan 12: <strong>${p.prediksi.bulan_12}</strong></p>`);

      const error = isHomogen ? HTML.warningBox(`<p><strong>Rata-rata Error:</strong> ${p.rata_rata_error}</p>`) : HTML.warningBox(`<p><strong>Error:</strong> ${p.rata_rata_error} | <strong>Status:</strong> ${p.status}</p>`);

      return HTML.produkCard(idx, p.produk, info + prediksi + error);
    })
    .join("");
}

function loadHomogen() {
  loadData("relasi-homogen", (data) => `${HTML.section("Relasi Rekurensi Linier Homogen", "T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3)")}${renderRelasiProduk(data, true)}`);
}

function loadNonhomogen() {
  loadData("relasi-nonhomogen", (data) => `${HTML.section("Relasi Rekurensi Non-Homogen", "T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3) + f(n)")}${renderRelasiProduk(data, false)}`);
}

function showLoading() {
  DOM.setContent('<div class="loading"><div class="spinner"></div><p>Memuat data...</p></div>');
}

function goHome() {
  const buttons = [
    ["loadPendapatan()", "Pendapatan", "primary"],
    ["loadMenu()", "Menu Terlaris", "secondary"],
    ["loadHomogen()", "Relasi Homogen", "primary"],
    ["loadNonhomogen()", "Non-Homogen", "secondary"],
    ["loadPerformance()", "Analisis Performa", "primary"],
  ];
  const btnGroups = [buttons.slice(0, 2), buttons.slice(2, 4), buttons.slice(4)].map((group) => `<div class="hero-buttons">${group.map(([fn, txt, cls]) => `<button class="btn btn-${cls}" onclick="${fn}">${txt}</button>`).join("")}</div>`).join("<br><br>");
  DOM.setContent(`<section class="hero"><h2>Selamat Datang</h2>
    <p>Platform analisis data penjualan usaha Bebek Bakar 2024</p>${btnGroups}</section>`);
}

function loadPerformance() {
  DOM.setContent(`${HTML.section("Analisis Performa Algoritma")}
    <div class="performance-form">
        <div class="form-group">
            <label>Masukkan Nilai N (Ukuran Data Maksimal):</label>
            <input type="number" id="input-n" value="100000" min="1" max="10000000">
            <span class="helper-text">Minimal 1, Maksimal 10,000,000</span>
        </div>
        <button class="btn btn-primary" onclick="runPerformanceAnalysis()">Generate & Analisis</button>
    </div><div id="performance-results"></div>`);
}

function runPerformanceAnalysis() {
  const n = parseInt(document.getElementById("input-n").value);
  if (!n || n < 1) return alert("Masukkan nilai N yang valid (minimal 1)");

  DOM.setResults(`<div class="loading"><div class="spinner"></div><p>Menganalisis dengan N = ${fmt.id(n)}...</p></div>`);

  fetch("/api/performance-analysis", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ n }) })
    .then((r) => r.json())
    .then(displayPerformanceResults)
    .catch((err) => DOM.setResults(`<div class="error">Error: ${err.message}</div>`));
}

function displayPerformanceResults(data) {
  const sections = [
    ["Pencarian Pendapatan", "pendapatan", "Iteratif", "Rekursif (D&C)"],
    ["Pencarian Menu Terlaris", "menu", "Iteratif", "Rekursif (D&C)"],
    ["Relasi Homogen", "homogen", "Iteratif", "Matrix Exponentiation"],
  ];
  const complexityInfo = [
    ["O(n) - Iteratif", "Linear: Waktu bertambah proporsional dengan data"],
    ["O(n) - Rekursif D&C", "Overhead rekursi lebih tinggi meski kompleksitas sama"],
    ["O(log n) - Matrix", "Logaritmik: Efisien untuk nilai n besar"],
  ];

  let html = "<h3>Hasil Analisis Performa</h3>";
  html += sections.map(([title, type, l1, l2]) => renderPerfSection(title, data, type, l1, l2)).join("");
  html += `<div class="perf-section complexity"><h4>Analisis Kompleksitas</h4><div class="complexity-info">${complexityInfo.map(([h, p]) => `<div class="complexity-item"><h5>${h}</h5><p>${p}</p></div>`).join("")}</div></div>`;
  DOM.setResults(html);
}

function renderPerfSection(title, data, type, label1, label2) {
  const typeMap = { pendapatan: ["iteratif_pendapatan", "rekursif_pendapatan"], menu: ["iteratif_menu", "rekursif_menu"], homogen: ["iteratif_homogen", "matrix_homogen"] };
  const [key1, key2] = typeMap[type];
  const rows = data.sizes
    .map((s, i) => {
      const [v1, v2] = [data[key1][i], data[key2][i]];
      return `<tr><td>${fmt.id(s)}</td><td>${v1.toFixed(6)}</td><td>${v2.toFixed(6)}</td><td>${(((v2 - v1) / v1) * 100).toFixed(2)}%</td></tr>`;
    })
    .join("");

  return `<div class="perf-section"><h4>${title}</h4>${createPerformanceChart(data.sizes, data[key1], data[key2], label1, label2)}
    <div class="perf-table"><table class="data-table"><thead><tr><th>Ukuran</th><th>${label1} (ms)</th><th>${label2} (ms)</th><th>Selisih</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
}

// SVG Chart Components
const SVG = {
  line: (x1, y1, x2, y2, stroke = "#999", width = 2, dasharray = "") => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${width}"${dasharray ? ` stroke-dasharray="${dasharray}"` : ""}/>`,
  text: (x, y, content, size = 12, anchor = "middle", fill = "#333") => `<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="${fill}">${content}</text>`,
  rect: (x, y, w, h, fill, opacity = 1, stroke = "", rx = 0) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" opacity="${opacity}"${stroke ? ` stroke="${stroke}" stroke-width="1"` : ""}${rx ? ` rx="${rx}"` : ""}/>`,
  gridLine: (x1, y, x2, label) => `${SVG.line(x1, y, x2, y, "#e0e0e0", 1, "5,5")}${SVG.text(10, y + 4, label, 12, "end")}`,
};

function createPerformanceChart(sizes, data1, data2, label1, label2) {
  const maxVal = Math.max(...data1, ...data2);
  const [h, w] = [300, Math.max(sizes.length * 80, 600)];
  const { primary, secondary } = CONFIG.chartColors;

  // Y-axis grid and labels
  const gridLines = Array.from({ length: 6 }, (_, i) => SVG.gridLine(45, h - (i * h) / 5, w - 20, ((maxVal / 5) * i).toFixed(2))).join("");

  // Bars and labels
  const bw = (w - 70) / (sizes.length * 2.5);
  const sp = (w - 70) / sizes.length;
  const bars = sizes
    .map((s, i) => {
      const x = 50 + i * sp + sp / 2;
      const [h1, h2] = [(data1[i] / maxVal) * h, (data2[i] / maxVal) * h];
      return `${SVG.rect(x - bw * 1.2, h - h1, bw, h1, primary, 0.8)}${SVG.rect(x - bw * 0.2, h - h2, bw, h2, secondary, 0.8)}${SVG.text(x, h + 20, s, 11)}`;
    })
    .join("");

  // Legend
  const legend = `${SVG.rect(w - 220, 15, 200, 60, "white", 1, "#ccc", 3)}${SVG.rect(w - 210, 25, 15, 15, primary, 0.8)}${SVG.text(w - 190, 37, label1, 12, "start")}${SVG.rect(w - 210, 50, 15, 15, secondary, 0.8)}${SVG.text(w - 190, 62, label2, 12, "start")}`;

  return `<div class="perf-chart-container" style="overflow-x: auto;">
    <svg viewBox="0 0 ${w} ${h + 50}" width="100%" height="400" style="background: #f8f9fa; border-radius: 5px;">
      ${SVG.line(50, h, w - 20, h)}${SVG.line(50, 10, 50, h)}
      ${gridLines}${bars}${legend}
    </svg></div>`;
}

window.addEventListener("DOMContentLoaded", goHome);
