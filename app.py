import streamlit as st

# =======================
# GLUCOTRACK: SWEET TRACKER
# =======================

# Database produk dan kadar gula per porsi (gram)
produk_gula = {
    "Teh Botol": 18.0, "Coca Cola": 35.0, "Oreo": 8.0, "Aqua": 0.0,
    "Fanta": 36.0, "Good Day": 17.0, "Indomilk": 12.0, "Nutrisari": 20.0,
    "Ultra Milk": 10.5, "Sprite": 33.0,
    "Milo": 12.0, "Susu Kental Manis": 20.0, "Yakult": 11.0, "Chocolatos": 9.0,
    "Pocari Sweat": 14.0, "Floridina": 25.0, "Green Tea Botol": 22.0,
    "Red Bull": 27.0, "Kratingdaeng": 26.0, "Buavita": 19.0,
    "Sari Kacang Hijau": 16.0, "Minute Maid": 21.0, "Frisian Flag": 13.0,
    "Nestle Bear Brand": 10.0, "C1000": 18.0, "Soyjoy": 12.0, "Tebs": 32.0,
    "Pepsi": 34.0, "Fruit Tea": 30.0, "Mizone": 15.0, "Isoplus": 12.0,
    "Le Minerale Sparkling": 1.0, "YOU C1000": 22.0, "Snickers": 20.0,
    "SilverQueen": 25.0, "Chitato": 3.0, "Taro Net": 4.0, "Roti Sari Roti": 9.0,
    "BreadTalk": 12.0, "Yupi": 13.0, "Permen Fox": 10.0, "Kopi Kapal Api": 6.0,
    "Kopi ABC": 8.0, "Nutrijell": 5.0, "Puding Instan": 7.0, "Dancow": 11.0,
    "Ovaltine": 10.0, "Roti Coklat": 13.0, "Kue Lapis": 14.0, "Donat": 15.0
}

# Inisialisasi session state
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "batas_gula" not in st.session_state:
    st.session_state.batas_gula = 50

# =======================
# HEADER APLIKASI
# =======================
st.markdown("""
    <div style='text-align: center; padding: 10px 0'>
        <h1 style='color: #4CAF50;'>🩸 GlucoTrack</h1>
        <h4 style='color: gray;'>Aplikasi Pemantau Konsumsi Gula Harian</h4>
    </div>
""", unsafe_allow_html=True)

# =======================
# SIDEBAR: PENGATURAN
# =======================
st.sidebar.header("⚙️ Pengaturan")

usia = st.sidebar.number_input("Masukkan usia Anda", min_value=1, max_value=120, value=25)

# Ceklis untuk mengikuti WHO
pakai_who = st.sidebar.checkbox("Gunakan batas sehat WHO (5%)", value=True)

# Fungsi batas gula sesuai usia
def hitung_batas(usia, sehat=True):
    if sehat:
        if usia <= 6:
            return 15
        elif usia <= 10:
            return 20
        elif usia <= 17:
            return 25
        elif usia <= 59:
            return 25
        else:
            return 25
    else:
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

# Atur batas gula
batas_default = hitung_batas(usia, sehat=pakai_who)
batas = st.sidebar.number_input(
    "Batas konsumsi gula harian (gram)",
    min_value=1,
    value=batas_default,
    step=1
)
st.session_state.batas_gula = batas

# =======================
# FORM INPUT
# =======================
with st.form("form_produk"):
    st.subheader("➕ Tambahkan Konsumsi Gula")
    produk = st.selectbox("Pilih Produk", list(produk_gula.keys()))
    jumlah = st.number_input("Jumlah Porsi", min_value=1, value=1)
    submitted = st.form_submit_button("Tambah")

    if submitted:
        total = produk_gula[produk] * jumlah
        st.session_state.riwayat.append((produk, jumlah, total))
        st.success(f"{jumlah} porsi {produk} = {total:.1f} gram gula ditambahkan.")

# =======================
# TAMPILKAN RIWAYAT
# =======================
if st.session_state.riwayat:
    st.subheader("📋 Riwayat Konsumsi Hari Ini")
    total_gula = sum(item[2] for item in st.session_state.riwayat)

    for i, (produk, jumlah, gula) in enumerate(st.session_state.riwayat, start=1):
        st.write(f"{i}. {jumlah} porsi {produk} = {gula:.1f} gram gula")

    # Notifikasi batas
    if total_gula > st.session_state.batas_gula:
        st.error(f"⚠️ Total konsumsi {total_gula:.1f} gram telah melebihi batas {st.session_state.batas_gula} gram!")
        st.markdown("**🚫 Keterangan:** Konsumsi gula Anda hari ini **tidak sehat**.")
        st.markdown("**💡 Saran:** Kurangi minuman manis dan perbanyak konsumsi air putih serta makanan segar.")
    else:
        st.info(f"✅ Total Gula Hari Ini: {total_gula:.1f} gram dari batas {st.session_state.batas_gula} gram.")
        st.markdown("**🟢 Keterangan:** Konsumsi gula Anda hari ini masih **dalam batas sehat**.")

# Tombol reset
if st.button("🔄 Reset Data"):
    st.session_state.riwayat = []
    st.warning("Riwayat konsumsi telah dihapus.")
