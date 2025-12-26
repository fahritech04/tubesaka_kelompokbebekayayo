// Configuration
const CONFIG = { colors: ["var(--gradient-1)", "var(--gradient-2)", "var(--gradient-3)", "var(--gradient-4)"], chartColors: { primary: "#667eea", secondary: "#764ba2" } };

// Helpers
const fmt = { id: (n) => n.toLocaleString("id-ID"), rupiah: (n) => `Rp ${fmt.id(n)}`, porsi: (n) => `${fmt.id(n)} porsi` };
const DOM = { content: () => document.getElementById("content"), setContent: (html) => (DOM.content().innerHTML = html), setResults: (html) => (document.getElementById("performance-results").innerHTML = html) };
const loading = (msg = "Memuat data...") => `<div class="loading"><div class="spinner"></div><p>${msg}</p></div>`;

// Helper: Generic test search function
function runTestSearch(inputId, endpoint, resultId, formatItem, unit) {
  const target = parseInt(document.getElementById(inputId).value);
  const resultDiv = document.getElementById(resultId);
  resultDiv.innerHTML = loading("Testing...");

  fetch(`/api/${endpoint}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ target }) })
    .then((r) => r.json())
    .then((data) => {
      if (!data.found) return (resultDiv.innerHTML = `<div class="test-result"><h4>❌ Tidak Ditemukan</h4><p>${data.message}</p><p>Total data dicari: ${fmt.id(data.total_data)} ${unit}</p></div>`);
      const winner = data.perbandingan.winner;
      const hasilList = data.iteratif.hasil.map((item) => `<li>${formatItem(item)}</li>`).join("");
      resultDiv.innerHTML = `<div class="test-result"><h4>✅ Ditemukan ${data.jumlah_hasil} data!</h4><p>Total data dicari: ${fmt.id(
        data.total_data
      )} ${unit}</p><div style="background: #f0f7ff; padding: 1rem; border-radius: 5px; margin: 1rem 0;"><h5>📋 Hasil (${
        data.jumlah_hasil
      } item):</h5><ul style="margin: 0.5rem 0; padding-left: 1.5rem;">${hasilList}</ul></div><div class="algo-comparison"><div class="algo-item ${winner === "Iteratif" ? "winner" : ""}"><h5>✨ Iteratif</h5><p>Ditemukan: <strong>${
        data.iteratif.hasil.length
      } data</strong></p><p>Waktu: <strong>${data.iteratif.waktu_str}</strong></p>${winner === "Iteratif" ? '<span class="badge-winner">WINNER</span>' : ""}</div><div class="algo-item ${
        winner === "Rekursif" ? "winner" : ""
      }"><h5>🔄 Rekursif D&C</h5><p>Ditemukan: <strong>${data.rekursif.hasil.length} data</strong></p><p>Waktu: <strong>${data.rekursif.waktu_str}</strong></p>${
        winner === "Rekursif" ? '<span class="badge-winner">WINNER</span>' : ""
      }</div></div><div class="conclusion"><p><strong>Kesimpulan:</strong> ${winner} lebih cepat <strong>${data.perbandingan.lebih_cepat}</strong></p><p>Selisih: ${data.perbandingan.selisih_persen.toFixed(2)}%</p></div></div>`;
    })
    .catch((err) => (resultDiv.innerHTML = `<div class="error">Error: ${err.message}</div>`));
}

// HTML Builders
const HTML = {
  section: (title, subtitle = "") => `<div class="section-title">${title}</div>${subtitle ? `<p class="section-subtitle">${subtitle}</p>` : ""}`,
  infoBox: (content) => `<div class="info-box">${content}</div>`,
  warningBox: (content) => `<div class="warning-box">${content}</div>`,
  produkCard: (idx, title, content) => `<div class="produk-card"><h3 class="produk-title">Produk ${idx + 1}: ${title}</h3>${content}</div>`,
  koefInfo: (koef, sumKoef, dataAwal) => `<p><strong>Koefisien:</strong> a=${koef[0]}, b=${koef[1]}, c=${koef[2]}</p><p><strong>∑Koef:</strong> ${sumKoef} | <strong>Data Awal:</strong> ${dataAwal.join(", ")}</p>`,
};

function renderTopList(items, displayKey, valueKey, valueFormat = "text") {
  return items
    .map(
      (item, idx) => `<div class="top-item"><span class="top-item-rank">#${idx + 1}</span><span class="top-item-name">${item[displayKey]}</span><span class="top-item-value">${fmt[valueFormat] ? fmt[valueFormat](item[valueKey]) : item[valueKey]}</span></div>`
    )
    .join("");
}
function renderStatCards(stats) {
  return stats.map((stat, idx) => `<div class="stat-card" style="background: ${CONFIG.colors[idx % 4]};"><h4>${stat.label}</h4><div class="stat-value">${stat.value}</div></div>`).join("");
}
function loadData(endpoint, renderer) {
  DOM.setContent(loading());
  fetch(`/api/${endpoint}`)
    .then((r) => r.json())
    .then((data) => DOM.setContent(renderer(data)))
    .catch((err) => DOM.setContent(`<div class="error">Error: ${err.message}</div>`));
}

