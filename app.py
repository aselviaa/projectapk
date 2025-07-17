import streamlit as st

# Database produk gula (gram per porsi)
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

# Simpan daftar konsumsi sementara
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

st.title("🍬 SweetTracker")
st.subheader("Penghitung Kadar Gula Harian")

# Form input
with st.form("form_produk"):
    produk = st.selectbox("Pilih Produk", list(produk_gula.keys()))
    jumlah = st.number_input("Jumlah Porsi", min_value=1, value=1)
    submitted = st.form_submit_button("Tambah")

    if submitted:
        total = produk_gula[produk] * jumlah
        st.session_state.riwayat.append((produk, jumlah, total))
        st.success(f"{jumlah} porsi {produk} = {total} gram gula")

# Tampilkan riwayat konsumsi
if st.session_state.riwayat:
    st.subheader("📋 Riwayat Konsumsi Hari Ini")
    total_gula = 0.0
    for i, (produk, jumlah, gula) in enumerate(st.session_state.riwayat, start=1):
        st.write(f"{i}. {jumlah} porsi {produk} = {gula} gram gula")
        total_gula += gula
    st.info(f"💡 Total Gula Hari Ini: **{total_gula} gram**")

# Reset tombol
if st.button("🔄 Reset Data"):
    st.session_state.riwayat = []
    st.warning("Riwayat konsumsi telah dihapus.")
