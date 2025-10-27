# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import copy
from datetime import datetime

# --------------------------
# Basit kullanıcı doğrulama (örnek)
# --------------------------
USER_CREDENTIALS = {
    "aster1": "1212",
    "meg25": "2525",
    "mtc61": "6116",
    "shs61": "6161"
}

# --------------------------
# Tam ürün -> alt parça yapısı (orijinal sayıda ürün korunmuştur)
# --------------------------
product_structure = {
    "044921F": {"30302475": 1, "33005127": 1, "32103174001": 1, "32001125": 1, "30705054": 1, "33005128": 1, "30705022": 1, "20501005001": 1, "30802023": 1, "32003631": 1, "37023078": 0.01, "37021056": 1},
    "044728F": {"30302475": 1, "30301874005": 1, "33005127": 1, "32001109": 1, "30705054": 1, "33005128": 1, "30705022": 1, "30603125": 1, "32103104001": 1, "30403910": 1, "30802023": 1, "20501005001": 1, "32003631": 1, "37021028": 3.571, "37023077": 0.02},
    "01844013F": {"30505004": 2, "32002961": 1, "30403494": 1, "33206006": 1, "33005017": 1, "30603116": 4, "30603097": 2, "32001153": 1, "33003046": 1, "33206005": 1, "32103040": 2, "32003310": 1, "32003311": 1, "32103039": 1, "30802028": 1, "32003312": 1, "33005271": 1, "32103041": 1, "30603116001": 1, "37021001": 0.031, "37021002": 0.171, "37021044": 0.992, "37023138": 0.0555, "37023102": 0.0555, "37023077": 0.0555},
    "00100011F": {"20501015": 1, "30302007": 1, "32005029": 1, "30505004": 2, "32005030": 1, "30302017": 1, "30403001": 1, "40020011": 1, "30603006": 1, "37023077": 0.02, "37021018": 5.405, "30802003": 1, "30802021": 1, "30603002": 1},
    "044385F": {"30603189": 2, "30603190": 1, "32001097": 1, "32001096": 1, "37023018": 1, "37021047": 1}
}

