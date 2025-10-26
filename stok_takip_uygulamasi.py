# -*- coding: utf-8 -*- 
import streamlit as st
import pandas as pd
import copy

# -------------------------
# Ürün -> alt parça yapısı
# -------------------------
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

# --------------------------------
# Başlangıç alt parça stokları
# (Tüm girişler dict formatında olmalı)
# --------------------------------
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

# ------------------------------------------------
# Session state initialization (deep copy to be safe)
# ------------------------------------------------
if "sub_parts_stock" not in st.session_state:
    st.session_state.sub_parts_stock = copy.deepcopy(initial_sub_parts_stock)

# Hatalı tip tespiti: (eski hatalı state kalmışsa hemen uyar)
for key, val in st.session_state.sub_parts_stock.items():
    if isinstance(val, set):
        st.error(f"⚠️ '{key}' hatalı tipte: set bulundu. '{key}': {{'stok': ..., 'kritik': ...}} formatında olmalı.")
        st.stop()
    if not isinstance(val, dict):
        st.error(f"⚠️ '{key}' beklenmeyen tipte: {type(val)}. Düzeltin.")
        st.stop()
    # stok ve kritik anahtarlarının olduğundan emin ol
    if "stok" not in val or "kritik" not in val:
        st.error(f"⚠️ '{key}' içinde 'stok' veya 'kritik' anahtarı eksik.")
        st.stop()

# -------------------------
# Sidebar - sayfa seçimi
# -------------------------
st.sidebar.title("Sayfa Seçimi")
page = st.sidebar.radio("Gitmek istediğiniz sayfayı seçin:", ["Urun Girisi", "Alt Parca Stoklari"])

# -------------------------
# Urun Girisi sayfası
# -------------------------
if page == "Urun Girisi":
    st.title("Urun Girisi ve Stok Guncelleme")
    st.write("Lütfen ürün miktarlarını girin:")

    product_quantities = {}
    for product in product_structure.keys():
        # key olarak ürün kodunu kullanıyoruz; unique olmalı
        qty = st.number_input(f"{product} miktarı", min_value=0, step=1, key=f"qty_{product}")
        product_quantities[product] = qty

    # Güvenlik kontrolü: product_structure'deki tüm parçaların stokta olduğundan emin ol
    missing_parts = set()
    for p_struct in product_structure.values():
        for part_code in p_struct.keys():
            if part_code not in st.session_state.sub_parts_stock:
                missing_parts.add(part_code)
    if missing_parts:
        st.error(f"Aşağıdaki alt parça kodları stok verisinde bulunamadı: {', '.join(sorted(missing_parts))}")
        st.stop()

    if st.button("Stoklari Güncelle"):
        try:
            # Eğer herhangi bir qty negatifse önlenir (number_input zaten engelliyor ama çift kontrol)
            for product, qty in product_quantities.items():
                if qty is None:
                    continue
                for part, amount_per_unit in product_structure[product].items():
                    total_deduction = qty * amount_per_unit
                    # ek güvenlik: stok tipi ve değerini kontrol et
                    current = st.session_state.sub_parts_stock[part].get("stok", None)
                    if not isinstance(current, (int, float)):
                        raise TypeError(f"'{part}' için stok sayısı beklenen formatta değil: {current}")
                    st.session_state.sub_parts_stock[part]["stok"] = current - total_deduction
            st.success("Stoklar başarıyla güncellendi.")
        except Exception as e:
            st.error(f"Hata oluştu: {e}")

    # Opsiyonel: Stokları CSV'ye indir
    if st.button("Stokları CSV olarak indir (.csv)"):
        df_export = pd.DataFrame([
            {"Parca": part, "Mevcut Stok": info["stok"], "Kritik Seviye": info["kritik"]}
            for part, info in st.session_state.sub_parts_stock.items()
        ])
        csv = df_export.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "sub_parts_stock.csv", "text/csv")

# -------------------------
# Alt Parca Stokları sayfası
# -------------------------
elif page == "Alt Parca Stoklari":
    st.title("Alt Parça Stokları")
    st.write("Mevcut alt parça stok durumu:")

    data = []
    for part, info in st.session_state.sub_parts_stock.items():
        status = "Yeterli" if info["stok"] >= info["kritik"] else "Kritik"
        data.append([part, info["stok"], info["kritik"], status])

    df = pd.DataFrame(data, columns=["Parça", "Mevcut Stok", "Kritik Seviye", "Durum"])
    st.dataframe(df)

    critical_parts = [row[0] for row in data if row[3] == "Kritik"]
    if critical_parts:
        st.warning(f"Kritik seviyenin altına düşen parçalar: {', '.join(critical_parts)}")

    # Reset butonu (isteğe bağlı)
    if st.button("Stokları Başlangıç Değerlerine Döndür"):
        st.session_state.sub_parts_stock = copy.deepcopy(initial_sub_parts_stock)
        st.success("Stoklar başlangıç değerlerine döndürüldü.")
