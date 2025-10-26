# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import copy

# ------------------------------
# --- ÖRNEK ÜRÜN YAPISI ---
# ------------------------------
product_structure = {
    "044921F": {"30302475": 1, "33005127": 1, "32103174001": 1, "32001125": 1, "30705054": 1, "33005128": 1,
                 "30705022": 1, "20501005001": 1, "30802023": 1, "32003631": 1, "37023078": 0.01, "37021056": 1},
    "044728F": {"30302475": 1, "30301874005": 1, "33005127": 1, "32001109": 1, "30705054": 1, "33005128": 1,
                 "30705022": 1, "30603125": 1, "32103104001": 1, "30403910": 1, "30802023": 1, "20501005001": 1,
                 "32003631": 1, "37021028": 3.571, "37023077": 0.02},
    "044385F": {"30603189": 2, "30603190": 1, "32001097": 1, "32001096": 1, "37023018": 1, "37021047": 1}
}

# ------------------------------
# --- BAŞLANGIÇ STOK VERİLERİ ---
# ------------------------------
initial_sub_parts_stock = {
    "30302475": {"stok": 10000, "kritik": 1000},
    "33005127": {"stok": 10000, "kritik": 1000},
    "32103174001": {"stok": 10000, "kritik": 1000},
    "32001125": {"stok": 10000, "kritik": 1000},
    "30705054": {"stok": 10000, "kritik": 1000},
    "33005128": {"stok": 10000, "kritik": 1000},
    "30705022": {"stok": 10000, "kritik": 1000},
    "20501005001": {"stok": 10000, "kritik": 1000},
    "30802023": {"stok": 10000, "kritik": 1000},
    "32003631": {"stok": 10000, "kritik": 1000},
    "37023078": {"stok": 10000, "kritik": 1000},
    "37021056": {"stok": 10000, "kritik": 1000},
}

# ------------------------------
# --- LOGIN ---
# ------------------------------
users = {"mtc61": "1234", "selim61": "6161"}  # basit kullanıcılar

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Stok Takip Girişi")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("Giriş başarılı ✅")
            st.rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre!")
    st.stop()

# ------------------------------
# --- STOK VERİLERİNİ YÜKLE ---
# ------------------------------
if "sub_parts_stock" not in st.session_state:
    st.session_state.sub_parts_stock = copy.deepcopy(initial_sub_parts_stock)

# ------------------------------
# --- SAYFA SEÇİMİ ---
# ------------------------------
st.sidebar.title("Sayfa Seçimi")
page = st.sidebar.radio("Gitmek istediğiniz sayfayı seçin:", ["Ürün Girişi", "Alt Parça Stokları"])

# ------------------------------
# --- ÜRÜN GİRİŞİ SAYFASI ---
# ------------------------------
if page == "Ürün Girişi":
    st.title("📦 Ürün Girişi ve Stok Güncelleme")

    product_quantities = {}
    for product in product_structure.keys():
        qty = st.number_input(f"{product} miktarı", min_value=0, step=1, key=product)
        product_quantities[product] = qty

    if st.button("Stokları Güncelle"):
        for product, qty in product_quantities.items():
            for part, amount_per_unit in product_structure[product].items():
                total_deduction = qty * amount_per_unit
                if part in st.session_state.sub_parts_stock:
                    st.session_state.sub_parts_stock[part]["stok"] -= total_deduction
        st.success("Stoklar başarıyla güncellendi ✅")

# ------------------------------
# --- ALT PARÇA STOKLARI SAYFASI ---
# ------------------------------
elif page == "Alt Parça Stokları":
    st.title("🧩 Alt Parça Stokları")

    df = pd.DataFrame([
        {"Parça": part, "Stok": info["stok"], "Kritik": info["kritik"]}
        for part, info in st.session_state.sub_parts_stock.items()
    ])

    st.write("Aşağıdaki tabloda stok değerlerini düzenleyebilirsiniz 👇")
    edited_df = st.data_editor(df, num_rows="dynamic")

    if st.button("Değişiklikleri Kaydet 💾"):
        for _, row in edited_df.iterrows():
            part = row["Parça"]
            if part in st.session_state.sub_parts_stock:
                st.session_state.sub_parts_stock[part]["stok"] = float(row["Stok"])
                st.session_state.sub_parts_stock[part]["kritik"] = float(row["Kritik"])
        st.success("Stoklar başarıyla güncellendi ✅")

    # Kritik uyarılar
    kritikler = [p for p, v in st.session_state.sub_parts_stock.items() if v["stok"] < v["kritik"]]
    if kritikler:
        st.warning(f"⚠️ Kritik seviyenin altına düşen parçalar: {', '.join(kritikler)}")
