import streamlit as st

# ===========================
# GLUCOTRACK: SWEET TRACKER
# ===========================

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
    "Sprite": 33.0,
    "Milo": 12.0,
    "Yakult": 10.0,
    "Fruit Tea": 24.0,
    "Pocari Sweat": 6.0,
    "Susu Kental Manis": 21.0,
    "Kratingdaeng": 27.0,
    "Red Bull": 28.0,
    "Floridina": 18.0,
    "Pulpy Orange": 21.0,
    "Minute Maid": 25.0,
    "You C 1000": 15.0,
    "Bear Brand": 7.0,
    "Cap Panda": 20.0,
    "Marimas": 22.0,
    "Es Teh Manis": 20.0,
    "Kopi Gula Aren": 19.0,
    "Matcha Latte": 23.0,
    "Pop Ice": 30.0,
    "Coklat Dingin": 26.0,
    "Chocolatos Drink": 14.0,
    "Kapal Api Sachet": 8.0,
    "ABC Susu": 12.0,
    "Teh Kotak": 19.0,
    "Mizone": 9.0,
    "Buavita": 20.0,
    "Nutriboost": 22.0,
    "Green Tea Botol": 15.0,
    "Jus Apel": 24.0,
    "Jus Mangga": 28.0,
    "Jus Jambu": 27.0,
    "Rasa Anggur": 26.0,
    "Le Minerale": 0.0,
    "Soda Gembira": 40.0,
    "Fruittea Blackcurrant": 25.0,
    "Frozz Tea": 18.0,
    "Kopiko 78": 22.0,
    "Cimory Yogurt Drink": 10.0,
    "Energen": 13.0,
    "Dancow Sachet": 11.0,
    "Susu Jahe Instan": 15.0,
    "Cereal Drink": 14.0
}

# ===========================
# SESSION STATE INISIALISASI
# ===========================

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "batas_gula" not in st.session_state:
    st.session_state.batas_gula = 50  # default

# ===========================
# HEADER APLIKASI
# ===========================

st.markdown(
    """
    <div style='text-align: center; padding: 10px 0'>
        <h1 style='color: #4CAF50;'>🩸 GlucoTrack</h1>
        <h4 style='color: gray;'>Aplikasi Pemantau Konsumsi Gula Harian</h4>
    </div>
    """, unsafe_allow_html=True
)

# ===========================
# SIDEBAR PENGATURAN
# ===========================

st.sidebar.header("⚙️ Pengaturan")

usia = st.sidebar.number_input("Masukkan Usia Anda", min_value=1, max_value=120, value=25)

def hitung_batas_usia(usia):
    if usia <= 6:
        return 19
    elif usia <= 10:
        return 24
    elif usia <= 17:
        return 30
    elif usia <= 59:
        return 50
    else:
        return 40

batas_default = hitung_batas_usia(usia)

# Input batas (bisa diganti manual)
batas = st.sidebar.number_input(
    "Batas maksimum konsumsi gula harian (gram)",
    min_value=1,
    value=batas_default,
    step=1
)

st.session_state.batas_gula = batas

# ===========================
# FORM INPUT KONSUMSI
# ===========================

with st.form("form_produk"):
    st.subheader("➕ Tambahkan Konsumsi Gula")
    produk = st.selectbox("Pilih Produk", sorted(produk_gula.keys()))
    jumlah = st.number_input("Jumlah Porsi", min_value=1, value=1)
    submitted = st.form_submit_button("Tambah")

    if submitted:
        total = produk_gula[produk] * jumlah
        st.session_state.riwayat.append((produk, jumlah, total))
        st.success(f"{jumlah} porsi {produk} = {total:.1f} gram gula ditambahkan.")

# ===========================
# RIWAYAT KONSUMSI
# ===========================

if st.session_state.riwayat:
    st.subheader("📋 Riwayat Konsumsi Hari Ini")
    total_gula = sum(item[2] for item in st.session_state.riwayat)

    for i, (produk, jumlah, gula) in enumerate(st.session_state.riwayat, start=1):
        st.write(f"{i}. {jumlah} porsi {produk} = {gula:.1f} gram gula")

    # Notifikasi batas konsumsi
    if total_gula > st.session_state.batas_gula:
        st.error(f"⚠️ Total konsumsi {total_gula:.1f} gram telah melebihi batas {st.session_state.batas_gula} gram!")
    else:
        st.info(f"💡 Total Gula Hari Ini: {total_gula:.1f} gram dari batas {st.session_state.batas_gula} gram berdasarkan usia {usia} tahun.")

# ===========================
# RESET DATA
# ===========================

if st.button("🔄 Reset Data"):
    st.session_state.riwayat = []
    st.warning("Riwayat konsumsi telah dihapus.")
