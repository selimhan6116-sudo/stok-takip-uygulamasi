# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# --------------------------
# Supabase bağlantı
# --------------------------
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_SERVICE_KEY"]
)

# --------------------------
# Kullanıcılar
# --------------------------
USER_CREDENTIALS = {
    "aster1": "1212",
    "meg25": "2525",
    "mtc61": "6116",
    "shs61": "6161",
    "ıstu59": "5959"
}

# --------------------------
# Session init
# --------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --------------------------
# DB yardımcıları
# --------------------------
def load_stock():
    res = supabase.table("sub_parts_stock").select("*").execute()
    return {r["part_code"]: r for r in res.data}

def save_stock(stock_dict):
    rows = []
    for p, v in stock_dict.items():
        rows.append({
            "part_code": p,
            "stok": v["stok"],
            "kritik": v["kritik"]
        })
    supabase.table("sub_parts_stock").upsert(rows).execute()

def add_history(user, product, qty, details):
    supabase.table("stock_history").insert({
        "timestamp": datetime.now().isoformat(),
        "user_name": user,
        "product": product,
        "qty": qty,
        "details": details
    }).execute()

# --------------------------
# Login
# --------------------------
def login_page():
    st.title("🔐 Stok Takip Sistemi")
    u = st.text_input("Kullanıcı")
    p = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if USER_CREDENTIALS.get(u) == p:
            st.session_state.logged_in = True
            st.session_state.username = u
            st.rerun()
        else:
            st.error("Hatalı giriş")

# --------------------------
# Fire Girişi
# --------------------------
def fire_girisi_page():
    st.title("🔥 Fire Girişi")
    stock = load_stock()

    part = st.selectbox("Alt Parça", stock.keys())
    qty = st.number_input("Fire Adedi", min_value=0.0)

    if st.button("Kaydet"):
        if qty <= 0:
            st.warning("Miktar gir")
            return
        if stock[part]["stok"] < qty:
            st.error("Yetersiz stok")
            return

        before = stock[part]["stok"]
        stock[part]["stok"] -= qty
        save_stock(stock)

        add_history(
            st.session_state.username,
            "FIRE",
            qty,
            [{"part": part, "before": before, "after": stock[part]["stok"]}]
        )
        st.success("Fire kaydedildi")

# --------------------------
# Alt Parça Stokları
# --------------------------
def alt_parca_stoklari_page():
    st.title("⚙️ Alt Parça Stokları")
    stock = load_stock()

    df = pd.DataFrame([
        {"Parça": p, "Stok": v["stok"], "Kritik": v["kritik"]}
        for p, v in stock.items()
    ])

    edited = st.data_editor(df, use_container_width=True)

    if st.button("Kaydet"):
        for _, r in edited.iterrows():
            stock[r["Parça"]]["stok"] = float(r["Stok"])
            stock[r["Parça"]]["kritik"] = float(r["Kritik"])
        save_stock(stock)
        st.success("Kaydedildi")

    kritik = [p for p,v in stock.items() if v["stok"] < v["kritik"]]
    if kritik:
        st.warning("⚠️ Kritik: " + ", ".join(kritik))

# --------------------------
# Geçmiş
# --------------------------
def stok_gecmisi_page():
    st.title("📜 Stok Geçmişi")
    res = supabase.table("stock_history").select("*").order("timestamp", desc=True).execute()
    st.dataframe(pd.DataFrame(res.data), use_container_width=True)

# --------------------------
# MAIN
# --------------------------
if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.write(f"👤 {st.session_state.username}")
    page = st.sidebar.radio(
        "Menü",
        ["Fire Girisi", "Alt Parca Stoklari", "Stok Gecmisi"]
    )

    if page == "Fire Girisi":
        fire_girisi_page()
    elif page == "Alt Parca Stoklari":
        alt_parca_stoklari_page()
    else:
        stok_gecmisi_page()
