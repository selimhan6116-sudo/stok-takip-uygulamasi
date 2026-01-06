# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ==========================
# SUPABASE BAĞLANTISI
# ==========================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_SERVICE_KEY"]
)

# ==========================
# KULLANICI
# ==========================
USER_CREDENTIALS = {
    "aster1": "1212",
    "meg25": "2525",
    "mtc61": "6116",
    "shs61": "6161",
    "ıstu59": "5959"
}

# ==========================
# SESSION
# ==========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================
# DB FONKSİYONLARI
# ==========================
def load_stock():
    res = supabase.table("sub_parts_stock").select("*").execute()
    return {r["part"]: {"stok": r["stok"], "kritik": r["kritik"]} for r in res.data}

def update_stock(part, new_stock):
    supabase.table("sub_parts_stock").update(
        {"stok": new_stock}
    ).eq("part", part).execute()

def log_history(user, product, qty, details):
    supabase.table("stok_history").insert({
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "product": product,
        "qty": qty,
        "details": details
    }).execute()

# ==========================
# LOGIN
# ==========================
def login_page():
    st.title("🔐 Giriş")
    u = st.text_input("Kullanıcı")
    p = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if u in USER_CREDENTIALS and USER_CREDENTIALS[u] == p:
            st.session_state.logged_in = True
            st.session_state.username = u
            st.rerun()
        else:
            st.error("Hatalı giriş")

# ==========================
# LOGOUT
# ==========================
def logout():
    st.sidebar.write(f"👤 {st.session_state.username}")
    if st.sidebar.button("Çıkış"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# ==========================
# FIRE GİRİŞİ
# ==========================
def fire_page(stock):
    st.title("🔥 Fire Girişi")
    part = st.selectbox("Alt Parça", sorted(stock.keys()))
    qty = st.number_input("Fire Adedi", min_value=0.0, step=1.0)

    if st.button("Kaydet"):
        if qty <= 0:
            st.warning("Adet 0 olamaz")
            return

        current = stock[part]["stok"]
        if current < qty:
            st.error("Yetersiz stok")
            return

        new_stock = current - qty
        update_stock(part, new_stock)

        log_history(
            st.session_state.username,
            "FIRE",
            qty,
            [{"part": part, "before": current, "after": new_stock}]
        )

        st.success("Fire kaydedildi")
        st.rerun()

# ==========================
# STOK TABLOSU
# ==========================
def stock_page(stock):
    st.title("⚙️ Alt Parça Stokları")
    df = pd.DataFrame([
        {"Parça": p, "Stok": v["stok"], "Kritik": v["kritik"]}
        for p, v in stock.items()
    ])
    st.dataframe(df, use_container_width=True)

    kritik = [p for p, v in stock.items() if v["stok"] < v["kritik"]]
    if kritik:
        st.warning("⚠️ Kritik stokta: " + ", ".join(kritik))

# ==========================
# GEÇMİŞ
# ==========================
def history_page():
    st.title("📜 Stok Geçmişi")
    res = supabase.table("stok_history").select("*").order("timestamp", desc=True).execute()
    if not res.data:
        st.info("Kayıt yok")
        return
    st.dataframe(pd.DataFrame(res.data), use_container_width=True)

# ==========================
# MAIN
# ==========================
if not st.session_state.logged_in:
    login_page()
else:
    logout()
    stock = load_stock()
    page = st.sidebar.radio("Sayfa", ["Fire Girisi", "Alt Parca Stoklari", "Stok Gecmisi"])

    if page == "Fire Girisi":
        fire_page(stock)
    elif page == "Alt Parca Stoklari":
        stock_page(stock)
    elif page == "Stok Gecmisi":
        history_page()
