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

# if st.sidebar.button("📈 Hasil Prediksi"):
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
    

import pandas as pd

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from config.koneksi import koneksi

db = koneksi()
cursor = db.cursor()

st.set_page_config(layout="wide")

st.title("Upload Data Testing")
st.caption("Kelola data komentar yang akan diprediksi oleh model SVM")

tab1, tab2, tab3 = st.tabs([
    "Upload File",
    "Input Manual",
    "Data Testing"
])

# =====================================
# TAB 1 UPLOAD FILE
# =====================================
with tab1:

    st.subheader("Upload Dataset Testing")

    st.info("""
    Format file harus memiliki kolom:

    komentar

    contoh:

    makanannya enak
    porsi sedikit
    kurang hangat
    """)

    file = st.file_uploader(
        "Upload file CSV",
        type=["csv"]
    )

    if file:

        df = pd.read_csv(file)

        st.write("Preview Data")
        st.dataframe(df, use_container_width=True)

        if st.button("Simpan ke Database"):

            for i, row in df.iterrows():

                cursor.execute("""
                INSERT INTO dataset_testing
                (komentar)
                VALUES (%s)
                """,(row["komentar"],))

            db.commit()

            st.success("Data testing berhasil disimpan")

# =====================================
# TAB 2 INPUT MANUAL
# =====================================
with tab2:

    st.subheader("Tambah Data Testing Manual")

    komentar = st.text_area("Komentar")

    if st.button("Simpan Komentar"):

        cursor.execute("""
        INSERT INTO dataset_testing
        (komentar)
        VALUES (%s)
        """,(komentar,))

        db.commit()

        st.success("Komentar berhasil ditambahkan")

# =====================================
# TAB 3 DATA TESTING
# =====================================
with tab3:

    st.subheader("Data Testing")

    df = pd.read_sql("""
    SELECT *
    FROM dataset_testing
    ORDER BY id_testing DESC
    """, db)

    if len(df) == 0:

        st.warning("Belum ada data testing")

    else:

        # nomor urut
        df.index = range(1,len(df)+1)

        tampil = df[["komentar"]]

        st.dataframe(
            tampil,
            use_container_width=True
        )

        st.divider()

        # =====================
        # EDIT DATA
        # =====================
        st.subheader("Edit Komentar")

        pilih = st.selectbox(
            "Pilih nomor data",
            df.index
        )

        data_terpilih = df.loc[pilih]

        komentar_baru = st.text_area(
            "Ubah komentar",
            value=data_terpilih["komentar"]
        )

        if st.button("Update Komentar"):

            cursor.execute("""
            UPDATE dataset_testing
            SET komentar=%s
            WHERE id_testing=%s
            """,(komentar_baru,data_terpilih["id_testing"]))

            db.commit()

            st.success("Komentar berhasil diupdate")

        st.divider()

        # =====================
        # HAPUS DATA
        # =====================
        st.subheader("Hapus Data")

        hapus_no = st.selectbox(
            "Pilih nomor yang ingin dihapus",
            df.index,
            key="hapus"
        )

        if st.button("Hapus Data"):

            id_hapus = df.loc[hapus_no]["id_testing"]

            cursor.execute("""
            DELETE FROM dataset_testing
            WHERE id_testing=%s
            """,(id_hapus,))

            db.commit()

            st.success("Data berhasil dihapus")