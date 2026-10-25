from flask import Flask, request, jsonify, render_template_string
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Model untuk dua arah terjemahan
MODEL_MAP = {
    "en-id": "Helsinki-NLP/opus-mt-en-id",
    "id-en": "Helsinki-NLP/opus-mt-id-en"
}
models = {}

def get_translator(direction):
    if direction not in models:
        name = MODEL_MAP.get(direction, MODEL_MAP["en-id"])
        print(f"Memuat model {direction}: {name}...")
        tok = AutoTokenizer.from_pretrained(name)
        mod = AutoModelForSeq2SeqLM.from_pretrained(name)
        models[direction] = (tok, mod)
    return models[direction]

# Prapemuatan awal model Inggris -> Indonesia
get_translator("en-id")

HTML_PAGE = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>byprhmniTranslate Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #07090e;
      --card-bg: rgba(15, 20, 32, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #6366f1;
      --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --surface-dark: rgba(9, 12, 20, 0.9);
      --border-subtle: rgba(255, 255, 255, 0.05);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 100% 100%, rgba(6, 182, 212, 0.08) 0%, transparent 40%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    /* Navbar */
    header {
      backdrop-filter: blur(16px);
      background: rgba(7, 9, 14, 0.85);
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 40;
    }
    .nav-wrapper {
      max-width: 1100px;
      margin: 0 auto;
      padding: 0.85rem 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 0.65rem;
    }
    .brand-logo {
      width: 34px;
      height: 34px;
      border-radius: 10px;
      background: var(--primary-gradient);
      display: grid;
      place-items: center;
      flex-shrink: 0;
    }
    .brand-title {
      font-size: 1.1rem;
      font-weight: 800;
      letter-spacing: -0.02em;
    }
    .brand-title span {
      background: var(--primary-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .engine-pill {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      padding: 0.3rem 0.65rem;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 600;
      color: #34d399;
      white-space: nowrap;
    }
    .pulse-dot {
      width: 6px;
      height: 6px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      flex-shrink: 0;
    }

    /* Layout */
    main {
      flex: 1;
      max-width: 1100px;
      width: 100%;
      margin: 0 auto;
      padding: 1.5rem 1rem 3rem;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .hero-section {
      text-align: center;
      padding: 0 0.5rem;
    }
    .hero-section h1 {
      font-size: 2.1rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.25;
      background: linear-gradient(180deg, #ffffff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero-section p {
      color: var(--text-muted);
      font-size: 0.88rem;
      margin-top: 0.4rem;
      line-height: 1.5;
    }

    /* Translation Card */
    .studio-box {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      backdrop-filter: blur(20px);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .lang-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      padding: 0.75rem 1rem;
      background: var(--surface-dark);
      border-bottom: 1px solid var(--card-border);
    }
    .tag-bubble {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 0.35rem 0.65rem;
      border-radius: 8px;
      color: #e2e8f0;
      font-size: 0.78rem;
      font-weight: 600;
      white-space: nowrap;
      text-align: center;
      flex: 1;
      max-width: 140px;
    }
    .tag-bubble.active-target {
      border-color: rgba(99, 102, 241, 0.45);
      background: rgba(99, 102, 241, 0.15);
      color: #a5b4fc;
    }

    .btn-swap-lang {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      cursor: pointer;
      display: grid;
      place-items: center;
      flex-shrink: 0;
      transition: all 0.25s ease;
    }
    .btn-swap-lang:hover, .btn-swap-lang:active {
      background: rgba(99, 102, 241, 0.2);
      border-color: var(--primary);
      color: #fff;
      transform: rotate(180deg);
    }

    .dual-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
    }

    .editor-col {
      padding: 1.25rem 1rem;
      display: flex;
      flex-direction: column;
      min-height: 180px;
    }
    .editor-col:first-child {
      border-right: 1px solid var(--card-border);
    }
    .editor-col.output-bg {
      background: rgba(7, 10, 18, 0.4);
    }

    textarea {
      flex: 1;
      width: 100%;
      background: transparent;
      border: none;
      outline: none;
      resize: none;
      color: #fff;
      font-size: 1.05rem;
      line-height: 1.6;
      min-height: 140px;
      word-break: break-word;
    }
    textarea::placeholder {
      color: #475569;
    }

    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 0.85rem;
      border-top: 1px solid var(--border-subtle);
      margin-top: 0.75rem;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .tool-cluster {
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    .action-icon-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      width: 34px;
      height: 34px;
      border-radius: 8px;
      cursor: pointer;
      display: grid;
      place-items: center;
      transition: all 0.2s;
    }
    .action-icon-btn:hover, .action-icon-btn:active {
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
    }
    .counter-text {
      font-size: 0.75rem;
      color: var(--text-dim);
      font-family: 'JetBrains Mono', monospace;
      margin-left: 0.3rem;
      white-space: nowrap;
    }

    .right-tools {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .btn-submit {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      background: var(--primary-gradient);
      color: #fff;
      border: none;
      padding: 0.65rem 1.25rem;
      font-weight: 700;
      border-radius: 10px;
      cursor: pointer;
      font-size: 0.88rem;
      box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
      transition: all 0.2s;
      white-space: nowrap;
    }
    .btn-submit:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .shortcut-badge {
      font-size: 0.72rem;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    kbd {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 4px;
      padding: 0.1rem 0.3rem;
      font-size: 0.65rem;
      font-family: 'JetBrains Mono', monospace;
      color: #cbd5e1;
    }

    /* Fitur & Riwayat */
    .features-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1rem;
    }
    .feat-card {
      background: rgba(15, 20, 32, 0.45);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 1.1rem;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }
    .feat-card-header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 700;
      font-size: 0.88rem;
      color: #f1f5f9;
    }
    .feat-icon {
      width: 26px;
      height: 26px;
      border-radius: 7px;
      background: rgba(99, 102, 241, 0.15);
      display: grid;
      place-items: center;
      color: #818cf8;
      flex-shrink: 0;
    }
    .feat-card p {
      font-size: 0.8rem;
      color: var(--text-muted);
      line-height: 1.45;
    }

    .history-card {
      background: rgba(15, 20, 32, 0.45);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.25rem 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }
    .history-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .history-head h3 {
      font-size: 0.92rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .btn-clear-history {
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 0.78rem;
      cursor: pointer;
    }
    .history-list {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      max-height: 220px;
      overflow-y: auto;
    }
    .history-item {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
    }
    .history-texts {
      overflow: hidden;
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }
    .hist-src { font-size: 0.82rem; color: #cbd5e1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .hist-tgt { font-size: 0.78rem; color: #818cf8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    #toast {
      position: fixed;
      bottom: 1.5rem;
      left: 50%;
      transform: translateX(-50%) translateY(70px);
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(99, 102, 241, 0.4);
      color: #fff;
      padding: 0.6rem 1.25rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      opacity: 0;
      transition: all 0.3s;
      z-index: 100;
      white-space: nowrap;
    }
    #toast.show {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }

    /* Footer & Tombol Sosial */
    footer {
      border-top: 1px solid var(--border-subtle);
      padding: 1.5rem 1rem;
      color: var(--text-dim);
      font-size: 0.82rem;
    }
    .footer-wrap {
      max-width: 1100px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 1rem;
      flex-wrap: wrap;
      text-align: center;
    }
    .social-cluster {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .social-link-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      transition: all 0.25s ease;
      text-decoration: none;
    }
    .social-link-btn:hover {
      background: rgba(99, 102, 241, 0.2);
      border-color: var(--primary);
      color: #fff;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }

    @media (max-width: 768px) {
      .dual-grid { grid-template-columns: 1fr; }
      .editor-col:first-child { border-right: none; border-bottom: 1px solid var(--card-border); }
      .features-grid { grid-template-columns: 1fr; }
      .shortcut-badge { display: none; }
      .engine-pill span:last-child { display: none; }
      .engine-pill::after { content: "Offline"; }
      .hero-section h1 { font-size: 1.6rem; }
      .hero-section p { font-size: 0.82rem; }
      .btn-submit { flex: 1; }
      .right-tools { width: 100%; }
      .footer-wrap { flex-direction: column; gap: 0.65rem; }
    }
  </style>
</head>
<body>

  <header>
    <div class="nav-wrapper">
      <div class="brand-group">
        <div class="brand-logo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m5 8 6 6"/>
            <path d="m4 14 6-6 2-3"/>
            <path d="M2 5h12"/>
            <path d="M7 2h1"/>
            <path d="m22 22-5-10-5 10"/>
            <path d="M14 18h6"/>
          </svg>
        </div>
        <div class="brand-title">byprhmniTranslate <span>Studio</span></div>
      </div>

      <div class="engine-pill">
        <span class="pulse-dot"></span>
        <span>MarianMT &bull; 5-Beams Engine</span>
      </div>
    </div>
  </header>

  <main>
    <div class="hero-section">
      <h1>Translatebyprhmni</h1>
      <p>Penerjemahan dua arah Bahasa Inggris & Indonesia bertenaga Transformer lokal.</p>
    </div>

    <div class="studio-box">
      <div class="lang-bar">
        <span id="srcLabel" class="tag-bubble">English</span>
        <button class="btn-swap-lang" onclick="swapLanguages()" title="Tukar Posisi Bahasa">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m16 3 4 4-4 4"/>
            <path d="M20 7H4"/>
            <path d="m8 21-4-4 4-4"/>
            <path d="M4 17h16"/>
          </svg>
        </button>
        <span id="tgtLabel" class="tag-bubble active-target">Indonesia</span>
      </div>

      <div class="dual-grid">
        <!-- Panel Masukan -->
        <div class="editor-col">
          <textarea id="inputText" placeholder="Ketik teks di sini..." spellcheck="false"></textarea>
          
          <div class="card-footer">
            <div class="tool-cluster">
              <button class="action-icon-btn" onclick="pasteClipboard()" title="Tempel">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/></svg>
              </button>
              <button class="action-icon-btn" onclick="clearInput()" title="Bersihkan">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
              </button>
              <button class="action-icon-btn" onclick="speakText('input')" title="Dengarkan Suara">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
              </button>
              <span id="charCount" class="counter-text">0 huruf</span>
            </div>

            <div class="right-tools">
              <span class="shortcut-badge"><kbd>Ctrl</kbd> + <kbd>Enter</kbd></span>
              <button id="btnTranslate" class="btn-submit" onclick="translateText()">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                  <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
                </svg>
                <span id="btnLabel">Terjemahkan</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Panel Hasil -->
        <div class="editor-col output-bg">
          <textarea id="outputText" readonly placeholder="Hasil terjemahan akan tampil di sini..." spellcheck="false"></textarea>
          
          <div class="card-footer">
            <div class="tool-cluster">
              <button class="action-icon-btn" onclick="copyOutput()" title="Salin">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
              </button>
              <button class="action-icon-btn" onclick="speakText('output')" title="Dengarkan Suara">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
              </button>
              <button class="action-icon-btn" onclick="downloadTxt()" title="Unduh File">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              </button>
            </div>

            <span id="latencyTag" class="counter-text" style="color: #818cf8;">Siap</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Fitur -->
    <div class="features-grid">
      <div class="feat-card">
        <div class="feat-card-header">
          <div class="feat-icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
          <span>Privasi Mutlak & Offline</span>
        </div>
        <p>Inferensi diproses langsung di mesin lokal tanpa koneksi luar.</p>
      </div>
      <div class="feat-card">
        <div class="feat-card-header">
          <div class="feat-icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></div>
          <span>Beam Search 5-Beams</span>
        </div>
        <p>Mencari kemungkinan susunan kalimat terbaik agar tata bahasa lebih tertata.</p>
      </div>
      <div class="feat-card">
        <div class="feat-card-header">
          <div class="feat-icon"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m10 15 5-3-5-3v6z"/></svg></div>
          <span>Seq2Seq MarianMT</span>
        </div>
        <p>Dioptimalkan untuk efisiensi komputasi CPU laptop/desktop.</p>
      </div>
    </div>

    <!-- Riwayat -->
    <div class="history-card">
      <div class="history-head">
        <h3>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          Riwayat Terjemahan Sesi Ini
        </h3>
        <button class="btn-clear-history" onclick="clearHistory()">Hapus Riwayat</button>
      </div>
      <div id="historyList" class="history-list"></div>
    </div>
  </main>

  <div id="toast">Tersalin ke papan klip!</div>

  <!-- Footer dengan Akun Asli -->
  <footer>
    <div class="footer-wrap">
      <span>byprhmniTranslate Studio &bull; Proyek Repositori Mandiri</span>
      <div class="social-cluster">
        <!-- Akun GitHub prhmni -->
        <a href="https://github.com/prhmni" target="_blank" rel="noopener noreferrer" class="social-link-btn" title="Kunjungi Akun GitHub prhmni">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
          </svg>
        </a>

        <!-- Akun Instagram prhmni__ -->
        <a href="https://www.instagram.com/prhmni__?dlrf=MTM5d3lrMG40OWdncg%3D%3D&utm_source=qr" target="_blank" rel="noopener noreferrer" class="social-link-btn" title="Kunjungi Akun Instagram prhmni__">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="20" height="20" x="2" y="2" rx="5" ry="5"/>
            <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>
            <line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>
          </svg>
        </a>
      </div>
    </div>
  </footer>

  <script>
    let currentDir = "en-id";
    const inputEl = document.getElementById('inputText');
    const outputEl = document.getElementById('outputText');
    const srcLabel = document.getElementById('srcLabel');
    const tgtLabel = document.getElementById('tgtLabel');
    const charCount = document.getElementById('charCount');
    const latencyTag = document.getElementById('latencyTag');
    const btnTranslate = document.getElementById('btnTranslate');
    const btnLabel = document.getElementById('btnLabel');
    const historyList = document.getElementById('historyList');

    let historyData = JSON.parse(localStorage.getItem('byprhmni_history') || '[]');
    renderHistory();

    inputEl.addEventListener('input', () => {
      charCount.innerText = inputEl.value.length + ' huruf';
    });

    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') translateText();
    });

    function swapLanguages() {
      if (currentDir === "en-id") {
        currentDir = "id-en";
        srcLabel.innerText = "Indonesia";
        tgtLabel.innerText = "English";
      } else {
        currentDir = "en-id";
        srcLabel.innerText = "English";
        tgtLabel.innerText = "Indonesia";
      }

      const temp = inputEl.value;
      inputEl.value = outputEl.value;
      outputEl.value = temp;
      charCount.innerText = inputEl.value.length + ' huruf';
      showToast("Arah bahasa ditukar!");
    }

    function clearInput() {
      inputEl.value = '';
      outputEl.value = '';
      charCount.innerText = '0 huruf';
      latencyTag.innerText = 'Siap';
      inputEl.focus();
    }

    async function pasteClipboard() {
      try {
        const text = await navigator.clipboard.readText();
        inputEl.value = text;
        charCount.innerText = text.length + ' huruf';
        showToast("Teks ditempel!");
      } catch (err) {
        showToast("Gagal membaca papan klip.");
      }
    }

    async function translateText() {
      const text = inputEl.value.trim();
      if (!text) return;

      btnTranslate.disabled = true;
      btnLabel.innerText = "...";
      latencyTag.innerText = "Memproses...";

      const tStart = performance.now();
      try {
        const res = await fetch('/api/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: text, direction: currentDir })
        });
        const data = await res.json();
        outputEl.value = data.result || '';
        const dur = Math.round(performance.now() - tStart);
        latencyTag.innerText = `${dur} ms`;

        if (data.result) {
          addHistoryItem(text, data.result, currentDir);
        }
      } catch (err) {
        outputEl.value = "[Gagal memproses terjemahan]";
        latencyTag.innerText = "Terputus";
      } finally {
        btnTranslate.disabled = false;
        btnLabel.innerText = "Terjemahkan";
      }
    }

    function copyOutput() {
      if (!outputEl.value) return;
      navigator.clipboard.writeText(outputEl.value);
      showToast("Teks berhasil disalin!");
    }

    function downloadTxt() {
      if (!outputEl.value) return;
      const blob = new Blob([outputEl.value], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `terjemahan-${Date.now()}.txt`;
      a.click();
      URL.revokeObjectURL(url);
      showToast("File diunduh!");
    }

    function speakText(pane) {
      const text = pane === 'input' ? inputEl.value : outputEl.value;
      if (!text) return;
      const u = new SpeechSynthesisUtterance(text);
      if (pane === 'input') {
        u.lang = currentDir === 'en-id' ? 'en-US' : 'id-ID';
      } else {
        u.lang = currentDir === 'en-id' ? 'id-ID' : 'en-US';
      }
      window.speechSynthesis.speak(u);
    }

    function addHistoryItem(src, tgt, direction) {
      historyData.unshift({ src, tgt, direction, time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) });
      if (historyData.length > 6) historyData.pop();
      localStorage.setItem('byprhmni_history', JSON.stringify(historyData));
      renderHistory();
    }

    function renderHistory() {
      if (!historyData.length) {
        historyList.innerHTML = `<div style="text-align:center; padding: 1rem; color: #64748b; font-size: 0.8rem;">Belum ada riwayat terjemahan.</div>`;
        return;
      }
      historyList.innerHTML = historyData.map((item, idx) => `
        <div class="history-item" onclick="loadHistoryItem(${idx})">
          <div class="history-texts">
            <span class="hist-src">${escapeHtml(item.src)}</span>
            <span class="hist-tgt">${escapeHtml(item.tgt)}</span>
          </div>
          <span style="font-size: 0.7rem; color: #64748b;">${item.time}</span>
        </div>
      `).join('');
    }

    function loadHistoryItem(idx) {
      const item = historyData[idx];
      if (!item) return;
      inputEl.value = item.src;
      outputEl.value = item.tgt;
      charCount.innerText = item.src.length + ' huruf';
      showToast("Riwayat dimuat!");
    }

    function clearHistory() {
      historyData = [];
      localStorage.removeItem('byprhmni_history');
      renderHistory();
      showToast("Riwayat dibersihkan.");
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2000);
    }

    function escapeHtml(str) {
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/api/translate", methods=["POST"])
def translate_api():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    direction = data.get("direction", "en-id")
    if not text:
        return jsonify({"result": ""})
    
    tok, mod = get_translator(direction)
    inputs = tok(text, return_tensors="pt", padding=True)
    
    outputs = mod.generate(
        **inputs,
        num_beams=5,
        length_penalty=1.0,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    
    translated_text = tok.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"result": translated_text})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)