function loadPendapatan() {
  loadData("pendapatan", (data) => {
    const s = data.statistik;
    return `${HTML.section(
      "Analisis Pendapatan Harian 2024"
    )}<div class="test-box"><h3>🧪 Test Perbandingan Algoritma</h3><div class="test-form"><label>Cari pendapatan dengan (Rp):</label><input type="number" id="test-pendapatan-target" value="1000000" min="1" step="100000"><button class="btn btn-primary" onclick="testPendapatan()">Test & Bandingkan</button></div><div id="test-pendapatan-result"></div></div><h3>Top 10 Pendapatan Tertinggi</h3><div class="top-list">${renderTopList(
      data.top10,
      "tanggal",
      "pendapatan",
      "rupiah"
    )}</div><h3>Statistik Pendapatan</h3><div class="statistik">${renderStatCards([
      { label: "Total Hari", value: s.total_hari },
      { label: "Total Pendapatan", value: fmt.rupiah(s.total_pendapatan) },
      { label: "Rata-rata Harian", value: fmt.rupiah(s.rata_rata) },
    ])}</div>`;
  });
}

function testPendapatan() {
  runTestSearch("test-pendapatan-target", "test-pendapatan", "test-pendapatan-result", (h) => `<strong>${h.tanggal}</strong> - ${fmt.rupiah(h.pendapatan)}`, "hari");
}

function loadMenu() {
  loadData(
    "menu",
    (data) =>
      `${HTML.section(
        "Menu Terlaris Tahun 2024"
      )}<div class="test-box"><h3>🧪 Test Perbandingan Algoritma</h3><div class="test-form"><label>Cari penjualan dengan (porsi):</label><input type="number" id="test-menu-target" value="100" min="1" step="10"><button class="btn btn-primary" onclick="testMenu()">Test & Bandingkan</button></div><div id="test-menu-result"></div></div><h3>Top 10 Menu Terlaris</h3><div class="top-list">${renderTopList(
        data.top10,
        "nama",
        "jumlah",
        "porsi"
      )}</div><h3>Statistik Penjualan</h3><div class="statistik">${renderStatCards([
        { label: "Total Menu", value: data.total_menu },
        { label: "Total Penjualan", value: fmt.id(data.total_penjualan) },
        { label: "Rata-rata per Menu", value: fmt.id(Math.round(data.total_penjualan / data.total_menu)) },
      ])}</div>`
  );
}

function testMenu() {
  runTestSearch("test-menu-target", "test-menu", "test-menu-result", (m) => `<strong>${m.nama}</strong> - ${fmt.porsi(m.jumlah)}`, "menu");
}

