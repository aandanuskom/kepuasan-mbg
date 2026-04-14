import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# =====================
# CONFIG PAGE
# =====================
st.set_page_config(
    page_title="Dashboard MBG",
    page_icon="📊",
    layout="wide"
)

# =====================
# LOGIN SESSION
# =====================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.get("login"):
    st.switch_page("pages/login_admin.py")
    st.stop()

# =====================
# DATABASE CONNECTION
# =====================
def koneksi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_kepuasan"
    )

db = koneksi()

# =====================
# CSS RESPONSIVE
# =====================
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}

.card h3 {
    font-size: 34px;
    margin: 0;
}

.card p {
    color: gray;
    font-size: 14px;
}

.title {
    font-size: 28px;
    font-weight: 600;
}

/* HIDE SIDEBAR NAV */
[data-testid="stSidebarNav"]{
    display:none;
}

/* RESPONSIVE */
@media screen and (max-width: 768px) {

    .card {
        padding: 12px !important;
    }

    .card h3 {
        font-size: 22px !important;
    }

    .title {
        font-size: 20px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================
# SIDEBAR MENU
# =====================
st.sidebar.title("MENU ADMIN")

if st.sidebar.button("📊 Dashboard"): 
    st.switch_page("pages/1_Dashboard.py") 
    
if st.sidebar.button("📂 Upload Training"): 
    st.switch_page("pages/2_Upload_Training.py") 
    
if st.sidebar.button("🧪 Upload Testing"): 
    st.switch_page("pages/3_Upload_Testing.py") 
    
if st.sidebar.button("🤖 Training SVM"): 
    st.switch_page("pages/4_Training_SVM.py") 
    
# if st.sidebar.button("📈 Hasil Prediksi Training"): 
#     st.switch_page("pages/5_Hasil_Prediksi.py") 
    
if st.sidebar.button("💬 Data Komentar"): 
    st.switch_page("pages/6_Data_Komentar.py") 
    
if st.sidebar.button("⚙ Proses SVM Komentar"): 
    st.switch_page("pages/7_Proses_Sentimen.py") 
    
if st.sidebar.button("📑 Laporan"): 
    st.switch_page("pages/8_Laporan.py") 
    
if st.sidebar.button("👤 Manajemen Admin"): 
    st.switch_page("pages/9_Manajemen_Admin.py") 

st.sidebar.divider() 

if st.sidebar.button("🚪 Logout"): 
    st.session_state.clear() 
    
    st.switch_page("app.py")

# =====================
# TITLE
# =====================
st.markdown('<p class="title">📊 Dashboard Survey MBG - SVM</p>', unsafe_allow_html=True)

# =====================
# QUERY DATA
# =====================
jml_training = pd.read_sql("SELECT COUNT(*) as total FROM dataset_training", db)
jml_testing = pd.read_sql("SELECT COUNT(*) as total FROM dataset_testing", db)
jml_komentar = pd.read_sql("SELECT COUNT(*) as total FROM komentar", db)

akurasi = pd.read_sql("""
SELECT akurasi 
FROM log_training 
ORDER BY id_log DESC 
LIMIT 1
""", db)

# RESPONDEN ONLY
sentimen_responden = pd.read_sql("""
SELECT hasil, COUNT(*) as jumlah
FROM hasil_sentimen
GROUP BY hasil
""", db)

komentar_per_hari = pd.read_sql("""
SELECT DATE(tanggal) as tgl, COUNT(*) as jumlah
FROM komentar
GROUP BY DATE(tanggal)
""", db)

# =====================
# HANDLE EMPTY
# =====================
total_training = jml_training['total'][0] if not jml_training.empty else 0
total_testing = jml_testing['total'][0] if not jml_testing.empty else 0
total_komentar = jml_komentar['total'][0] if not jml_komentar.empty else 0
nilai_akurasi = akurasi['akurasi'][0] if not akurasi.empty else 0

# =====================
# CARDS
# =====================
col1, col2, col3, col4 = st.columns(4, gap="small")

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>{total_training}</h3>
        <p>Data Training</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>{total_testing}</h3>
        <p>Data Testing</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <h3>{total_komentar}</h3>
        <p>Komentar Responden</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card">
        <h3>{f"{round(nilai_akurasi * 100, 2)}%"}</h3>
        <p>Akurasi Model</p>
    </div>
    """, unsafe_allow_html=True)

# =====================
# CHART SECTION
# =====================
col5, col6 = st.columns([1,1], gap="large")

# =====================
# PIE RESPONDEN ONLY
# =====================
with col5:

    st.subheader("Persentase Kepuasan Responden")

    if not sentimen_responden.empty:

        fig, ax = plt.subplots(figsize=(4,4))

        ax.pie(
            sentimen_responden["jumlah"],
            labels=sentimen_responden["hasil"],
            autopct='%1.1f%%',
            startangle=90
        )

        ax.set_title("Kepuasan Responden")

        st.pyplot(fig)

    else:
        st.info("Belum ada data responden")

# =====================
# BAR CHART
# =====================
with col6:

    st.subheader("Jumlah Komentar per Hari")

    if not komentar_per_hari.empty:

        fig, ax = plt.subplots(figsize=(5,3))

        ax.bar(
            komentar_per_hari['tgl'],
            komentar_per_hari['jumlah']
        )

        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah")
        plt.xticks(rotation=45)

        st.pyplot(fig)

    else:
        st.info("Belum ada komentar")

# =====================
# FOOTER
# =====================
st.write("")
st.markdown("""
<div style='text-align:center; color:gray; font-size:20px; padding:10px;'>
    Sistem Analisis Kepuasan MBG menggunakan metode SVM
</div>
""", unsafe_allow_html=True)
