# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import copy
from datetime import datetime

# --------------------------
# Basit kullanıcı doğrulama
# --------------------------
USER_CREDENTIALS = {
    "aster1": "1212",
    "meg25": "2525",
    "mtc61": "6116",
    "shs61": "6161",
    "ıstu59": "5959"
}

# --------------------------
# Tam ürün -> alt parça yapısı 
# --------------------------
product_structure = {
    "044921F": {"30302475": 1,"30301874": 1, "32103174001": 1, "33005127": 1, "32001125": 1, "30705054": 1, "33005128": 1, "30705022": 1, "20501005001": 1, "30802023": 1, "32003631": 1, "37023078": 0.015, "37021056": 0.015 },
    "044728F": {"30302475": 1, "30301874005": 1, "33005127": 1, "32001109": 1, "30705054": 1, "33005128": 1, "30705022": 1, "30603125": 1, "321032104001": 1, "30403910": 1, "30802023": 1, "20501005001": 1, "32003631": 1, "37021028": 0.015, "37023077": 0.015},
    "044385F": {"30603189": 1, "30603190": 4, "32001096": 1, "32001097": 1,"37023018": 50, "37021026": 1},
    "0185205F": {"30505004": 2, "32002961": 1, "30403494": 1, "33206006": 1, "33005017": 1, "30603116": 4, "30603097": 2, "32001153": 1, "33003046": 1, "33206005": 1, "30301210": 1, "3003310": 1, "32003311": 1, "32001038": 1, "30802028": 1, "32003312": 1, "33005271": 1, "37023077": 0.056, "30603116001": 1, "37021001": 0.031, "37021002": 0.171, "37021044": 0.1, "37023102": 0.056, "37023138": 0.056 },
    "0185200F": {"30603116": 4, "30603097": 2, "32002961": 1, "33005271": 1, "30802028": 1, "32003312": 1, "33206005": 1, "30301210": 1, "32003310": 1, "32003311": 1, "32001038": 1, "33206006": 1, "33005017": 1, "32001153": 1, "33003046": 1, "30603116001": 1, "37021001": 0.046, "37021002": 0.171, "37023102": 0.056, "37023138": 0.056, "37023077": 0.056},
    "01844014F": {"30505004": 2, "32002961": 1, "30403494": 1, "33206006008": 1, "33005017": 1, "30603116": 4, "30603097": 2, "32001153": 1, "33003046": 1, "33206005": 1, "32103039": 1, "32003310": 1, "32003311": 1, "32103040": 2, "30802028": 1, "32003312": 1, "33005271": 1, "32103041": 1, "30603116001": 1, "37021001": 0.031, "37021002": 0.171, "37021044": 1, "37023102": 0.056, "37023138": 0.056, "37023077": 0.056},
    "01844013F": {"30505004": 2, "32002961": 1, "30403494": 1, "33206006": 1, "33005017": 1, "30603116": 4, "30603097": 2, "32001153": 1, "33003046": 1, "33206005": 1, "32103040": 2, "32003310": 1, "320033311": 1, "32103039": 1, "30802028": 1, "32003312": 1, "33005271": 1, "32103041": 1, "30603116001": 1, "37021001": 0.031, "37021002": 0.171, "37021044": 1, "37023138": 0.056, "37023102": 0.056, "37023077": 0.056},
    "00144044F": {"30302458": 1, "32005030": 1, "30302392": 1, "30403001": 1, "30802003": 1, "30802021": 1, "30603002": 1, "30505004": 2, "32005517": 1, "20501015": 1, "32005518": 1, "30302326": 1, "30302394": 1, "30802002": 1, "22001001": 1, "32005022": 1, "320021128": 1, "37023078": 0.005, "CY124": 2, "32003941349": 2, "30603006": 1, "400000144023": 1, "30401003": 1, "31301094": 1, "33003094": 1, "30705003": 1, "37023077": 0.02, "37021018": 5.405},
    "00100011F": {"30802003": 1, "30802021": 1, "30603002": 1, "20501015": 1, "30302007": 1, "32005029": 1, "30505004": 2, "32005030": 1, "30302017": 1, "30403001": 1, "32005518": 1, "30302025": 1, "30302011": 1, "30802002": 1, "22001001": 1, "32005022": 1, "37023078": 0.005, "30603006": 1, "37023077": 0.02, "37021018": 5.405},
    "20544001F": {"30302475": 1,"30301874": 1, "33005127": 1, "32001125": 1, "30705054": 1, "33005128": 1, "30705022": 1, "30603125": 1, "32103104001": 1, "30405807": 1, "30802023": 1, "205010005001": 1, "32003631": 1, "37021028": 3.571, "37023078": 0.0142, "32105504": 1 },
    "20544002F": {"30302475": 1,"30301874": 1, "32103569001": 1, "33005127": 1, "32001125": 1, "30705054": 1, "33005128": 1, "30705022": 1, "20501005001": 1, "30802023": 1, "32003631": 1, "37021028": 3.571, "37023078": 0.0142}
}
# --------------------------
# Başlangıç alt parça stokları
# --------------------------
initial_sub_parts_stock = {
    "30302475": {"stok": 0, "kritik": 6000},
    "30301874": {"stok": 0, "kritik": 4500},
    "32103174001": {"stok": 0, "kritik": 1500},
    "33005127": {"stok": 0, "kritik": 6000},
    "32001125": {"stok": 0, "kritik": 4500},
    "30705054": {"stok": 0, "kritik": 6000},
    "33005128": {"stok": 0, "kritik": 6000},
    "30705022": {"stok": 0, "kritik": 6000},
    "20501005001": {"stok": 0, "kritik": 6000},
    "30802023": {"stok": 0, "kritik": 6000},
    "32003631": {"stok": 0, "kritik": 6000},
    "37023078": {"stok": 0, "kritik": 5000},
    "37021056": {"stok": 0, "kritik": 1500},
    "30603189": {"stok": 0, "kritik": 1500},
    "30603190": {"stok": 0, "kritik": 2000},
    "32001097": {"stok": 0, "kritik": 1500},
    "32001096": {"stok": 0, "kritik": 1500},
    "37023018": {"stok": 0, "kritik": 1000},
    "37021026": {"stok": 0, "kritik": 2000},
    "30301874005": {"stok": 0, "kritik": 1500},
    "32001109": {"stok": 0, "kritik": 1500},
    "30603125": {"stok": 0, "kritik": 3000},
    "32103104001": {"stok": 0, "kritik": 3000},
    "30403910": {"stok": 0, "kritik": 1500},
    "37021028": {"stok": 0, "kritik": 6000},
    "3702377": {"stok": 0, "kritik": 7000},
    "30505004": {"stok": 0, "kritik": 10000},
    "32002961": {"stok": 0, "kritik": 6000},
    "30403494": {"stok": 0, "kritik": 4500},
    "33206006": {"stok": 0, "kritik": 4500},
    "33005017": {"stok": 0, "kritik": 6000},
    "30603116": {"stok": 0, "kritik": 8000},
    "30603097": {"stok": 0, "kritik": 8000},
    "32001153": {"stok": 0, "kritik": 6000},
    "33003046": {"stok": 0, "kritik": 6000},
    "33206005": {"stok": 0, "kritik": 6000},
    "32103040": {"stok": 0, "kritik": 4000},
    "32003310": {"stok": 0, "kritik": 6000},
    "32003311": {"stok": 0, "kritik": 6000},
    "32103039": {"stok": 0, "kritik": 3000},
    "30802028": {"stok": 0, "kritik": 6000},
    "32003312": {"stok": 0, "kritik": 6000},
    "33005271": {"stok": 0, "kritik": 6000},
    "32103041": {"stok": 0, "kritik": 3000},
    "30603116001": {"stok": 0, "kritik": 6000},
    "37021001": {"stok": 0, "kritik": 4000},
    "37021002": {"stok": 0, "kritik": 4000},
    "37021044": {"stok": 0, "kritik": 3000},
    "37023138": {"stok": 0, "kritik": 4000},
    "37023102": {"stok": 0, "kritik": 4000},
    "30802003": {"stok": 0, "kritik": 3000},
    "30802021": {"stok": 0, "kritik": 3000},
    "30603002": {"stok": 0, "kritik": 3000},
    "20501015": {"stok": 0, "kritik": 3000},
    "30302007": {"stok": 0, "kritik": 1500},
    "32005029": {"stok": 0, "kritik": 1500},
    "32005030": {"stok": 0, "kritik": 3000},
    "30302017": {"stok": 0, "kritik": 1500},
    "30403001": {"stok": 0, "kritik": 3000},
    "32005518": {"stok": 0, "kritik": 3000},
    "30302025": {"stok": 0, "kritik": 1500},
    "30302011": {"stok": 0, "kritik": 1500},
    "30802002": {"stok": 0, "kritik": 3000},
    "22001001": {"stok": 0, "kritik": 3000},
    "32005022": {"stok": 0, "kritik": 3000},
    "30603006": {"stok": 0, "kritik": 3000},
    "37021018": {"stok": 0, "kritik": 3000},
    "32103569001": {"stok": 0, "kritik": 1500},
    "332106006008": {"stok": 0, "kritik": 1500},
    "30301210": {"stok": 0, "kritik": 3000},
    "32001038": {"stok": 0, "kritik": 3000},
    "30405807": {"stok": 0, "kritik": 1500},
    "32105504": {"stok": 0, "kritik": 1500},
    "30302458": {"stok": 0, "kritik": 1500},
    "30302392": {"stok": 0, "kritik": 1500},
    "32005517": {"stok": 0, "kritik": 1500},
    "30302326": {"stok": 0, "kritik": 1500},
    "30302394": {"stok": 0, "kritik": 1500},
    "32002128": {"stok": 0, "kritik": 1500},
    "CY124": {"stok": 0, "kritik": 2000},
    "32003941349": {"stok": 0, "kritik": 2000},
    "400000144023": {"stok": 0, "kritik": 1500},
    "30401003": {"stok": 0, "kritik": 1500},
    "31301094": {"stok": 0, "kritik": 1500},
    "33003094": {"stok": 0, "kritik": 1500},
    "30705003": {"stok": 0, "kritik": 1500}
}

