import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
from fpdf import FPDF  # type: ignore
import plotly.express as px  # type: ignore
from model_stunting import BayesianNetworkStunting

# =========================================
# KONFIGURASI HALAMAN
# =========================================
st.set_page_config(
    page_title="CareStunt - Sistem Pakar",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================
# FUNGSI PDF
# =========================================
def generate_pdf(nama, umur, hasil, risiko):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "LAPORAN SISTEM PAKAR RISIKO STUNTING", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Nama Balita : {nama}", ln=True)
    pdf.cell(0, 8, f"Umur        : {umur} Bulan", ln=True)
    pdf.cell(0, 8, f"Hasil Risiko: {risiko}", ln=True)
    pdf.ln(5)

    pdf.cell(0, 8, "Probabilitas Risiko:", ln=True)
    for k, v in hasil.items():
        pdf.cell(0, 8, f"- {k}: {v:.2f}%", ln=True)

    return pdf.output(dest="S").encode("latin-1")

# =========================================
# CUSTOM CSS (AMAN, TANPA RUSAK ICON)
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

/* Header bawaan streamlit */
header[data-testid="stHeader"] {
    background: #020617 !important;
    border-bottom: 1px solid #1e293b;
}

/* Background utama */
.stApp {
    background: #020617;
    color: #ffffff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 2px solid #1e40af;
}

/* Teks utama (JANGAN sentuh span agar icon aman) */
h1, h2, h3, h4, h5, h6, p, li, label {
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
}

/* Divider */
.custom-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #3b82f6, transparent);
    margin: 12px 0;
}

