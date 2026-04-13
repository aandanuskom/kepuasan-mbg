import streamlit as st
import numpy as np
import pandas as pd
import pickle
import sys
import os
import joblib

def clean_text(text):
    text = text.lower()

    # =====================
    # HANDLE NEGASI (WAJIB)
    # =====================
    text = text.replace("kurang enak", "tidak_puas")
    text = text.replace("tidak enak", "tidak_puas")
    text = text.replace("ga enak", "tidak_puas")
    text = text.replace("gak enak", "tidak_puas")

    return text

from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# =====================
# SESSION LOGIN
# =====================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.get("login"):

    st.switch_page("pages/login_admin.py")
    st.stop()

if "hasil_df" not in st.session_state:
    st.session_state.hasil_df = None

# =====================
# SIDEBAR CUSTOM
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

# if st.sidebar.button("📈 Hasil Prediksi"):
#     st.switch_page("pages/5_Hasil_Prediksi.py")

if st.sidebar.button("💬 Data Komentar"):
    st.switch_page("pages/6_Data_Komentar.py")

if st.sidebar.button("⚙ Proses SVM Komentar"):
    st.switch_page("pages/7_Proses_Sentimen.py")

if st.sidebar.button("📑 Laporan"):
    st.switch_page("pages/78_Laporan.py")

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
# LOAD MODEL SVM
# =====================
try:

    model = joblib.load("model/svm_model.joblib")

    vectorizer = joblib.load("model/tfidf.joblib")

except:

    st.error("Model SVM belum tersedia, silakan training terlebih dahulu")

    st.stop()

# =====================
# AMBIL DATA KOMENTAR
# =====================
df = pd.read_sql("""

SELECT

k.id_komentar,
r.nama,
k.isi_komentar

FROM komentar k

JOIN responden r
ON k.id_responden = r.id_responden

ORDER BY k.id_komentar ASC

""", db)

st.title("Proses Sentimen SVM")
st.caption("Klasifikasi komentar responden menjadi PUAS / NETRAL / TIDAK PUAS")

st.metric("Jumlah komentar",len(df))

st.divider()

# =====================
# TOMBOL PROSES
# =====================
if st.button("Proses Sentimen"):

    if len(df) == 0:
        st.warning("Belum ada komentar")

    else:
        # teks asli (tidak diubah)
        teks = df["isi_komentar"]

        # teks untuk model (sudah dibersihkan)
        teks_model = teks.apply(clean_text)

        # proses ke TF-IDF
        X = vectorizer.transform(teks_model)
        prediksi = model.predict(X)
        confidence = model.decision_function(X)

        confidence_score = np.max(confidence, axis=1) if len(confidence.shape) > 1 else confidence

        # SIMPAN KE DATABASE
        for i in range(len(df)):

            id_k = int(df.iloc[i]["id_komentar"])
            hasil = str(prediksi[i])
            nilai = float(confidence_score[i])

            cursor.execute("""
            INSERT INTO hasil_sentimen
            (id_komentar, hasil, confidence)
            VALUES(%s,%s,%s)
            ON DUPLICATE KEY UPDATE
            hasil=%s,
            confidence=%s
            """, (id_k, hasil, nilai, hasil, nilai))

        db.commit()

        st.success("Sentimen berhasil diproses")

        # SIMPAN KE SESSION STATE
        st.session_state.hasil_df = pd.DataFrame({
            "No": range(1, len(df)+1),
            "Nama": df["nama"],
            "Komentar": teks,
            "Hasil": prediksi,
            "Confidence": confidence_score
        }).reset_index(drop=True)

# =====================
# TAMPILKAN HASIL
# =====================
if st.session_state.get("hasil_df") is not None:

    st.subheader("Hasil Prediksi")
    st.dataframe(st.session_state.hasil_df, use_container_width=True, hide_index=True)

# =====================
# EXPORT EXCEL
# =====================
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Hasil Sentimen")
    return output.getvalue()

if st.session_state.get("hasil_df") is not None:

    st.download_button(
        "⬇ Download Excel",
        data=to_excel(st.session_state.hasil_df),
        file_name="hasil_sentimen.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# =====================
# EXPORT PDF
# =====================
def to_pdf(df):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer)

    data = [df.columns.tolist()] + df.values.tolist()

    table = Table(data)

    style = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ])

    table.setStyle(style)
    pdf.build([table])

    buffer.seek(0)
    return buffer

if st.session_state.get("hasil_df") is not None:

    st.download_button(
        "⬇ Download PDF",
        data=to_pdf(st.session_state.hasil_df),
        file_name="hasil_sentimen.pdf",
        mime="application/pdf"
    )