# --------------------------
# Session state init
# --------------------------
if "sub_parts_stock" not in st.session_state:
    st.session_state.sub_parts_stock = copy.deepcopy(initial_sub_parts_stock)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------
# Login UI
# --------------------------
def login_page():
    st.title("🔐 Stok Takip Sistemi Girişi")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Hatalı kullanıcı adı veya şifre")

# --------------------------
# Logout
# --------------------------
def logout_button():
    st.sidebar.write(f"👤 {st.session_state.username}")
    if st.sidebar.button("Çıkış Yap"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

# --------------------------
# Ürün Girişi
# --------------------------
def urun_girisi_page():
    st.title("📦 Ürün Girişi")

    product_quantities = {}
    for product in product_structure:
        product_quantities[product] = st.number_input(
            f"{product} miktarı", min_value=0, step=1, key=product
        )

    if st.button("Stokları Güncelle"):
        for product, qty in product_quantities.items():
            if qty <= 0:
                continue

            details = []
            for part, per_unit in product_structure[product].items():
                total = qty * per_unit
                before = st.session_state.sub_parts_stock[part]["stok"]
                st.session_state.sub_parts_stock[part]["stok"] = before - total
                details.append({
                    "part": part,
                    "deducted": total,
                    "before": before,
                    "after": before - total
                })

            st.session_state.history.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": st.session_state.username,
                "product": product,
                "qty": qty,
                "details": details
            })

        st.success("Stoklar güncellendi")

