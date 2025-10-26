# -*- coding: utf-8 -*- 
import streamlit as st
import pandas as pd
import copy

# --------------------------
# Giriş Bilgileri
# --------------------------
USER_CREDENTIALS = {
    "aster1": "1234",
    "selim61": "6161", 
    "mt61": "6116"  
}

# --------------------------
# Ürün Yapısı
# --------------------------
product_structure = {
    "044921F": {
        "30302475": 1, "33005127": 1, "32103174001": 1, "32001125": 1,
        "30705054": 1, "33005128": 1, "30705022": 1, "20501005001": 1,
        "30802023": 1, "32003631": 1, "37023078": 0.01, "37021056": 1
    },
    "044728F": {
        "30302475": 1, "30301874005": 1, "33005127": 1, "32001109": 1,
        "30705054": 1, "33005128": 1, "30705022": 1, "30603125": 1,
        "32103104001": 1, "30403910": 1, "30802023": 1, "20501005001": 1,
        "32003631": 1, "37021028": 3.571, "37023077": 0.02
    },
    "01844013F": {
        "30505004": 2, "32002961": 1, "30403494": 1, "33206006": 1,
        "33005017": 1, "30603116": 4, "30603097": 2, "32001153": 1,
        "33003046": 1, "33206005": 1, "32103040": 2, "32003310": 1,
        "32003311": 1, "32103039": 1, "30802028": 1, "32003312": 1,
        "33005271": 1, "32103041": 1, "30603116001": 1, "37021001": 0.031,
        "37021002": 0.171, "37021044": 0.992, "37023138": 0.0555,
        "37023102": 0.0555, "37023077": 0.0555
    },
    "00100011F": {
        "20501015": 1, "30302007": 1, "32005029": 1, "30505004": 2,
        "32005030": 1, "30302017": 1, "30403001": 1, "40020011": 1,
        "30603006": 1, "37023077": 0.02, "37021018": 5.405,
        "30802003": 1, "30802021": 1, "30603002": 1
    },
    "044385F": {
        "30603189": 2, "30603190": 1, "32001097": 1, "32001096": 1,
        "37023018": 1, "37021047": 1
    }
}

# --------------------------
# Başlangıç Stok Verisi
# --------------------------
initial_sub_parts_stock = {k: {"stok": 10000, "kritik": 1000} for k in {
    "30302475","33005127","32103174001","32001125","30705054","33005128","30705022",
    "20501005001","30802023","32003631","37023078","37021056","30301874005","32001109",
    "30603125","32103104001","30403910","37021028","37023077","30505004","32002961",
    "30403494","33206006","33005017","30603116","30603097","32001153","33003046",
    "33206005","32103040","32003310","32003311","32103039","30802028","32003312",
    "33005271","32103041","30603116001","37021001","37021002","37021044","37023138",
    "37023102","20501015","30302007","32005029","32005030","30302017","30403001",
    "40020011","30603006","37021018","30802003","30802021","30603002","30603189",
    "30603190","32001097","32001096","37023018","37021047"
}}

# --------------------------
# Session Initialization
# --------------------------
if "sub_parts_stock" not in st.session_state:
    st.session_state.sub_parts_stock = copy.deepcopy(initial_sub_parts_stock)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --------------------------
# Login Page
# --------------------------
def login_page():
    st.title("🔐 Stok Takip Sistemi Girişi")

    username = st.text_input("Kullanıcı Adı:")
    password = st.text_input("Şifre:", type="password")

    if st.button("Giriş Yap"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Hoşgeldin, {username} 👋")
            st.rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")

# --------------------------
# Logout Button
# --------------------------
def logout_button():
    st.sidebar.write(f"👤 Giriş yapan: **{st.session_state.username}**")
    if st.sidebar.button("🚪 Çıkış Yap"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# --------------------------
# Main Pages (After Login)
# --------------------------
def urun_girisi_page():
    st.title("📦 Ürün Girişi ve Stok Güncelleme")

    product_quantities = {}
    for product in product_structure.keys():
        qty = st.number_input(f"{product} miktarı", min_value=0, step=1, key=f"qty_{product}")
        product_quantities[product] = qty

    if st.button("Stokları Güncelle"):
        for product, qty in product_quantities.items():
            for part, amount_per_unit in product_structure[product].items():
                total_deduction = qty * amount_per_unit
                st.session_state.sub_parts_stock[part]["stok"] -= total_deduction
        st.success("✅ Stoklar başarıyla güncellendi!")

def alt_parca_stoklari_page():
    st.title("⚙️ Alt Parça Stokları")

    data = []
    for part, info in st.session_state.sub_parts_stock.items():
        durum = "Yeterli" if info["stok"] >= info["kritik"] else "Kritik"
        data.append([part, info["stok"], info["kritik"], durum])

    df = pd.DataFrame(data, columns=["Parça", "Mevcut Stok", "Kritik Seviye", "Durum"])
    st.dataframe(df)

    kritik = [row[0] for row in data if row[3] == "Kritik"]
    if kritik:
        st.warning(f"Kritik seviyede parçalar: {', '.join(kritik)}")

# --------------------------
# App Logic
# --------------------------
if not st.session_state.logged_in:
    login_page()
else:
    logout_button()

    page = st.sidebar.radio("Sayfa Seç:", ["Urun Girisi", "Alt Parca Stoklari"])
    if page == "Urun Girisi":
        urun_girisi_page()
    elif page == "Alt Parca Stoklari":
        alt_parca_stoklari_page()