/* Header card */
.header-card {
    background: linear-gradient(135deg, #1e40af, #1e3a8a);
    padding: 2.5rem;
    border-radius: 24px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Glass card */
.glass {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 1.5rem;
}

/* Button */
div.stButton > button {
    background: #22c55e !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 12px;
    padding: 0.8rem 2rem;
    border: none;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# NAVIGATION STATE
# =========================================
if "page" not in st.session_state:
    st.session_state.page = "🏠 Beranda"

def nav_to(page):
    st.session_state.page = page
    st.rerun()

# =========================================
# SIDEBAR (PAKAI BAWAAN STREAMLIT)
# =========================================
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🩺 CareStunt</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:13px;'>Sistem Pakar Diagnosa Stunting</p>", unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        ["🏠 Beranda", "🔍 Diagnosa", "📘 Edukasi", "ℹ️ Tentang"],
        index=["🏠 Beranda", "🔍 Diagnosa", "📘 Edukasi", "ℹ️ Tentang"].index(st.session_state.page)
    )

    if menu != st.session_state.page:
        st.session_state.page = menu
        st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Model (rapat & rapi)
    st.markdown("""
    <div style="line-height:1.2;">
        <h4 style="margin-bottom:2px;">Model</h4>
        <p style="margin-top:2px; font-size:13px; opacity:0.85;">
            Algorithm Bayesian Network
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# HALAMAN: BERANDA
# =========================================
if st.session_state.page == "🏠 Beranda":
    st.markdown("""
    <div class="header-card">
        <h1>Sistem Pakar Risiko Stunting pada Balita</h1>
        <p style="font-size:1rem; opacity:0.9;">
        Analisis Risiko Stunting Menggunakan Metode Bayesian Network
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
    <h3>📌 Tujuan Sistem</h3>
    <p>
    Sistem ini merupakan <b>sistem pakar berbasis Bayesian Network</b>
    yang dirancang untuk membantu orang tua dan tenaga kesehatan
    dalam <b>menganalisis risiko stunting pada balita</b>
    secara probabilistik berdasarkan pengetahuan pakar.
    </p>

    <h4>Parameter yang Digunakan</h4>
    <ul>
        <li><b>Umur Balita</b>: rentang usia pertumbuhan kritis (0 - 36 bulan).</li>
        <li><b>Pola Makan</b>: kualitas asupan gizi harian.</li>
        <li><b>Riwayat Infeksi</b>: frekuensi penyakit yang pernah dialami.</li>
        <li><b>Sanitasi Lingkungan</b>: kondisi kebersihan dan sumber air.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.info("Sistem ini bersifat **pendukung keputusan**, bukan diagnosis medis.")

    if st.button("Mulai Diagnosa Sekarang"):
        nav_to("🔍 Diagnosa")

# =========================================
# HALAMAN: DIAGNOSA
# =========================================
elif st.session_state.page == "🔍 Diagnosa":
    st.markdown("# Analisis Risiko Stunting")

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.markdown('<div>', unsafe_allow_html=True)
        nama = st.text_input("Nama Balita")
        umur = st.number_input("Umur (Bulan)", 0, 60, 24)
        pola = st.selectbox("Pola Makan", ["Baik", "Cukup", "Kurang"])
        sakit = st.selectbox("Riwayat Infeksi", ["Tidak Ada", "Jarang", "Sering"])
        sanitasi = st.selectbox("Sanitasi Lingkungan", ["Baik", "Cukup", "Kurang"])
        btn = st.button("Hitung Risiko Stunting")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if btn:
            if not nama:
                st.error("Nama balita wajib diisi.")
            else:
                model = BayesianNetworkStunting()
                hasil, _ = model.inferensi(umur, pola, sakit, sanitasi)
                risiko = max(hasil, key=hasil.get)

                st.markdown(f"### Hasil Diagnosa: **{risiko}**")

                df = pd.DataFrame(hasil.items(), columns=["Risiko", "Persentase"])
                fig = px.bar(
                    df,
                    x="Risiko",
                    y="Persentase",
                    color="Risiko",
                    text_auto=".2f"
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white"
                )
                st.plotly_chart(fig, use_container_width=True)

                pdf = generate_pdf(nama, umur, hasil, risiko)
                st.download_button(
                    "📄 Unduh Laporan PDF",
                    pdf,
                    file_name=f"Laporan_{nama}.pdf"
                )

# =========================================
# HALAMAN: EDUKASI
# =========================================
elif st.session_state.page == "📘 Edukasi":
    st.markdown("## 📘 Edukasi Stunting")

    st.markdown("""
    <div class="glass">
    <h3>Apa itu Stunting?</h3>
    <p>
    <b>Stunting</b> adalah kondisi gagal tumbuh pada anak balita
    yang ditandai dengan tinggi badan lebih rendah dibandingkan
    standar usianya. Kondisi ini terjadi akibat kekurangan gizi
    kronis dalam jangka waktu lama serta paparan infeksi berulang.
    </p>

    <h3>Mengapa Stunting Berbahaya?</h3>
    <p>
    Stunting tidak hanya berdampak pada pertumbuhan fisik,
    tetapi juga memengaruhi perkembangan kognitif dan kesehatan
    anak dalam jangka panjang.
    </p>

    <ul>
        <li>Terhambatnya pertumbuhan fisik dan tinggi badan</li>
        <li>Perkembangan otak tidak optimal</li>
        <li>Daya tahan tubuh rendah dan mudah sakit</li>
        <li>Meningkatnya risiko penyakit kronis di masa dewasa</li>
        <li>Menurunnya kualitas sumber daya manusia</li>
    </ul>

    <h3>Periode 1000 Hari Pertama Kehidupan (1000 HPK)</h3>
    <p>
    <b>1000 Hari Pertama Kehidupan (1000 HPK)</b> merupakan periode
    emas dan krusial dalam pertumbuhan anak yang dimulai sejak
    masa kehamilan hingga anak berusia 2 tahun (0 - 24 bulan).
    Pada periode ini, pertumbuhan fisik dan perkembangan otak
    berlangsung sangat cepat dan tidak dapat diulang.
    </p>

    <p>
    Kekurangan gizi yang terjadi selama periode 1000 HPK
    berisiko menyebabkan stunting yang bersifat permanen,
    sehingga pencegahan stunting harus difokuskan pada
    pemenuhan gizi ibu hamil, ibu menyusui, dan balita.
    </p>

    <h3>Faktor Penyebab Stunting</h3>
    <ul>
        <li>Asupan gizi ibu dan anak yang tidak mencukupi</li>
        <li>Riwayat infeksi yang sering atau berulang</li>
        <li>Sanitasi dan lingkungan yang kurang sehat</li>
        <li>Akses layanan kesehatan yang terbatas</li>
        <li>Kurangnya edukasi dan pengetahuan orang tua</li>
    </ul>

    <h3>Upaya Pencegahan dan Penanganan</h3>
    <p>
    Pencegahan stunting perlu dilakukan sejak dini,
    terutama selama periode 1000 HPK, melalui langkah-langkah berikut:
    </p>

    <ul>
        <li>Pemenuhan gizi seimbang sejak masa kehamilan</li>
        <li>Pemberian ASI eksklusif selama 6 bulan</li>
        <li>Pemberian MP-ASI yang bergizi dan sesuai usia</li>
        <li>Imunisasi lengkap dan pencegahan infeksi</li>
        <li>Perbaikan sanitasi dan akses air bersih</li>
        <li>Pemantauan pertumbuhan balita secara rutin</li>
    </ul>

    <h3>Peran Sistem CareStunt</h3>
    <p>
    <b>CareStunt</b> merupakan aplikasi berbasis
    <b>sistem pakar</b> yang berfungsi sebagai
    <b>pendukung keputusan</b> dalam menganalisis
    risiko stunting pada balita.
    Sistem ini membantu memberikan gambaran awal
    berdasarkan parameter kesehatan dan lingkungan,
    sehingga dapat digunakan sebagai bahan edukasi
    dan pertimbangan sebelum konsultasi medis.
    </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# HALAMAN: TENTANG
# =========================================
elif st.session_state.page == "ℹ️ Tentang":
    st.markdown("## ℹ️ Tentang Sistem")

    st.markdown("""
    <div class="glass">
    <h3>Deskripsi Sistem</h3>
    <p>
    <b>CareStunt</b> merupakan aplikasi <b>Sistem Pakar</b>
    yang dirancang untuk membantu proses
    <b>analisis risiko stunting pada balita</b>.
    Sistem ini bekerja dengan memodelkan pengetahuan pakar
    dalam bentuk hubungan probabilistik antar faktor penyebab stunting.
    </p>

    <h4>Metode dan Pendekatan</h4>
    <ul>
        <li>Jenis Sistem: <b>Sistem Pakar</b></li>
        <li>Metode Inferensi: <b>Bayesian Network</b></li>
        <li>Pendekatan: Probabilistik</li>
    </ul>

    <h4>Kegunaan Sistem</h4>
    <ul>
        <li>Membantu orang tua dalam memahami risiko stunting pada balita</li>
        <li>Mendukung tenaga kesehatan dalam pengambilan keputusan awal</li>
        <li>Menyediakan estimasi risiko berdasarkan parameter kesehatan balita</li>
        <li>Memberikan rekomendasi awal secara cepat dan sistematis</li>
    </ul>

    <h4>Batasan Sistem</h4>
    <p>
    Sistem ini bersifat <b>pendukung keputusan</b>
    dan tidak menggantikan peran tenaga medis.
    Hasil analisis yang diberikan merupakan estimasi risiko awal
    yang dapat digunakan sebagai bahan pertimbangan
    sebelum dilakukan pemeriksaan lebih lanjut oleh tenaga kesehatan.
    </p>
    </div>
    """, unsafe_allow_html=True)