# --------------------------
# 🔥 Fire Girişi
# --------------------------
def fire_girisi_page():
    st.title("🔥 Fire Girişi")

    part_list = sorted(st.session_state.sub_parts_stock.keys())
    selected_part = st.selectbox("Alt Parça Kodu", part_list)
    fire_qty = st.number_input("Fire Adedi", min_value=0.0, step=1.0)

    if st.button("Fireyi Kaydet"):
        if fire_qty <= 0:
            st.warning("Fire miktarı 0'dan büyük olmalı")
            return

        current = st.session_state.sub_parts_stock[selected_part]["stok"]

        if current < fire_qty:
            st.error("Yetersiz stok")
            return

        st.session_state.sub_parts_stock[selected_part]["stok"] = current - fire_qty

        st.session_state.history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": st.session_state.username,
            "product": "FIRE",
            "qty": fire_qty,
            "details": [{
                "part": selected_part,
                "deducted": fire_qty,
                "before": current,
                "after": current - fire_qty
            }]
        })

        st.success("Fire kaydedildi")

# --------------------------
# Alt Parça Stokları
# --------------------------
def alt_parca_stoklari_page():
    st.title("⚙️ Alt Parça Stokları")

    df = pd.DataFrame([
        {"Parça": p, "Stok": v["stok"], "Kritik": v["kritik"]}
        for p, v in st.session_state.sub_parts_stock.items()
    ])

    edited_df = st.data_editor(df, use_container_width=True)

    if st.button("Kaydet"):
        for _, row in edited_df.iterrows():
            st.session_state.sub_parts_stock[row["Parça"]]["stok"] = float(row["Stok"])
            st.session_state.sub_parts_stock[row["Parça"]]["kritik"] = float(row["Kritik"])
        st.success("Kaydedildi")

# --------------------------
# Stok Geçmişi
# --------------------------
def stok_gecmisi_page():
    st.title("📜 Stok Geçmişi")

    if not st.session_state.history:
        st.info("Kayıt yok")
        return

    df = pd.DataFrame(st.session_state.history[::-1])
    st.dataframe(df, use_container_width=True)

# --------------------------
# Main
# --------------------------
if not st.session_state.logged_in:
    login_page()
else:
    logout_button()
    page = st.sidebar.radio(
        "Sayfa Seç",
        ["Urun Girisi", "Fire Girisi", "Alt Parca Stoklari", "Stok Gecmisi"]
    )

    if page == "Urun Girisi":
        urun_girisi_page()
    elif page == "Fire Girisi":
        fire_girisi_page()
    elif page == "Alt Parca Stoklari":
        alt_parca_stoklari_page()
    elif page == "Stok Gecmisi":
        stok_gecmisi_page()