# --------------------------
# Başlangıç alt parça stokları (tüm anahtarlar dict formatında)
# --------------------------
initial_sub_parts_stock = {
    "30302475": {"stok": 10000, "kritik": 1000},
    "33005127": {"stok": 10000, "kritik": 1000},
    "32103174001": {"stok": 100000, "kritik": 1000},
    "32001125": {"stok": 10000, "kritik": 1000},
    "30705054": {"stok": 10000, "kritik": 1000},
    "33005128": {"stok": 10000, "kritik": 1000},
    "30705022": {"stok": 10000, "kritik": 1000},
    "20501005001": {"stok": 10000, "kritik": 1000},
    "30802023": {"stok": 10000, "kritik": 1000},
    "32003631": {"stok": 10000, "kritik": 1000},
    "37023078": {"stok": 10000, "kritik": 1000},
    "37021056": {"stok": 10000, "kritik": 1000},
    "30301874005": {"stok": 10000, "kritik": 1000},
    "32001109": {"stok": 10000, "kritik": 1000},
    "30603125": {"stok": 10000, "kritik": 1000},
    "32103104001": {"stok": 10000, "kritik": 1000},
    "30403910": {"stok": 10000, "kritik": 1000},
    "37021028": {"stok": 10000, "kritik": 1000},
    "37023077": {"stok": 10000, "kritik": 1000},
    "30505004": {"stok": 10000, "kritik": 1000},
    "32002961": {"stok": 10000, "kritik": 1000},
    "30403494": {"stok": 10000, "kritik": 1000},
    "33206006": {"stok": 10000, "kritik": 1000},
    "33005017": {"stok": 10000, "kritik": 1000},
    "30603116": {"stok": 10000, "kritik": 1000},
    "30603097": {"stok": 10000, "kritik": 1000},
    "32001153": {"stok": 10000, "kritik": 1000},
    "33003046": {"stok": 10000, "kritik": 1000},
    "33206005": {"stok": 10000, "kritik": 1000},
    "32103040": {"stok": 10000, "kritik": 1000},
    "32003310": {"stok": 10000, "kritik": 1000},
    "32003311": {"stok": 10000, "kritik": 1000},
    "32103039": {"stok": 10000, "kritik": 1000},
    "30802028": {"stok": 10000, "kritik": 1000},
    "32003312": {"stok": 10000, "kritik": 1000},
    "33005271": {"stok": 10000, "kritik": 1000},
    "32103041": {"stok": 10000, "kritik": 1000},
    "30603116001": {"stok": 10000, "kritik": 1000},
    "37021001": {"stok": 10000, "kritik": 1000},
    "37021002": {"stok": 10000, "kritik": 1000},
    "37021044": {"stok": 10000, "kritik": 1000},
    "37023138": {"stok": 10000, "kritik": 1000},
    "37023102": {"stok": 10000, "kritik": 1000},
    "20501015": {"stok": 10000, "kritik": 1000},
    "30302007": {"stok": 10000, "kritik": 1000},
    "32005029": {"stok": 10000, "kritik": 1000},
    "32005030": {"stok": 10000, "kritik": 1000},
    "30302017": {"stok": 10000, "kritik": 1000},
    "30403001": {"stok": 10000, "kritik": 1000},
    "40020011": {"stok": 10000, "kritik": 1000},
    "30603006": {"stok": 10000, "kritik": 1000},
    "37021018": {"stok": 10000, "kritik": 1000},
    "30802003": {"stok": 10000, "kritik": 1000},
    "30802021": {"stok": 10000, "kritik": 1000},
    "30603002": {"stok": 10000, "kritik": 1000},
    "30603189": {"stok": 10000, "kritik": 1000},
    "30603190": {"stok": 10000, "kritik": 1000},
    "32001097": {"stok": 10000, "kritik": 1000},
    "32001096": {"stok": 10000, "kritik": 1000},
    "37023018": {"stok": 10000, "kritik": 1000},
    "37021047": {"stok": 10000, "kritik": 1000}
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
    # history will be list of dicts: timestamp, user, product, qty, details
    st.session_state.history = []

# --------------------------
# Hatalı tip tespiti (koruma)
# --------------------------
for key, val in st.session_state.sub_parts_stock.items():
    if isinstance(val, set):
        st.error(f"⚠️ '{key}' hatalı tipte: set bulundu. Düzeltin.")
        st.stop()
    if not isinstance(val, dict):
        st.error(f"⚠️ '{key}' beklenmeyen tipte: {type(val)}. Düzeltin.")
        st.stop()
    if "stok" not in val or "kritik" not in val:
        st.error(f"⚠️ '{key}' içinde 'stok' veya 'kritik' anahtarı eksik.")
        st.stop()

# --------------------------
# Login UI & logic
# --------------------------
def login_page():
    st.title("🔐 Stok Takip Sistemi Girişi")
    username = st.text_input("Kullanıcı Adı", key="login_user")
    password = st.text_input("Şifre", type="password", key="login_pass")

    if st.button("Giriş Yap"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Hoşgeldin, {username} 👋")
            st.experimental_rerun()
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")

# --------------------------
# Logout
# --------------------------
def logout_button():
    st.sidebar.write(f"👤 Giriş yapan: **{st.session_state.username}**")
    if st.sidebar.button("🚪 Çıkış Yap"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

# --------------------------
# Urun Girisi page (tüm ürünler aynı sayıda korunur)
# --------------------------
def urun_girisi_page():
    st.title("📦 Ürün Girişi ve Stok Güncelleme")
    st.write("Her ürün için miktarı girip 'Stokları Güncelle' tuşuna basın.")

    product_quantities = {}
    for product in product_structure.keys():
        # key isimlerini benzersiz yapmak için prefix ekledim
        qty = st.number_input(f"{product} miktarı", min_value=0, step=1, key=f"qty_{product}")
        product_quantities[product] = qty

    if st.button("Stokları Güncelle"):
        # Ön kontrol: eksik parça kodu var mı?
        missing_parts = set()
        for p_struct in product_structure.values():
            for part_code in p_struct.keys():
                if part_code not in st.session_state.sub_parts_stock:
                    missing_parts.add(part_code)
        if missing_parts:
            st.error(f"Aşağıdaki alt parça kodları stok verisinde bulunamadı: {', '.join(sorted(missing_parts))}")
            return

        # Gerçek güncelleme ve history kaydı
        any_change = False
        for product, qty in product_quantities.items():
            if not qty:
                continue
            if qty > 0:
                any_change = True
                deduction_details = []
                for part, amount_per_unit in product_structure[product].items():
                    total_deduction = qty * amount_per_unit
                    # stok tipi kontrolü
                    current = st.session_state.sub_parts_stock[part].get("stok", None)
                    if not isinstance(current, (int, float)):
                        st.error(f"'{part}' için stok değeri geçersiz: {current}")
                        return
                    st.session_state.sub_parts_stock[part]["stok"] = current - total_deduction
                    deduction_details.append({"part": part, "deducted": total_deduction, "before": current, "after": current - total_deduction})
                # history kaydı
                st.session_state.history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": st.session_state.username,
                    "product": product,
                    "qty": qty,
                    "details": deduction_details
                })
        if any_change:
            st.success("Stoklar başarıyla güncellendi.")
        else:
            st.info("Hiçbir ürün için miktar girilmedi (veya tümü 0).")

# --------------------------
# Alt Parca Stoklari (düzenlenebilir)
# --------------------------
def alt_parca_stoklari_page():
    st.title("⚙️ Alt Parça Stokları (Düzenlenebilir)")
    st.write("Tablodaki 'Stok' ve 'Kritik' alanlarını düzenleyip 'Değişiklikleri Kaydet' tuşuna basın.")

    df = pd.DataFrame([
        {"Parça": part, "Stok": info["stok"], "Kritik": info["kritik"]}
        for part, info in st.session_state.sub_parts_stock.items()
    ])

    # Kullanıcı düzenleyebilsin
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("Değişiklikleri Kaydet"):
        # validate and write back
        errors = []
        for _, row in edited_df.iterrows():
            part = row["Parça"]
            try:
                stok_val = float(row["Stok"])
                kritik_val = float(row["Kritik"])
            except Exception:
                errors.append(part)
                continue
            if part in st.session_state.sub_parts_stock:
                st.session_state.sub_parts_stock[part]["stok"] = stok_val
                st.session_state.sub_parts_stock[part]["kritik"] = kritik_val
        if errors:
            st.warning(f"Aşağıdaki parçalar için geçersiz değerler vardı ve atlandı: {', '.join(errors)}")
        st.success("Değişiklikler kaydedildi.")

    # Kritik uyarıları göster (canlı)
    kritikler = [p for p, v in st.session_state.sub_parts_stock.items() if v["stok"] < v["kritik"]]
    if kritikler:
        st.warning(f"⚠️ Kritik seviyenin altına düşen parçalar: {', '.join(kritikler)}")

# --------------------------
# Stok Geçmişi sayfası
# --------------------------
def stok_gecmisi_page():
    st.title("📜 Stok Geçmişi")
    st.write("Ürün girişlerinden kaynaklanan stok değişiklikleri burada listelenir (en yeni üstte).")

    if not st.session_state.history:
        st.info("Henüz stok değişikliği kaydı yok.")
        return

    # ters sırayla göster (yeni en üstte)
    hist_list = list(reversed(st.session_state.history))
    # Flatten for table view
    rows = []
    for entry in hist_list:
        # Kısa özet satırı
        rows.append({
            "Tarih": entry["timestamp"],
            "Kullanıcı": entry["user"],
            "Ürün": entry["product"],
            "Miktar": entry["qty"],
            "Detay Sayısı": len(entry["details"])
        })
    df_hist = pd.DataFrame(rows)
    st.dataframe(df_hist, use_container_width=True)

    # Seçili kaydın detaylarını gösterme
    idx = st.number_input("Detayını görmek istediğin kaydın sıra numarası (1 = en yeni)", min_value=1, max_value=len(hist_list), value=1, step=1)
    sel = hist_list[idx - 1]  # çünkü hist_list ters sıralı
    st.markdown("**Seçili kayıt detayları:**")
    st.write(f"Tarih: {sel['timestamp']}, Kullanıcı: {sel['user']}, Ürün: {sel['product']}, Miktar: {sel['qty']}")
    det_df = pd.DataFrame(sel["details"])
    st.dataframe(det_df, use_container_width=True)

# --------------------------
# App main
# --------------------------
if not st.session_state.logged_in:
    login_page()
else:
    logout_button()
    page = st.sidebar.radio("Sayfa Seç:", ["Urun Girisi", "Alt Parca Stoklari", "Stok Gecmisi"])

    if page == "Urun Girisi":
        urun_girisi_page()
    elif page == "Alt Parca Stoklari":
        alt_parca_stoklari_page()
    elif page == "Stok Gecmisi":
        stok_gecmisi_page()
