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
import hashlib

import sys
import os

# supaya bisa akses folder config
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from config.koneksi import koneksi

# koneksi database
db = koneksi()
cursor = db.cursor()

st.set_page_config(layout="wide")

st.title("Manajemen Admin")
st.caption("Kelola akun admin yang dapat mengakses sistem")

# =============================
# fungsi enkripsi password
# =============================
def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

# =============================
# TAMBAH ADMIN
# =============================
st.subheader("Tambah Admin")

col1,col2 = st.columns(2)

with col1:

    nama = st.text_input("Nama Admin")

    username = st.text_input("Username")

with col2:

    password = st.text_input(
        "Password",
        type="password"
    )

    konfirmasi = st.text_input(
        "Konfirmasi Password",
        type="password"
    )

if st.button("Simpan Admin"):

    if not nama or not username or not password:

        st.warning("Semua field harus diisi")

    elif password != konfirmasi:

        st.error("Konfirmasi password tidak sama")

    else:

        pwd = hash_password(password)

        try:

            cursor.execute("""

            INSERT INTO admin
            (nama,username,password)

            VALUES (%s,%s,%s)

            """,(nama,username,pwd))

            db.commit()

            st.success("Admin berhasil ditambahkan")

            st.rerun()

        except Exception as e:

            st.error("Username sudah digunakan atau terjadi error")

            st.write(e)

st.divider()

# =============================
# TAMPIL DATA ADMIN
# =============================
st.subheader("Daftar Admin")

df = pd.read_sql("""

SELECT *
FROM admin
ORDER BY id_admin DESC

""", db)

st.metric(
    "Total Admin",
    len(df)
)

if len(df) > 0:

    # nomor urut
    df.index = range(1,len(df)+1)

    st.dataframe(

        df[
            ["nama","username","created_at"]
        ],

        use_container_width=True

    )

    st.divider()

    # =============================
    # EDIT ADMIN
    # =============================
    st.subheader("Edit Admin")

    pilih = st.selectbox(

        "Pilih nomor admin",

        df.index

    )

    nama_edit = st.text_input(

        "Nama baru",

        df.loc[pilih,"nama"]

    )

    username_edit = st.text_input(

        "Username baru",

        df.loc[pilih,"username"]

    )

    st.caption("Kosongkan password jika tidak ingin diubah")

    password_baru = st.text_input(

        "Password baru",

        type="password"

    )

    konfirmasi_baru = st.text_input(

        "Konfirmasi password baru",

        type="password"

    )

    if st.button("Update Admin"):

        id_data = df.loc[pilih,"id_admin"]

        try:

            # jika password diisi
            if password_baru:

                if password_baru != konfirmasi_baru:

                    st.error("Konfirmasi password tidak sama")

                    st.stop()

                pwd = hash_password(password_baru)

                cursor.execute("""

                UPDATE admin

                SET nama=%s,
                username=%s,
                password=%s

                WHERE id_admin=%s

                """,(nama_edit,username_edit,pwd,id_data))

            else:

                # jika password tidak diubah
                cursor.execute("""

                UPDATE admin

                SET nama=%s,
                username=%s

                WHERE id_admin=%s

                """,(nama_edit,username_edit,id_data))

            db.commit()

            st.success("Data admin berhasil diupdate")

            st.rerun()

        except Exception as e:

            st.error("Username sudah digunakan atau terjadi error")

            st.write(e)

    st.divider()

    # =============================
    # HAPUS ADMIN
    # =============================
    st.subheader("Hapus Admin")

    hapus = st.selectbox(

        "Pilih nomor yang akan dihapus",

        df.index,

        key="hapus"

    )

    if st.button("Hapus Admin"):

        id_hapus = df.loc[hapus,"id_admin"]

        cursor.execute("""

        DELETE FROM admin
        WHERE id_admin=%s

        """,(id_hapus,))

        db.commit()

        st.success("Admin berhasil dihapus")

        st.rerun()

else:

    st.info("Belum ada admin")