function renderRelasiProduk(data, isHomogen) {
  return data
    .map((p, idx) => {
      const info = isHomogen
        ? HTML.infoBox(HTML.koefInfo(p.koef, p.sum_koef, p.data_awal))
        : HTML.infoBox(`<p><strong>Koef:</strong> a=${p.koef[0]}, b=${p.koef[1]}, c=${p.koef[2]} (∑=${p.sum_koef})</p><p><strong>Data:</strong> ${p.data_awal.join(", ")} | <strong>f(n):</strong> ${p.f_n.join(", ")}</p>`);
      const prediksiId = `prediksi-${idx}`;
      const inputId = `n-produk-${idx}`;
      const labelId = `label-${idx}`;
      const prediksiContent = isHomogen
        ? `<h4 id="${labelId}">Prediksi (n=12)</h4><div id="${prediksiId}"><p>Iteratif: <strong>${p.prediksi.iteratif}</strong> | Matrix: <strong>${p.prediksi.matrix}</strong> | Closed: <strong>${p.prediksi.closed}</strong></p></div><div class="test-form" style="margin-top:0.5rem;"><input type="number" id="${inputId}" value="12" min="1" max="100000" style="width:100px;"><button class="btn btn-primary" style="padding:0.3rem 0.8rem;font-size:0.9rem;" onclick="updatePrediksi(${idx}, ${isHomogen})">Update n</button></div>`
        : `<h4 id="${labelId}">Prediksi (n=6 & n=12)</h4><div id="${prediksiId}"><p>Bulan 6: <strong>${p.prediksi.bulan_6}</strong> | Bulan 12: <strong>${p.prediksi.bulan_12}</strong></p></div><div class="test-form" style="margin-top:0.5rem;"><input type="number" id="${inputId}" value="12" min="1" max="10000" style="width:100px;"><button class="btn btn-primary" style="padding:0.3rem 0.8rem;font-size:0.9rem;" onclick="updatePrediksi(${idx}, ${isHomogen})">Update n</button></div>`;
      const prediksi = HTML.infoBox(prediksiContent);
      const error = isHomogen ? HTML.warningBox(`<p><strong>Rata-rata Error:</strong> ${p.rata_rata_error}</p>`) : HTML.warningBox(`<p><strong>Error:</strong> ${p.rata_rata_error} | <strong>Status:</strong> ${p.status}</p>`);
      return HTML.produkCard(idx, p.produk, info + prediksi + error);
    })
    .join("");
}

function loadHomogen() {
  loadData("relasi-homogen", (data) => {
    window.dataHomogen = data;
    return `${HTML.section("Relasi Rekurensi Linier Homogen", "T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3)")}${renderRelasiProduk(data, true)}`;
  });
}

function testHomogen() {
  const n = parseInt(document.getElementById("test-homogen-n").value);
  const resultDiv = document.getElementById("test-homogen-result");
  resultDiv.innerHTML = loading("Testing...");
  fetch("/api/test-relasi-homogen", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ n }) })
    .then((r) => r.json())
    .then((data) => {
      const winner = data.perbandingan.winner;
      resultDiv.innerHTML = `<div class="test-result"><h4>Hasil Test Prediksi Bulan ke-${data.n}</h4><p><strong>Nilai Awal:</strong> ${data.nilai_awal.join(", ")}</p><p><strong>Koefisien:</strong> a=${data.koefisien[0]}, b=${data.koefisien[1]}, c=${
        data.koefisien[2]
      }</p><div class="algo-comparison"><div class="algo-item ${winner === "Iteratif" ? "winner" : ""}"><h5>🔢 Iteratif</h5><p>Hasil: ${data.iteratif.hasil.toFixed(2)}</p><p>Waktu: <strong>${data.iteratif.waktu_str}</strong></p>${
        winner === "Iteratif" ? '<span class="badge-winner">WINNER</span>' : ""
      }</div><div class="algo-item ${winner === "Matrix" ? "winner" : ""}"><h5>⚡ Matrix Exp</h5><p>Hasil: ${data.matrix.hasil.toFixed(2)}</p><p>Waktu: <strong>${data.matrix.waktu_str}</strong></p>${
        winner === "Matrix" ? '<span class="badge-winner">WINNER</span>' : ""
      }</div><div class="algo-item ${winner === "Closed" ? "winner" : ""}><h5>✨ Closed Form</h5><p>Hasil: ${data.closed.hasil.toFixed(2)}</p><p>Waktu: <strong>${data.closed.waktu_str}</strong></p>${
        winner === "Closed" ? '<span class="badge-winner">WINNER</span>' : ""
      }</div></div><div class="conclusion"><p><strong>Kesimpulan:</strong> ${winner} adalah yang tercepat!</p><p>Iteratif vs Matrix: ${data.perbandingan.iteratif_vs_matrix}</p><p>Iteratif vs Closed: ${data.perbandingan.iteratif_vs_closed}</p></div></div>`;
    })
    .catch((err) => (resultDiv.innerHTML = `<div class="error">Error: ${err.message}</div>`));
}

