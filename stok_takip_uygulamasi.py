# -*- coding: utf-8 -*- 
import streamlit as st
import pandas as pd
import copy

# Sample data for products and their sub-parts
product_structure = {
    "044921F": {"30302475": 1, "33005127": 1, "32103174001": 1, "32001125": 1, "30705054": 1, "33005128": 1, "30705022": 1, "20501005001": 1, "30802023": 1, "32003631": 1, "37023078": 0.01, "37021056": 1},
    "044728F": {"30302475": 1, "30301874005": 1, "33005127": 1, "32001109": 1, "30705054": 1, "33005128": 1, "30705022": 1, "30603125": 1, "32103104001": 1, "30403910": 1, "30802023": 1, "20501005001": 1, "32003631": 1, "37021028": 3.571, "37023077": 0.02},
    "01844013F": {"30505004": 2, "32002961": 1, "30403494": 1, "33206006": 1, "33005017": 1, "30603116": 4, "30603097": 2, "32001153": 1, "33003046": 1, "33206005": 1, "32103040": 2, "32003310": 1, "32003311": 1, "32103039": 1, "30802028": 1, "32003312": 1, "33005271": 1, "32103041": 1, "30603116001": 1, "37021001": 0.031, "37021002": 0.171, "37021044": 0.992, "37023138": 0.0555, "37023102": 0.0555, "37023077": 0.0555},
    "00100011F": {"20501015": 1, "30302007": 1, "32005029": 1, "30505004": 2, "32005030": 1, "30302017": 1, "30403001": 1, "40020011": 1, "30603006": 1, "37023077": 0.02, "37021018": 5.405, "30802003": 1, "30802021": 1, "30603002": 1},
    "044385F": {"30603189": 2, "30603190": 1, "32001097": 1, "32001096": 1, "37023018": 1, "37021047": 1}
}

# Initial stock levels
initial_sub_parts_stock = {...}  # (senin tanımladığın uzun dict burada kalabilir)

# Initialize session state
if "sub_parts_stock" not in st.session_state:
    st.session_state.sub_parts_stock = copy.deepcopy(initial_sub_parts_stock)

# Sidebar page selector
st.sidebar.title("Sayfa Seçimi")
page = st.sidebar.radio("Gitmek istediğiniz sayfayi seçin:", ["Urun Girisi", "Alt Parca Stoklari"])

# Product Entry Page
if page == "Urun Girisi":
    st.title("Ürün Girişi ve Stok Güncelleme")

    st.write("Lütfen ürün miktarlarini girin:")
    product_quantities = {}
    for product in product_structure.keys():
        qty = st.number_input(f"{product} miktari", min_value=0, step=1, key=product)
        product_quantities[product] = qty

    if st.button("Stoklari Güncelle"):
        for product, qty in product_quantities.items():
            for part, amount_per_unit in product_structure[product].items():
                total_deduction = qty * amount_per_unit
                st.session_state.sub_parts_stock[part]["stok"] -= total_deduction
        st.success("Stoklar başariyla güncellendi.")

# Sub-Part Stocks Page
elif page == "Alt Parca Stoklari":
    st.title("Alt Parça Stoklari")

    st.write("Mevcut alt parça stok durumu:")
    data = []
    for part, info in st.session_state.sub_parts_stock.items():
        status = "Yeterli" if info["stok"] >= info["kritik"] else "Kritik"
        data.append([part, info["stok"], info["kritik"], status])

    df = pd.DataFrame(data, columns=["Parça", "Mevcut Stok", "Kritik Seviye", "Durum"])
    st.dataframe(df)

    critical_parts = [row[0] for row in data if row[3] == "Kritik"]
    if critical_parts:
        st.warning(f"Kritik seviyenin altina düşen parçalar: {', '.join(critical_parts)}")
