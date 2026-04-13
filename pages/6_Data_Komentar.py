import streamlit as st
import pandas as pd
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
# SEMBUNYIKAN MENU DEFAULT
# =====================
st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
}
</style>
""", unsafe_allow_html=True)

# =====================
# SIDEBAR CUSTOM
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

# =====================
# IMPORT KONEKSI
# =====================
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from config.koneksi import koneksi

db = koneksi()
cursor = db.cursor()

# =====================
# CONFIG PAGE
# =====================
st.set_page_config(layout="wide")

st.title("Data Komentar Responden")
st.caption("Daftar komentar yang dikirim oleh responden")

# =====================
# AMBIL DATA KOMENTAR
# =====================
df = pd.read_sql("""

SELECT

k.id_komentar,
r.id_responden,
r.nama,
r.sekolah,
r.kelas,
k.isi_komentar,
r.tanggal

FROM komentar k

JOIN responden r
ON k.id_responden = r.id_responden

ORDER BY k.id_komentar ASC

""", db)

# =====================
# RINGKASAN JUMLAH
# =====================
st.metric(
    "Total Komentar",
    len(df)
)

st.divider()

# =====================
# TAMPIL TABEL
# =====================
if len(df) > 0:

    df.index = range(1,len(df)+1)

    st.subheader("Daftar Komentar")

    st.dataframe(
        df[[
            "nama",
            "sekolah",
            "kelas",
            "isi_komentar",
            "tanggal"
        ]],
        use_container_width=True
    )

    st.divider()

    # =====================
    # EDIT KOMENTAR
    # =====================
    st.subheader("Edit Komentar")

    pilih = st.selectbox(

        "Pilih nomor komentar",

        df.index

    )

    komentar_lama = df.loc[pilih,"isi_komentar"]

    komentar_baru = st.text_area(

        "Edit komentar",

        komentar_lama

    )

    if st.button("Update Komentar"):

        id_data = int(df.loc[pilih, "id_komentar"])   # FIX DI SINI

        cursor.execute("""
        UPDATE komentar
        SET isi_komentar=%s
        WHERE id_komentar=%s
        """, (komentar_baru, id_data))

        db.commit()

        st.success("Komentar berhasil diupdate")

        st.rerun()

    st.divider()

    # =====================
    # HAPUS KOMENTAR
    # =====================
    st.subheader("Hapus Komentar")

    hapus = st.selectbox(

        "Pilih nomor yang akan dihapus",

        df.index,

        key="hapus"

    )

    if st.button("Hapus Komentar"):

        id_hapus = df.loc[hapus,"id_komentar"]

        cursor.execute("""

        DELETE FROM komentar
        WHERE id_komentar=%s

        """,(id_hapus,))

        db.commit()

        st.success("Komentar berhasil dihapus")

        st.rerun()

else:

    st.warning("Belum ada komentar responden")