function loadNonhomogen() {
  loadData("relasi-nonhomogen", (data) => {
    window.dataNonhomogen = data;
    return `${HTML.section("Relasi Rekurensi Non-Homogen", "T(n) = a·T(n-1) + b·T(n-2) + c·T(n-3) + f(n)")}${renderRelasiProduk(data, false)}`;
  });
}
function testNonhomogen() {
  const n = parseInt(document.getElementById("test-nonhomogen-n").value);
  const resultDiv = document.getElementById("test-nonhomogen-result");
  resultDiv.innerHTML = loading("Testing...");
  fetch("/api/test-relasi-nonhomogen", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ n }) })
    .then((r) => r.json())
    .then((data) => {
      resultDiv.innerHTML = `<div class="test-result"><h4>Hasil Test ${data.info}</h4><p><strong>Nilai Awal:</strong> ${data.nilai_awal.join(", ")}</p><p><strong>Koefisien:</strong> a=${data.koefisien[0]}, b=${data.koefisien[1]}, c=${
        data.koefisien[2]
      }</p><p><strong>Sample f(n):</strong> ${data.f_samples.map((v) => v.toFixed(1)).join(", ")}...</p><div class="algo-comparison"><div class="algo-item winner"><h5>🔢 Iteratif Non-Homogen</h5><p>Hasil Prediksi: <strong>${data.hasil.nilai.toFixed(
        2
      )}</strong></p><p>Waktu: <strong>${data.hasil.waktu_str}</strong></p><span class="badge-winner">✅ Dengan faktor eksternal</span></div></div></div>`;
    })
    .catch((err) => (resultDiv.innerHTML = `<div class="error">Error: ${err.message}</div>`));
}

