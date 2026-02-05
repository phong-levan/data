# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components
from datetime import datetime

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="Hệ thống Windy Việt Nam - Phong Le", layout="wide")

# CSS: Tối ưu hiển thị tràn viền
st.markdown("""
    <style>
    .main .block-container { padding: 0 !important; max-width: 100% !important; }
    iframe { width: 100%; height: 80vh; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. LẤY DỮ LIỆU SỐ (NGUYÊN TRẠNG MÔ HÌNH ECMWF) ---
@st.cache_data(ttl=3600)
def get_windy_style_data():
    # Tọa độ các vùng trọng điểm Việt Nam
    locations = {
        "Hà Nội": [21.03, 105.85], "Đà Nẵng": [16.05, 108.20], 
        "TP.HCM": [10.76, 106.66], "Trường Sa": [8.64, 111.92]
    }
    results = []
    for name, coord in locations.items():
        # Gọi API lấy 5 yếu tố cốt lõi
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coord[0]}&longitude={coord[1]}&current=temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m&timezone=Asia%2FBangkok"
        res = requests.get(url).json()['current']
        results.append({
            "Địa điểm": name,
            "Nhiệt độ (°C)": res['temperature_2m'],
            "Mưa (mm)": res['precipitation'],
            "Độ ẩm (%)": res['relative_humidity_2m'],
            "Khí áp (hPa)": res['surface_pressure'],
            "Gió (km/h)": res['wind_speed_10m']
        })
    return pd.DataFrame(results)

# --- 2. GIAO DIỆN CHÍNH ---
st.title("🌀 Windy Real-time Vietnam")

# Hiển thị bảng số liệu nhanh
df = get_windy_style_data()
st.dataframe(df, use_container_width=True)

# --- 3. NHÚNG BẢN ĐỒ WINDY NGUYÊN BẢN ---
# Bạn có thể thay đổi lớp dữ liệu mặc định bằng cách sửa 'wind' thành 'rain', 'temp', v.v.
windy_layers = {
    "Gió": "wind", "Nhiệt độ": "temp", "Lượng mưa": "rain", 
    "Khí áp": "pressure", "Độ ẩm": "rh"
}

with st.sidebar:
    st.header("⚙️ Lớp bản đồ Windy")
    selected_layer = st.selectbox("Chọn yếu tố hiển thị trên bản đồ:", list(windy_layers.keys()))

# URL Iframe của Windy (Cắt theo khu vực Việt Nam)
windy_url = f"https://www.windy.com/?{windy_layers[selected_layer]},16.05,108.20,6"
components.iframe(windy_url)

st.info("Dữ liệu được cập nhật theo thời gian thực từ mô hình ECMWF.")
