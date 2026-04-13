import streamlit as st

# =====================
# SESSION LOGIN
# =====================
# default session supaya reload tidak error
if "login" not in st.session_state:
    st.session_state.login = False

# cek login
if not st.session_state.get("login"):

    st.switch_page("pages/login_admin.py")
    st.stop()

# sembunyikan menu default
st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
}
</style>
""", unsafe_allow_html=True)

# sidebar custom
st.sidebar.title("MENU ADMIN")

if st.sidebar.button("📊 Dashboard"):
    st.switch_page("pages/1_Dashboard.py")

if st.sidebar.button("📂 Upload Training"):
    st.switch_page("pages/2_Upload_Training.py")

if st.sidebar.button("🧪 Upload Testing"):
    st.switch_page("pages/3_Upload_Testing.py")

if st.sidebar.button("🤖 Training SVM"):
    st.switch_page("pages/4_Training_SVM.py")

if st.sidebar.button("📈 Hasil Prediksi"):
    st.switch_page("pages/5_Hasil_Prediksi.py")

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


import pandas as pd
import joblib

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from config.koneksi import koneksi

# =============================
# koneksi database
# =============================
db = koneksi()
cursor = db.cursor()

st.set_page_config(layout="wide")

st.title("Hasil Prediksi Kepuasan")
st.caption("Hasil klasifikasi komentar responden menggunakan model SVM")

# =============================
# cek model tersedia
# =============================
if not os.path.exists("model/svm_model.joblib"):

    st.error("Model belum dibuat. Silakan training SVM terlebih dahulu.")
    st.stop()

# load model
model = joblib.load("model/svm_model.joblib")
tfidf = joblib.load("model/tfidf.joblib")

# =============================
# ambil data testing
# =============================
df = pd.read_sql("""

SELECT *
FROM dataset_testing
ORDER BY id_testing DESC

""", db)

if len(df) == 0:

    st.warning("Belum ada data testing")

else:

    st.subheader("Data Komentar")

    df.index = range(1,len(df)+1)

    st.dataframe(
        df[["komentar"]],
        use_container_width=True
    )

    st.divider()

    # =============================
    # tombol prediksi
    # =============================
    if st.button("Proses Prediksi"):

        # transform teks
        X = tfidf.transform(df["komentar"])

        # prediksi
        hasil = model.predict(X)

        df["hasil"] = hasil

        # simpan ke tabel hasil_prediksi
        cursor.execute("DELETE FROM hasil_prediksi")

        for i,row in df.iterrows():

            cursor.execute("""

            INSERT INTO hasil_prediksi
            (komentar,hasil)

            VALUES (%s,%s)

            """,(row["komentar"],row["hasil"]))

        db.commit()

        st.success("Prediksi selesai")

# =============================
# tampilkan hasil
# =============================
df_hasil = pd.read_sql("""

SELECT *
FROM hasil_prediksi
ORDER BY id_prediksi DESC

""", db)

if len(df_hasil) > 0:

    st.subheader("Hasil Klasifikasi")

    df_hasil.index = range(1,len(df_hasil)+1)

    st.dataframe(
        df_hasil[["komentar","hasil"]],
        use_container_width=True
    )

    st.divider()

    # =============================
    # ringkasan
    # =============================
    st.subheader("Ringkasan Kepuasan")

    puas = len(df_hasil[df_hasil["hasil"]=="PUAS"])

    netral = len(df_hasil[df_hasil["hasil"]=="NETRAL"])

    tidak_puas = len(df_hasil[df_hasil["hasil"]=="TIDAK PUAS"])

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "PUAS",
        puas
    )

    col2.metric(
        "NETRAL",
        netral
    )

    col3.metric(
        "TIDAK PUAS",
        tidak_puas
    )