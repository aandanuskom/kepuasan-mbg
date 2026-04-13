import streamlit as st
import hashlib
from config.koneksi import koneksi

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Admin Login",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================
# BACKGROUND MODERN
# =====================
st.markdown("""
<style>

/* BACKGROUND GRADIENT */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* REMOVE WHITE MAIN */
.main {
    background: transparent;
}

/* HIDE SIDEBAR */
[data-testid="stSidebar"] {
    display: none;
}

/* CENTER CARD */
.block-container {
    padding-top: 8vh;
}

/* LOGIN CARD GLASS */
.card {
    max-width: 420px;
    margin: auto;
    padding: 35px;
    border-radius: 20px;

    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);

    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);

    animation: fadeIn 1s ease-in-out;
}

/* FADE ANIMATION */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* SHAKE ERROR */
@keyframes shake {
    0% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    50% { transform: translateX(5px); }
    75% { transform: translateX(-5px); }
    100% { transform: translateX(0); }
}

.shake {
    animation: shake 0.4s;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    color: white;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 14px;
    color: #d1d1d1;
    margin-bottom: 20px;
}

/* INPUT */
input {
    border-radius: 10px !important;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px;
}

.stButton>button:hover {
    transform: scale(1.03);
}

/* LOGO */
.logo {
    text-align: center;
    font-size: 40px;
    margin-bottom: 10px;
}

/* RESPONSIVE */
@media screen and (max-width: 768px) {
    .card {
        width: 90%;
        padding: 25px;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================
# DB
# =====================
db = koneksi()
cursor = db.cursor()

# =====================
# HASH PASSWORD
# =====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================
# SESSION
# =====================
if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    st.switch_page("pages/1_Dashboard.py")
    st.stop()

# =====================
# CARD UI
# =====================
# st.markdown("<div class='card'>", unsafe_allow_html=True)

# LOGO + WELCOME TEXT
st.markdown("""
<div class="logo">🏦</div>
<div class="title">Welcome Back</div>
<div class="subtitle">Login Admin Sistem Analisis MBG</div>
""", unsafe_allow_html=True)

username = st.text_input("Username", placeholder="Masukkan username")
password = st.text_input("Password", type="password", placeholder="Masukkan password")

error_placeholder = st.empty()

if st.button("Login"):

    pwd = hash_password(password)

    cursor.execute("""
    SELECT *
    FROM admin
    WHERE username=%s
    AND password=%s
    """, (username, pwd))

    user = cursor.fetchone()

    if user:

        st.session_state.login = True
        st.session_state.username = username

        st.success("Login berhasil...")
        st.rerun()

    else:

        # SHAKE EFFECT
        st.markdown("""
        <script>
        document.querySelector('.card').classList.add('shake');
        setTimeout(() => {
            document.querySelector('.card').classList.remove('shake');
        }, 500);
        </script>
        """, unsafe_allow_html=True)

        error_placeholder.error("Username atau password salah")

st.markdown("</div>", unsafe_allow_html=True)