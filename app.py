import streamlit as st

# =======================
# GLUCOTRACK: SWEET TRACKER
# =======================

# Warna utama biru
PRIMARY_COLOR = "#007BFF"

# Database produk dan kadar gula per porsi (gram)
produk_gula = {
    "Teh Botol": 18.0,
    "Coca Cola": 35.0,
    "Oreo": 8.0,
    "Aqua": 0.0,
    "Fanta": 36.0,
    "Good Day": 17.0,
    "Indomilk": 12.0,
    "Nutrisari": 20.0,
    "Ultra Milk": 10.5,
    "Sprite": 33.0
}

# Inisialisasi session state
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "batas_gula" not in st.session_state:
    st.session_state.batas_gula = 50  # default batas

# =======================
# TAMPILAN AWAL – STYLING
# =======================

# Custom CSS biru
st.markdown(f"""
    <style>
    .main-title {{
        text-align: center;
        color: {PRIMARY_COLOR};
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 0;
    }}
    .sub-title {{
        text-align: center;
        color: #555;
        font-size: 20px;
        margin-top: 0;
    }}
    .stButton > button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# Judul Aplikasi
st.markdown("<div class='main-title'>🩸 GlucoTrack</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Pantau Kadar Gula Harian Anda</div>", unsafe_allow_html=True)
st.write("---")

# =======================
# SIDEBAR - PENGATURAN
# =======================

st.sidebar.header("⚙️ Pengaturan")
batas = st.sidebar.number_input(
    "Batas maksimum konsumsi gula harian (gram)",
    min_value=1,
    value=st.session_state.batas_gula,
    step=1
)
st.session_state.batas_gula = batas

# =======================
# FORM INPUT PRODUK
# =======================
with st.form("form_produk"):
    st.subheader("➕ Tambah Konsumsi Gula")
    produk = st.selectbox("Pilih Produk", list(produk_gula.keys()))
    jumlah = st.number_input("Jumlah Porsi", min_value=1, value=1)
    submitted = st.form_submit_button("Tambah")

    if submitted:
        total = produk_gula[produk] * jumlah
        st.session_state.riwayat.append((produk, jumlah, total))
        st.success(f"{jumlah} porsi {produk} = {total} gram gula ditambahkan.")

# =======================
# RIWAYAT & NOTIFIKASI
# =======================

if st.session_state.riwayat:
    st.subheader("📋 Riwayat Konsumsi Hari Ini")
    total_gula = sum(item[2] for item in st.session_state.riwayat)

    for i, (produk, jumlah, gula) in enumerate(st.session_state.riwayat, start=1):
        st.write(f"{i}. {jumlah} porsi {produk} = {gula} gram")

    if total_gula > st.session_state.batas_gula:
        st.error(f"⚠️ Total konsumsi {total_gula:.1f} gram melebihi batas {st.session_state.batas_gula} gram!")
    else:
        st.info(f"💡 Total Gula Hari Ini: {total_gula:.1f} gram dari {st.session_state.batas_gula} gram.")

# =======================
# TOMBOL RESET
# =======================

if st.button("🔄 Reset Data"):
    st.session_state.riwayat = []
    st.warning("Riwayat konsumsi telah dihapus.")
