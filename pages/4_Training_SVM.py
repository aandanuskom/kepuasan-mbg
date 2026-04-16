import streamlit as st
import pandas as pd
import re
import joblib
import os
import sys

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import precision_score, recall_score

# =====================
# SESSION LOGIN
# =====================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.get("login"):
    st.switch_page("pages/login_admin.py")
    st.stop()

# =====================
# STYLE SIDEBAR
# =====================
st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
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
# DATABASE
# =====================
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from config.koneksi import koneksi

db = koneksi()
cursor = db.cursor()

st.set_page_config(layout="wide")

st.title("Training Model SVM")
st.caption("Pipeline lengkap: TF-IDF + SVM + Evaluasi + Logging")

# =====================
# LOAD DATA TRAINING
# =====================
df = pd.read_sql("""
SELECT komentar, label
FROM dataset_training
""", db)

# =====================
# CLEANING TEXT
# =====================
def clean_text(text):
    text = text.lower()

    # =====================
    # NORMALISASI NEGASI
    # =====================
    text = text.replace("tidak ", "tidak_")
    text = text.replace("kurang ", "kurang_")
    text = text.replace("gak ", "tidak_")
    text = text.replace("ga ", "tidak_")

    # =====================
    # NEGATIF
    # =====================
    text = text.replace("tidak_enak", "tidak_puas")
    text = text.replace("kurang_enak", "tidak_puas")

    # =====================
    # POSITIF (WAJIB SAMA DENGAN PROSES)
    # =====================
    text = text.replace("suka", "puas")
    text = text.replace("bagus", "puas")
    text = text.replace("enak", "puas")
    text = text.replace("mantap", "puas")
    text = text.replace("bermanfaat", "puas")
    text = text.replace("membantu", "puas")
    text = text.replace("bersyukur", "puas")
    text = text.replace("memuaskan", "puas")

    # =====================
    # BERSIHKAN
    # =====================
    text = re.sub(r'[^a-zA-Z_ ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

if len(df) == 0:
    st.warning("Data training belum tersedia")

else:

    st.subheader("DATA TRAINING")
    df.index = range(1, len(df)+1)
    st.dataframe(df, use_container_width=True)

    # =====================
    # PREPROCESSING
    # =====================
    st.subheader("PREPROCESSING")

    df["clean"] = df["komentar"].apply(clean_text)
    st.dataframe(df[["komentar", "clean"]].head())

    st.divider()

    # =====================
    # SPLIT DATA
    # =====================
    st.subheader("SPLIT DATA")

    test_size = st.slider("Persentase data testing", 10, 40, 20)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"],
        df["label"],
        test_size=test_size/100,
        random_state=42,
        stratify=df["label"]
    )

    st.write(f"Training: {len(X_train)} data")
    st.write(f"Testing: {len(X_test)} data")

    st.divider()

    # =====================
    # TF-IDF VECTOR
    # =====================
    st.subheader("TF-IDF Vectorization")

    st.write("""
    Tahapan TF-IDF:
    1. Mengumpulkan data teks hasil preprocessing
    2. Mengubah teks menjadi vektor numerik
    3. Menghitung bobot kata berdasarkan frekuensi (TF-IDF)
    4. Menghasilkan fitur untuk model SVM
    """)

    tfidf = TfidfVectorizer(
        ngram_range=(1,2),
        min_df=2,
        max_df=0.9,
        stop_words=[
            "yang","dan","di","ke","dari","untuk","dengan","pada",
            "ini","itu","saya","kami","anda","adalah","itu","ini",
            "karena","jadi","agar","dengan","sebagai","oleh"
        ]
    )

    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    st.success(f"""
    TF-IDF berhasil dibentuk:
    - Data training: {X_train_tfidf.shape[0]}
    - Jumlah fitur unik: {X_train_tfidf.shape[1]}
    """)

    # =====================
    # SVM TRAINING
    # =====================
    st.subheader("SVM TRAINING")

    if st.button("Mulai Training SVM"):

        model = SVC(kernel="linear", C=2.0)

        model.fit(X_train_tfidf, y_train)

        st.success("Model berhasil dilatih")

        st.divider()

        # =====================
        # TESTING (PREDIKSI)
        # =====================
        st.subheader("TESTING (PREDIKSI)")

        y_pred = model.predict(X_test_tfidf)

        acc = accuracy_score(y_test, y_pred)

        prec = precision_score(y_test, y_pred, average="macro")
        rec = recall_score(y_test, y_pred, average="macro")

        st.write(pd.DataFrame({
            "Actual": y_test.values,
            "Predicted": y_pred
        }).head())

        st.divider()

        # =====================
        # HITUNG AKURASI
        # =====================
        st.subheader("AKURASI MODEL")

        acc = accuracy_score(y_test, y_pred)

        st.metric("Accuracy", f"{round(acc*100,2)} %")

        # =====================
        # CLASSIFICATION REPORT
        # =====================
        st.subheader("CLASSIFICATION REPORT")

        report = classification_report(
            y_test,
            y_pred,
            output_dict=True
        )

        st.dataframe(pd.DataFrame(report).transpose())

        # =====================
        # CONFUSION MATRIX
        # =====================
        st.subheader("CONFUSION MATRIX")

        cm = confusion_matrix(y_test, y_pred)
        st.dataframe(pd.DataFrame(cm))

        st.divider()

        # =====================
        # SIMPAN MODEL
        # =====================
        os.makedirs("model", exist_ok=True)

        joblib.dump(model, "model/svm_model.joblib")
        joblib.dump(tfidf, "model/tfidf.joblib")

        jumlah_data = len(df)

        # =====================
        # SIMPAN LOG TRAINING
        # =====================
        cursor.execute("""
        INSERT INTO log_training
        (jumlah_data, akurasi, precision_score, recall_score, tanggal)
        VALUES (%s, %s, %s, %s, NOW())
        """, (
            int(jumlah_data),
            float(acc),
            float(prec),
            float(rec)
        ))

        db.commit()

        st.success("Model & log training berhasil disimpan")
