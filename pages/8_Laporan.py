import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# =====================
# SESSION LOGIN
# =====================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.get("login"):
    st.switch_page("pages/login_admin.py")
    st.stop()

# =====================
# SIDEBAR (JANGAN DIHAPUS)
# =====================
st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
}
</style>
""", unsafe_allow_html=True)

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
# DB CONNECTION
# =====================
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from config.koneksi import koneksi
db = koneksi()

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(layout="wide")

st.title("📑 Laporan Kepuasan MBG")
st.caption("Hasil analisis sentimen responden menggunakan SVM")

# =====================
# DATA RESPONDEN (FIX)
# =====================
df = pd.read_sql("""
SELECT 
    k.isi_komentar AS komentar,
    h.hasil,
    h.confidence,
    k.tanggal
FROM hasil_sentimen h
JOIN komentar k 
ON h.id_komentar = k.id_komentar
ORDER BY h.id_komentar ASC
""", db)

if df.empty:
    st.warning("Belum ada data laporan")
    st.stop()

# =====================
# NORMALISASI
# =====================
df["hasil"] = df["hasil"].str.upper()

# =====================
# HITUNG JUMLAH
# =====================
total = len(df)
puas = (df["hasil"] == "PUAS").sum()
netral = (df["hasil"] == "NETRAL").sum()
tidak_puas = (df["hasil"] == "TIDAK PUAS").sum()

# =====================
# RINGKASAN
# =====================
st.subheader("📊 Ringkasan")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Responden", total)
c2.metric("PUAS", puas)
c3.metric("NETRAL", netral)
c4.metric("TIDAK PUAS", tidak_puas)

st.divider()

# =====================
# PIE CHART
# =====================
st.subheader("📈 Grafik Persentase Kepuasan")

fig, ax = plt.subplots(figsize=(5,5))

labels = ["PUAS", "NETRAL", "TIDAK PUAS"]
values = [puas, netral, tidak_puas]

ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
ax.set_title("Kepuasan Responden")

st.pyplot(fig)

st.divider()

# =====================
# BAR CHART
# =====================
st.subheader("📊 Perbandingan Kepuasan")

fig2, ax2 = plt.subplots()

ax2.bar(labels, values)

ax2.set_ylabel("Jumlah")
ax2.set_title("Distribusi Sentimen")

st.pyplot(fig2)

st.divider()

st.subheader("🔎 Filter Data Berdasarkan Tanggal")

df["tanggal"] = pd.to_datetime(df["tanggal"])

min_date = df["tanggal"].min()
max_date = df["tanggal"].max()

date_range = st.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date)
)

# =====================
# HANDLE BELUM LENGKAP
# =====================
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.warning("Silakan pilih rentang tanggal (start dan end)")
    st.stop()

# filter data
df_filtered = df[
    (df["tanggal"] >= pd.to_datetime(start_date)) &
    (df["tanggal"] <= pd.to_datetime(end_date))
]

# =====================
# TABLE DETAIL
# =====================
st.subheader("📋 Data Lengkap")

df_filtered.index = range(1, len(df_filtered) + 1)

st.dataframe(df_filtered, use_container_width=True, hide_index=True)

# =====================
# EXPORT
# =====================
st.subheader("⬇ Export Data")

csv = df_filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV (Filtered)",
    data=csv,
    file_name="laporan_kepuasan_filtered.csv",
    mime="text/csv"
)