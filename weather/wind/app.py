# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
from datetime import datetime, timedelta

# --- CẤU HÌNH ĐƯỜNG DẪN (Tương thích thư mục mới) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "besttrack.xlsx")

st.set_page_config(page_title="Hệ thống Khí tượng - Phong Le", layout="wide")

# --- CSS: FIXED SLIDER & FULL SCREEN ---
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden; height: 100vh; }
    .main .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; }
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Tùy chỉnh thanh cuộn thời gian nằm cố định ở dưới */
    .stSlider {
        position: fixed;
        bottom: 30px;
        left: 10%;
        right: 10%;
        z-index: 10001;
        background: rgba(255, 255, 255, 0.9);
        padding: 10px 25px;
        border-radius: 15px;
        border: 2px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. LOGIC THANH CUỘN THỜI GIAN (TIME SLIDER) ---
# Tạo danh sách các mốc thời gian (ví dụ: 24h qua, mỗi 30 phút một nấc)
now = datetime.now()
time_steps = [now - timedelta(minutes=30*i) for i in range(48)]
time_steps.reverse()

# Hiển thị thanh cuộn đồng bộ
selected_time = st.select_slider(
    "Lựa chọn thời gian quan trắc (Đồng bộ với HMS):",
    options=time_steps,
    format_func=lambda x: x.strftime("%H:%M %d/%m"),
    key="sync_slider"
)

# --- 2. GIAO DIỆN ĐIỀU KHIỂN SIDEBAR ---
with st.sidebar:
    st.header("🔐 Quản trị Hệ thống")
    acc = st.text_input("Tài khoản HMS:", value="", placeholder="phong-levan...")
    pwd = st.text_input("Mật khẩu:", type="password")
    
    st.divider()
    show_storm = st.toggle("Lớp bão", value=True)
    show_wind = st.toggle("Gió quan trắc (222.255.11.82)", value=True)

# --- 3. HIỂN THỊ BẢN ĐỒ & DỮ LIỆU ---
m = folium.Map(location=[16.0, 108.0], zoom_start=6, tiles="OpenStreetMap")

# Lớp gió quan trắc từ IP 222.255.11.82
if show_wind:
    # Logic: Dùng selected_time để gửi request lấy dữ liệu từ HMS
    # (Giả lập vị trí các trạm gió như trong ảnh bạn gửi)
    stations = [
        {"name": "Bạch Long Vĩ", "lat": 20.1, "lon": 107.7, "ws": 12},
        {"name": "Trường Sa", "lat": 8.6, "lon": 111.9, "ws": 15}
    ]
    for stn in stations:
        folium.Marker(
            [stn['lat'], stn['lon']],
            icon=folium.DivIcon(html=f'<div style="color:black; font-weight:bold;">{stn["ws"]}</div>'),
            popup=f"{stn['name']}: {stn['ws']} m/s lúc {selected_time.strftime('%H:%M')}"
        ).add_to(m)

st_folium(m, width=None, height=2000, use_container_width=True)
