import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
from fpdf import FPDF  # type: ignore
import plotly.express as px  # type: ignore
import tempfile  # type: ignore
from model_stunting import BayesianNetworkStunting

# LOAD CSS FILE
def load_css(path):
    with open(path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("CSS/stale.css")

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="CareStunt - Sistem Pakar",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# FUNGSI SARAN TINDAKAN
def get_saran(risiko):
    if risiko == "Tinggi":
        return [
            "Konsultasi ke tenaga kesehatan atau puskesmas terdekat untuk pemeriksaan lanjutan.",
            "Lakukan penimbangan berat badan dan pengukuran tinggi badan setiap bulan.",
            "Perbaiki asupan gizi harian dengan menambahkan sumber protein (telur, ikan, daging), zat besi, dan zinc.",
            "Pastikan balita mendapatkan ASI atau susu sesuai usia dan kebutuhan gizi.",
            "Jaga kebersihan lingkungan, air minum, dan sanitasi untuk mencegah infeksi berulang.",
            "Ikuti kegiatan posyandu secara rutin untuk pemantauan tumbuh kembang."
        ]

    elif risiko == "Sedang":
        return [
            "Tingkatkan kualitas pola makan dengan menu bergizi seimbang setiap hari.",
            "Pastikan jadwal imunisasi balita lengkap dan tepat waktu.",
            "Pantau berat dan tinggi badan minimal setiap 2 - 3 bulan.",
            "Kurangi risiko infeksi dengan menjaga kebersihan diri dan lingkungan rumah.",
            "Berikan makanan tambahan jika diperlukan sesuai anjuran tenaga kesehatan."
        ]

    else:  # Rendah
        return [
            "Pertahankan pola makan sehat dan bergizi seimbang sesuai usia balita.",
            "Lanjutkan pemantauan pertumbuhan secara rutin di posyandu atau fasilitas kesehatan.",
            "Pastikan kebersihan lingkungan tetap terjaga.",
            "Tetap berikan stimulasi dan perhatian terhadap tumbuh kembang balita."
        ]



# FUNGSI PDF
def generate_pdf(nama, umur, hasil, risiko, grafik_path):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Warna Biru Tua
    pdf.set_fill_color(30, 64, 175) 
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 20, "LAPORAN HASIL ANALISIS CARESTUNT", ln=True, align="C")
    pdf.ln(10)
    
    # Kembali ke teks hitam
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"IDENTITAS BALITA", ln=True)
    
    # Tabel Identitas Sederhana
    pdf.set_font("Arial", "", 11)
    pdf.cell(40, 8, "Nama Balita", border=1)
    pdf.cell(0, 8, f" : {nama}", border=1, ln=True)
    pdf.cell(40, 8, "Umur", border=1)
    pdf.cell(0, 8, f" : {umur} Bulan", border=1, ln=True)
    
    # Hasil Risiko dengan Background Warna
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "HASIL RISIKO:", 0)
    
    if risiko == "Tinggi": pdf.set_text_color(239, 68, 68)
    elif risiko == "Sedang": pdf.set_text_color(217, 119, 6)
    else: pdf.set_text_color(22, 163, 74)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, risiko.upper(), ln=True)
    pdf.set_text_color(0, 0, 0) 
    
    # Garis Pembatas
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Grafik
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "Visualisasi Probabilitas:", ln=True)
    pdf.image(grafik_path, x=15, w=180) 
    pdf.ln(5)

    # Detail Persentase
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "Detail Angka:", ln=True)
    pdf.set_font("Arial", "", 10)
    for k, v in hasil.items():
        pdf.cell(0, 6, f"- {k}: {v:.2f}%", ln=True)

    # Saran
    pdf.ln(10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, " REKOMENDASI TINDAKAN:", ln=True, fill=True)
    pdf.set_font("Arial", "", 10)
    saran_list = get_saran(risiko)
    for s in saran_list:
        pdf.multi_cell(0, 7, f"* {s}")

    return pdf.output(dest="S").encode("latin-1")


# NAVIGATION STATE
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

def nav_to(page):
    st.session_state.page = page
    st.rerun()


# SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🩺 CareStunt</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:13px;'>Sistem Pakar Diagnosa Stunting</p>", unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        ["Beranda", "Diagnosa", "Edukasi", "Tentang"],
        index=["Beranda", "Diagnosa", "Edukasi", "Tentang"].index(st.session_state.page)
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


# HALAMAN BERANDA
if st.session_state.page == "Beranda":
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
    <h3>Tujuan Sistem</h3>
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
        nav_to("Diagnosa")


# HALAMAN DIAGNOSA
elif st.session_state.page == "Diagnosa":

    # JUDUL HALAMAN
    st.markdown("# Analisis Risiko Stunting")
    st.markdown(
        "<p style='opacity:0.3;'>Masukkan data balita untuk melihat probabilitas risiko stunting.</p>",
        unsafe_allow_html=True
    )

    # INPUT DATA
    st.markdown("## Input Data Balita")

    col1, col2 = st.columns(2)

    with col1:
        nama = st.text_input("Nama Balita", placeholder="Contoh: Budi")
        umur = st.number_input("Umur (Bulan)", 0, 60, 24)
        pola = st.selectbox("Pola Makan", ["Baik", "Cukup", "Kurang"])

    with col2:
        sakit = st.selectbox("Riwayat Infeksi", ["Tidak Ada", "Jarang", "Sering"])
        sanitasi = st.selectbox("Sanitasi Lingkungan", ["Baik", "Cukup", "Kurang"])

    st.markdown("<br>", unsafe_allow_html=True)
    btn = st.button("Hitung Risiko Stunting")

    # PROSES DIAGNOSA
    if btn:
        if not nama:
            st.error("Nama balita wajib diisi.")
        else:
            with st.spinner("Sedang menganalisis data..."):
                model = BayesianNetworkStunting()
                hasil, _ = model.inferensi(umur, pola, sakit, sanitasi)

                # RISIKO & CONFIDENCE
                risiko = max(hasil, key=hasil.get)
                confidence = hasil[risiko]
                confidence_percent = round(confidence, 2)

            # WARNA RISIKO
            color_map = {
                "Rendah": "#22c55e",
                "Sedang": "#facc15",
                "Tinggi": "#ef4444"
            }
            res_color = color_map[risiko]

            # GRAFIK PROBABILITAS
            df = pd.DataFrame(hasil.items(), columns=["Risiko", "Persentase"])

            fig = px.bar(
                df,
                x="Risiko",
                y="Persentase",
                text=df["Persentase"].apply(lambda x: f"{x:.1f}%"),
                color="Risiko",
                color_discrete_map=color_map
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis=dict(range=[0, 110]),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                height=380,
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # HASIL RISIKO
            st.markdown("## Rekomendasi Tindakan")
            for i, s in enumerate(get_saran(risiko), start=1):
                st.markdown(f"**{i}.** {s}")

            st.markdown("""
                <style>
                /* DOWNLOAD BUTTON*/
                div[data-testid="stDownloadButton"] > button {
                    width: auto !important;
                    display: inline-flex !important;
                    justify-content: center;
                    align-items: center;
                }

                /* Text tetap putih */
                div[data-testid="stDownloadButton"] > button span {
                    color: #ffffff !important;
                }
                        
                /* HOVER */
                div[data-testid="stDownloadButton"] > button:hover {
                    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
                    box-shadow: 0 12px 30px rgba(34,197,94,0.35);
                }

                /* ACTIVE / CLICK */
                div[data-testid="stDownloadButton"] > button:active,
                div[data-testid="stDownloadButton"] > button:focus {
                    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
                    color: #ffffff !important;
                    box-shadow: none !important;
                    outline: none !important;
                }
                </>
                """, unsafe_allow_html=True)


            # PDF
            tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig.write_image(tmpfile.name)

            pdf_bytes = generate_pdf(
                nama, umur, hasil, risiko, tmpfile.name
            )

            st.download_button(
                "📄 Unduh Laporan PDF",
                data=pdf_bytes,
                file_name=f"Laporan_CareStunt_{nama}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# HALAMAN EDUKASI
elif st.session_state.page == "Edukasi":
    st.markdown("## Edukasi Stunting")

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


# HALAMAN TENTANG
elif st.session_state.page == "Tentang":
    st.markdown("## Tentang Sistem")

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
