import streamlit as st
import pandas as pd
import sys
import os

import random

sekolah_sd = [
    "SD Negeri 01 Padang",
    "SD Negeri 05 Padang",
    "SD Negeri 10 Padang"
]

sekolah_smp = [
    "SMP Negeri 1 Padang",
    "MTsN 1 Padang",
    "SMP Negeri 7 Padang"
]

sekolah_sma = [
    "SMA Negeri 1 Padang",
    "MAN 1 Padang",
    "SMA Negeri 3 Padang"
]

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

st.subheader("📂 Import Data Komentar")

file = st.file_uploader(
    "Upload file Excel / CSV",
    type=["xlsx", "csv"]
)

if file is not None:

    try:
        # baca file
        if file.name.endswith(".xlsx"):
            df_upload = pd.read_excel(file)
        elif file.name.endswith(".csv"):
            df_upload = pd.read_csv(file)

        st.write("Preview Data Upload:")
        st.dataframe(df_upload)

        # =====================
        # NORMALISASI KOLOM
        # =====================
        df_upload.columns = df_upload.columns.str.strip()
        df_upload.columns = df_upload.columns.str.lower()

        # cari kolom komentar otomatis
        kolom_komentar = None

        for col in df_upload.columns:
            if "komentar" in col:
                kolom_komentar = col
                break

        if kolom_komentar is None:
            st.error("Kolom komentar tidak ditemukan!")
            st.stop()

        # rename kalau beda
        df_upload.rename(columns={
            'nama lengkap': 'nama',
            'komentar': 'komentar',
            'isi komentar': 'komentar'
        }, inplace=True)

        if st.button("Import ke Database"):

            for i, row in df_upload.iterrows():

                nama = row.get('nama', None)
                komentar = row.get(kolom_komentar, None)

                if pd.isna(nama) or pd.isna(komentar):
                    continue  # skip kalau kosong

                # default data
                # sekolah = "Tidak diketahui"

                umur = row.get('umur', None)

                if pd.notna(umur):

                    umur = int(umur)

                    # =====================
                    # SD (5 - 12 tahun)
                    # =====================
                    if 5 <= umur <= 12:
                        kelas = f"Kelas {umur - 4}"   # umur 6 = kelas 2, dll
                        sekolah = random.choice(sekolah_sd)

                    # =====================
                    # SMP (12 - 14 tahun)
                    # =====================
                    elif 12 < umur <= 14:
                        kelas = f"Kelas {umur - 11} SMP"
                        sekolah = random.choice(sekolah_smp)

                    # =====================
                    # SMA (14 - 18 tahun)
                    # =====================
                    elif 14 < umur <= 18:
                        kelas = f"Kelas {umur - 13} SMA"
                        sekolah = random.choice(sekolah_sma)

                    else:
                        kelas = "Tidak diketahui"
                        sekolah = "Tidak diketahui"

                else:
                    kelas = "Tidak diketahui"
                    sekolah = "Tidak diketahui"

                # =====================
                # INSERT RESPONDEN
                # =====================
                cursor.execute("""
                    INSERT INTO responden (nama, sekolah, kelas)
                    VALUES (%s, %s, %s)
                """, (nama, sekolah, kelas))

                id_responden = cursor.lastrowid

                # =====================
                # INSERT KOMENTAR
                # =====================
                cursor.execute("""
                    INSERT INTO komentar (id_responden, isi_komentar)
                    VALUES (%s, %s)
                """, (id_responden, komentar))

            db.commit()

            st.success("✅ Data berhasil diimport!")
            st.rerun()

    except Exception as e:
        st.error(f"Terjadi error: {e}")

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
    # EDIT DATA (KOMENTAR + RESPONDEN)
    # =====================
    st.subheader("Edit Data Komentar & Responden")

    pilih = st.selectbox(
        "Pilih nomor data",
        df.index
    )

    # ambil data lama
    nama_lama = df.loc[pilih, "nama"]
    sekolah_lama = df.loc[pilih, "sekolah"]
    kelas_lama = df.loc[pilih, "kelas"]
    komentar_lama = df.loc[pilih, "isi_komentar"]

    # input form
    nama_baru = st.text_input("Nama", nama_lama)
    sekolah_baru = st.text_input("Sekolah", sekolah_lama)
    kelas_baru = st.text_input("Kelas", kelas_lama)
    komentar_baru = st.text_area("Komentar", komentar_lama)

    if st.button("Update Data"):

        id_komentar = int(df.loc[pilih, "id_komentar"])
        id_responden = int(df.loc[pilih, "id_responden"])

        # =====================
        # UPDATE TABEL KOMENTAR
        # =====================
        cursor.execute("""
        UPDATE komentar
        SET isi_komentar=%s
        WHERE id_komentar=%s
        """, (komentar_baru, id_komentar))

        # =====================
        # UPDATE TABEL RESPONDEN
        # =====================
        cursor.execute("""
        UPDATE responden
        SET nama=%s,
            sekolah=%s,
            kelas=%s
        WHERE id_responden=%s
        """, (nama_baru, sekolah_baru, kelas_baru, id_responden))

        db.commit()

        st.success("Data berhasil diupdate")

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