// Fungsi DRY untuk update prediksi (Opsi 2: per produk)
function updatePrediksi(produkIdx, isHomogen) {
  const n = parseInt(document.getElementById(`n-produk-${produkIdx}`).value);
  const targetDiv = document.getElementById(`prediksi-${produkIdx}`);
  const labelDiv = document.getElementById(`label-${produkIdx}`);
  targetDiv.innerHTML = '<p style="color:#666;">⏳ Memuat...</p>';

  // Update label
  if (labelDiv) {
    labelDiv.textContent = isHomogen ? `Prediksi (n=${n})` : `Prediksi (n=${n})`;
  }

  const endpoint = isHomogen ? "/api/prediksi-produk-homogen" : "/api/prediksi-produk-nonhomogen";
  fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ produk_idx: produkIdx, n }) })
    .then((r) => r.json())
    .then((data) => {
      if (data.error) return (targetDiv.innerHTML = `<p style="color:red;">${data.error}</p>`);

      if (isHomogen) {
        const winner = data.perbandingan.winner;
        targetDiv.innerHTML = `
          <div class="algo-comparison" style="margin-top:0.5rem;">
            <div class="algo-item ${winner === "Iteratif" ? "winner" : ""}" style="padding:0.5rem;">
              <h5 style="font-size:0.9rem;margin:0 0 0.3rem 0;">🔢 Iteratif</h5>
              <p style="margin:0.2rem 0;font-size:0.85rem;">Hasil: <strong>${data.iteratif.hasil}</strong></p>
              <p style="margin:0.2rem 0;font-size:0.85rem;">Waktu: <strong>${data.iteratif.waktu_str}</strong></p>
              ${winner === "Iteratif" ? '<span class="badge-winner" style="font-size:0.75rem;">WINNER</span>' : ""}
            </div>
            <div class="algo-item ${winner === "Matrix" ? "winner" : ""}" style="padding:0.5rem;">
              <h5 style="font-size:0.9rem;margin:0 0 0.3rem 0;">⚡ Matrix Exp</h5>
              <p style="margin:0.2rem 0;font-size:0.85rem;">Hasil: <strong>${data.matrix.hasil}</strong></p>
              <p style="margin:0.2rem 0;font-size:0.85rem;">Waktu: <strong>${data.matrix.waktu_str}</strong></p>
              ${winner === "Matrix" ? '<span class="badge-winner" style="font-size:0.75rem;">WINNER</span>' : ""}
            </div>
            <div class="algo-item ${winner === "Closed" ? "winner" : ""}" style="padding:0.5rem;">
              <h5 style="font-size:0.9rem;margin:0 0 0.3rem 0;">✨ Closed Form</h5>
              <p style="margin:0.2rem 0;font-size:0.85rem;">Hasil: <strong>${data.closed.hasil}</strong></p>
              <p style="margin:0.2rem 0;font-size:0.85rem;">Waktu: <strong>${data.closed.waktu_str}</strong></p>
              ${winner === "Closed" ? '<span class="badge-winner" style="font-size:0.75rem;">WINNER</span>' : ""}
            </div>
          </div>
          <div class="conclusion" style="padding:0.5rem;margin-top:0.5rem;background:#f0f7ff;border-radius:5px;">
            <p style="margin:0.2rem 0;font-size:0.85rem;"><strong>Kesimpulan:</strong> ${winner} adalah yang tercepat!</p>
            <p style="margin:0.2rem 0;font-size:0.85rem;">Iteratif vs Matrix: ${data.perbandingan.iteratif_vs_matrix}</p>
            <p style="margin:0.2rem 0;font-size:0.85rem;">Iteratif vs Closed: ${data.perbandingan.iteratif_vs_closed}</p>
          </div>
        `;
      } else {
        targetDiv.innerHTML = `
          <div class="algo-comparison" style="margin-top:0.5rem;">
            <div class="algo-item winner" style="padding:0.5rem;">
              <h5 style="font-size:0.9rem;margin:0 0 0.3rem 0;">🔢 Iteratif Non-Homogen</h5>
              <p style="margin:0.2rem 0;font-size:0.85rem;">Hasil Prediksi: <strong>${data.hasil.nilai}</strong></p>
              <p style="margin:0.2rem 0;font-size:0.85rem;">Waktu: <strong>${data.hasil.waktu_str}</strong></p>
              <span class="badge-winner" style="font-size:0.75rem;">✅ Dengan faktor eksternal</span>
            </div>
          </div>
        `;
      }
    })
    .catch((err) => (targetDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`));
}

// Hapus fungsi updateSemuaProduk karena tidak digunakan lagi

function goHome() {
  const buttons = [
    ["loadPendapatan()", "Pendapatan", "primary"],
    ["loadMenu()", "Menu Terlaris", "secondary"],
    ["loadHomogen()", "Relasi Homogen", "primary"],
    ["loadNonhomogen()", "Non-Homogen", "secondary"],
    ["loadPerformance()", "Analisis Performa", "primary"],
  ];
  const btnGroups = [buttons.slice(0, 2), buttons.slice(2, 4), buttons.slice(4)].map((group) => `<div class="hero-buttons">${group.map(([fn, txt, cls]) => `<button class="btn btn-${cls}" onclick="${fn}">${txt}</button>`).join("")}</div>`).join("<br><br>");
  DOM.setContent(`<section class="hero"><h2>Selamat Datang</h2><p>Platform analisis data penjualan usaha Bebek Bakar 2024</p>${btnGroups}</section>`);
}
function loadPerformance() {
  DOM.setContent(
    `${HTML.section(
      "Analisis Performa Algoritma"
    )}<div class="performance-tabs"><button class="tab-btn active" onclick="showTab('quick')">Analisis Cepat</button><button class="tab-btn" onclick="showTab('demo')">Demo Perbandingan Detail</button></div><div id="tab-quick" class="tab-content active"><div class="performance-form"><div class="form-group"><label>Masukkan Nilai N (Ukuran Data Maksimal):</label><input type="number" id="input-n" value="100000" min="1" max="10000000"><span class="helper-text">Minimal 1, Maksimal 10,000,000</span></div><button class="btn btn-primary" onclick="runPerformanceAnalysis()">Generate & Analisis</button></div><div id="performance-results"></div></div><div id="tab-demo" class="tab-content"><button class="btn btn-primary" onclick="runDemoComparison()">Jalankan Demo Lengkap</button><div id="demo-results"></div></div>`
  );
}

function showTab(tabName) {
  document.querySelectorAll(".tab-btn").forEach((btn) => btn.classList.remove("active"));
  document.querySelectorAll(".tab-content").forEach((content) => content.classList.remove("active"));
  event.target.classList.add("active");
  document.getElementById(`tab-${tabName}`).classList.add("active");
}
function runDemoComparison() {
  const container = document.getElementById("demo-results");
  container.innerHTML = loading("Menjalankan demo perbandingan lengkap...");

  fetch("/api/demo-comparison")
    .then((r) => r.json())
    .then((data) => {
      const mkTable = (headers, rows) => `<div class="demo-table"><table class="data-table"><thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div>`;
      const mkConclusion = (items) => `<div class="conclusion-box"><h4>KESIMPULAN:</h4><ul>${items.map((c) => `<li>${c}</li>`).join("")}</ul></div>`;
      container.innerHTML = `<div class="demo-comparison-results"><div class="demo-section"><h3>DEMO 1: ${data.demo1.title}</h3>${mkTable(
        ["Size", "Iteratif (ms)", "Rekursif (ms)", "Overhead", "Winner"],
        data.demo1.results
          .map((r) => `<tr><td>${fmt.id(r.size)}</td><td>${r.iteratif.toFixed(4)}</td><td>${r.rekursif.toFixed(4)}</td><td>${r.overhead.toFixed(1)}%</td><td><strong>${r.winner === "Iteratif" ? "✅ Iteratif" : "❌ Rekursif"}</strong></td></tr>`)
          .join("")
      )}${mkConclusion(data.demo1.conclusion)}</div><div class="demo-section"><h3>DEMO 2: ${data.demo2.title}</h3>${mkTable(
        ["n", "Iteratif (ms)", "Matrix (ms)", "Closed (ms)", "Winner"],
        data.demo2.results
          .map((r) => {
            const winnerSymbol = r.winner === "Iteratif" ? "✅ Iteratif" : r.winner === "Matrix" ? "⭐ Matrix Exp" : "⭐⭐ Closed Form";
            return `<tr><td>${fmt.id(r.n)}</td><td>${r.iteratif.toFixed(4)}</td><td>${r.matrix.toFixed(4)}</td><td>${r.closed.toFixed(4)}</td><td><strong>${winnerSymbol}</strong></td></tr>`;
          })
          .join("")
      )}${mkConclusion(data.demo2.conclusion)}</div><div class="demo-section"><h3>DEMO 3: ${data.demo3.title}</h3><p class="demo-question"><strong>SKENARIO:</strong> Prediksi untuk n = [${data.demo3.results.queries.join(", ")}] (${
        data.demo3.results.queries.length
      } queries)</p>${mkTable(
        ["Algoritma", "Total Time (ms)", "Per Query (ms)", "Rank"],
        `<tr><td>Closed Form</td><td>${data.demo3.results.closed_total.toFixed(4)}</td><td>${data.demo3.results.closed_avg.toFixed(4)}</td><td><strong>#1</strong></td></tr><tr><td>Matrix Exp</td><td>${data.demo3.results.matrix_total.toFixed(
          4
        )}</td><td>${data.demo3.results.matrix_avg.toFixed(4)}</td><td><strong>#2</strong></td></tr><tr><td>Iteratif</td><td>${data.demo3.results.iteratif_total.toFixed(4)}</td><td>${data.demo3.results.iteratif_avg.toFixed(
          4
        )}</td><td><strong>#3</strong></td></tr>`
      )}${mkConclusion(data.demo3.conclusion)}</div></div>`;
    })
    .catch((err) => {
      container.innerHTML = `<div class="error">Error: ${err.message}</div>`;
    });
}
function runPerformanceAnalysis() {
  const n = parseInt(document.getElementById("input-n").value);
  if (!n || n < 1) return alert("Masukkan nilai N yang valid (minimal 1)");
  DOM.setResults(loading(`Menganalisis dengan N = ${fmt.id(n)}...`));
  fetch("/api/performance-analysis", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ n }) })
    .then((r) => r.json())
    .then(tampilHasilAnalisis)
    .catch((err) => DOM.setResults(`<div class="error">Error: ${err.message}</div>`));
}
function tampilHasilAnalisis(data) {
  const sections = [
    ["Pencarian Pendapatan", "pendapatan", "Iteratif", "Rekursif (D&C)"],
    ["Pencarian Menu Terlaris", "menu", "Iteratif", "Rekursif (D&C)"],
    ["Relasi Homogen", "homogen", "Iteratif", "Matrix Exponentiation"],
    ["Relasi Non-Homogen", "nonhomogen", "Iteratif Non-Homogen", "Baseline (Homogen)"],
  ];
  const complexityInfo = [
    ["O(n) - Iteratif", "Linear: Waktu bertambah proporsional dengan data"],
    ["O(n) - Rekursif D&C", "Overhead rekursi lebih tinggi meski kompleksitas sama"],
    ["O(log n) - Matrix", "Logaritmik: Efisien untuk nilai n besar"],
    ["O(n) - Non-Homogen", "Linear dengan faktor eksternal f(n)"],
  ];
  DOM.setResults(
    `<h3>Hasil Analisis Performa</h3><div class="perf-grid">${sections
      .map(([title, type, l1, l2]) => buatSectionAnalisis(title, data, type, l1, l2))
      .join("")}</div><div class="perf-section complexity"><h4>Analisis Kompleksitas</h4><div class="complexity-info">${complexityInfo.map(([h, p]) => `<div class="complexity-item"><h5>${h}</h5><p>${p}</p></div>`).join("")}</div></div>`
  );
}

function buatSectionAnalisis(title, data, type, label1, label2) {
  const typeMap = { pendapatan: ["iteratif_pendapatan", "rekursif_pendapatan"], menu: ["iteratif_menu", "rekursif_menu"], homogen: ["iteratif_homogen", "matrix_homogen"], nonhomogen: ["nonhomogen", "iteratif_homogen"] };
  const [key1, key2] = typeMap[type];
  if (!data[key1] || !data[key2] || !Array.isArray(data[key1]) || !Array.isArray(data[key2])) return `<div class="perf-section"><h4>${title}</h4><div class="error">⚠️ Data tidak tersedia</div></div>`;
  if (data[key1].length !== data.sizes.length || data[key2].length !== data.sizes.length) return `<div class="perf-section"><h4>${title}</h4><div class="error">⚠️ Data length mismatch</div></div>`;
  const validIndices = data.sizes.map((s, i) => ({ size: s, idx: i, v1: data[key1][i], v2: data[key2][i] })).filter((item) => item.v1 > 0.000001 && item.v2 > 0.000001);
  if (validIndices.length === 0) return `<div class="perf-section"><h4>${title}</h4><div class="warning-box">⚠️ Data tidak valid (N terlalu kecil)</div></div>`;
  const rows = validIndices
    .map((item) => {
      const [s, v1, v2] = [item.size, item.v1, item.v2];
      const selisih = v1 > 0 ? (((v2 - v1) / v1) * 100).toFixed(2) : "0.00";
      return `<tr><td>${fmt.id(s)}</td><td>${v1.toFixed(6)}</td><td>${v2.toFixed(6)}</td><td>${selisih}%</td></tr>`;
    })
    .join("");
  const chart = buatGrafikPerbandingan(
    validIndices.map((i) => i.size),
    validIndices.map((i) => i.v1),
    validIndices.map((i) => i.v2),
    label1,
    label2
  );
  return `<div class="perf-section"><h4>${title}</h4>${chart}<div class="perf-table"><table class="data-table"><thead><tr><th>Ukuran</th><th>${label1} (ms)</th><th>${label2} (ms)</th><th>Selisih</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
}
const SVG = {
  line: (x1, y1, x2, y2, stroke = "#999", width = 2, dasharray = "") => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${width}"${dasharray ? ` stroke-dasharray="${dasharray}"` : ""}/>`,
  text: (x, y, content, size = 12, anchor = "middle", fill = "#333") => `<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="${fill}">${content}</text>`,
  rect: (x, y, w, h, fill, opacity = 1, stroke = "", rx = 0) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" opacity="${opacity}"${stroke ? ` stroke="${stroke}" stroke-width="1"` : ""}${rx ? ` rx="${rx}"` : ""}/>`,
  gridLine: (x1, y, x2, label) => `${SVG.line(x1, y, x2, y, "#e0e0e0", 1, "5,5")}${SVG.text(10, y + 4, label, 12, "end")}`,
};
function buatGrafikPerbandingan(sizes, data1, data2, label1, label2) {
  if (!sizes || !data1 || !data2 || sizes.length === 0 || data1.length === 0 || data2.length === 0) return '<div class="error">⚠️ Data tidak valid</div>';
  const maxVal = Math.max(...data1, ...data2);
  if (maxVal === 0 || !isFinite(maxVal)) return '<div class="warning-box">⚠️ Data terlalu kecil</div>';
  const [h, w] = [300, Math.max(sizes.length * 80, 600)];
  const { primary, secondary } = CONFIG.chartColors;
  const gridLines = Array.from({ length: 6 }, (_, i) => SVG.gridLine(45, h - (i * h) / 5, w - 20, ((maxVal / 5) * i).toFixed(2))).join("");
  const bw = (w - 70) / (sizes.length * 2.5);
  const sp = (w - 70) / sizes.length;
  const bars = sizes
    .map((s, i) => {
      const x = 50 + i * sp + sp / 2;
      const [h1, h2] = [(data1[i] / maxVal) * h, (data2[i] / maxVal) * h];
      return `${SVG.rect(x - bw * 1.2, h - h1, bw, h1, primary, 0.8)}${SVG.rect(x - bw * 0.2, h - h2, bw, h2, secondary, 0.8)}${SVG.text(x, h + 20, s, 11)}`;
    })
    .join("");
  const legend = `${SVG.rect(w - 220, 15, 200, 60, "white", 1, "#ccc", 3)}${SVG.rect(w - 210, 25, 15, 15, primary, 0.8)}${SVG.text(w - 190, 37, label1, 12, "start")}${SVG.rect(w - 210, 50, 15, 15, secondary, 0.8)}${SVG.text(w - 190, 62, label2, 12, "start")}`;
  return `<div class="perf-chart-container" style="overflow-x: auto;"><svg viewBox="0 0 ${w} ${h + 50}" width="100%" height="400" style="background: #f8f9fa; border-radius: 5px;">${SVG.line(50, h, w - 20, h)}${SVG.line(
    50,
    10,
    50,
    h
  )}${gridLines}${bars}${legend}</svg></div>`;
}
window.addEventListener("DOMContentLoaded", goHome);
