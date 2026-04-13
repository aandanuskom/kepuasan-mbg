import streamlit as st
from config.koneksi import koneksi

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Survey MBG",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# sembunyikan sidebar
st.markdown("""
<style>

[data-testid="stSidebar"]{
    display:none;
}

.main {
    background-color:#f0ebf8;
}

.header {
    background:#673ab7;
    height:8px;
    border-radius:10px 10px 0 0;
}

.card {
    background:white;
    padding:30px 35px;
    border-radius:10px;
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
}

.title {
    font-size:26px;
    font-weight:600;
}

.desc {
    color:#5f6368;
    margin-bottom:20px;
}

.stButton>button{
    background:#673ab7;
    color:white;
    border:none;
    border-radius:6px;
    height:45px;
    width:140px;
}

.footer{
    text-align:center;
    color:gray;
    font-size:13px;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# =====================
# FORM
# =====================

st.markdown('<div class="header"></div>', unsafe_allow_html=True)

with st.container():

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="title">Survey Kepuasan MBG</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="desc">Silakan isi komentar anda mengenai layanan MBG.</div>',
        unsafe_allow_html=True
    )

    nama = st.text_input("Nama")

    sekolah = st.text_input("Sekolah")

    kelas = st.text_input("Kelas")

    komentar = st.text_area(
        "Komentar"
    )

    if st.button("Kirim"):

        if nama=="" or sekolah=="" or kelas=="" or komentar=="":

            st.warning("Harap isi semua data")

        else:

            db = koneksi()
            cursor = db.cursor()

            # simpan responden
            cursor.execute("""

            INSERT INTO responden
            (nama,sekolah,kelas)

            VALUES (%s,%s,%s)

            """,(nama,sekolah,kelas))

            id_responden = cursor.lastrowid

            # simpan komentar
            cursor.execute("""

            INSERT INTO komentar
            (id_responden,isi_komentar)

            VALUES (%s,%s)

            """,(id_responden,komentar))

            db.commit()

            st.success(
                "Terima kasih, respon anda berhasil dikirim"
            )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================
# FOOTER
# =====================

st.markdown("""

<div class="footer">

© 2026 MBG

</div>

""", unsafe_allow_html=True)