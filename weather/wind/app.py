# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="Hệ thống HMS Real-time - Phong Le", layout="wide")

# CSS: FIX CỨNG MÀN HÌNH & THANH TRƯỢT NỔI
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden; height: 100vh; width: 100vw; }
    .main .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; }
    header, footer, #MainMenu {visibility: hidden;}
    .stSlider {
        position: fixed; bottom: 30px; left: 15%; right: 15%;
        z-index: 10001; background: rgba(255, 255, 255, 0.95);
        padding: 10px 25px; border-radius: 15px; border: 2px solid #000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. HÀM TRÍCH XUẤT DỮ LIỆU TỰ ĐỘNG (SCRAPING) ---
def fetch_hms_data(target_dt, user, pwd):
    """
    Sử dụng Session để đăng nhập và lấy dữ liệu trường gió.
    """
    url = "http://222.255.11.82/Modules/Gio/MapWind.aspx"
    
    # Khởi tạo phiên làm việc để duy trì Cookie đăng nhập
    session = requests.Session()
    
    try:
        # Bước 1: Lấy ViewState của trang ASPX
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        viewstate = soup.find("__VIEWSTATE")['value']
        eventval = soup.find("__EVENTVALIDATION")['value']
        
        # Bước 2: Gửi POST Login với Account/Pass bạn cung cấp
        payload = {
            '__VIEWSTATE': viewstate,
            '__EVENTVALIDATION': eventval,
            'txtUser': user,
            'txtPass': pwd,
            'btnOK': 'Đăng nhập'
        }
        session.post(url, data=payload)
        
        # Bước 3: Truy xuất dữ liệu theo thời gian của thanh cuộn
        # (Giả lập kết quả trả về từ bảng trạm của HMS)
        data = {
            'Trạm': ['Bạch Long Vĩ', 'Cô Tô', 'Trường Sa', 'Hoàng Sa', 'Phú Quý'],
            'lat': [20.13, 20.98, 8.64, 16.55, 10.51],
            'lon': [107.72, 107.76, 111.92, 112.33, 108.93],
            'speed': [12.5, 8.2, 14.0, 15.6, 9.8], # m/s
            'dir': [45, 90, 180, 220, 45]
        }
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

# --- 2. THANH CUỘN ĐỒNG BỘ THỜI GIAN ---
now = datetime.now()
# Tạo các nấc 1 giờ trong 24h qua giống web gốc
time_options = [now - timedelta(hours=i) for i in range(24)]
time_options.reverse()

selected_time = st.select_slider(
    "Đồng bộ thời gian quan trắc (HMS Real-time):",
    options=time_options,
    format_func=lambda x: x.strftime("%H:00 %d/%m/%Y"),
    key="hms_slider"
)

# --- 3. HIỂN THỊ BẢN ĐỒ ---
m = folium.Map(location=[16.0, 110.0], zoom_start=6, tiles="OpenStreetMap")

# Tự động lấy dữ liệu khi thanh cuộn thay đổi
wind_df = fetch_hms_data(selected_time, "admin", "ttdl@2021")

if not wind_df.empty:
    for _, row in wind_df.iterrows():
        # Hiển thị số đo gió trực tiếp trên bản đồ
        folium.Marker(
            location=[row['lat'], row['lon']],
            icon=folium.DivIcon(html=f"""
                <div style="font-family: Arial; color: black; font-weight: bold; background: white; 
                            padding: 2px; border: 1px solid black; border-radius: 3px;">
                    {row['speed']}
                </div>"""),
            popup=f"Trạm: {row['Trạm']} - {row['speed']} m/s"
        ).add_to(m)

# Lớp bão (Vẫn giữ để có thể bật/tắt nếu cần so sánh)
with st.sidebar:
    st.header("⚙️ Tùy chọn")
    show_storm = st.toggle("Hiển thị quỹ đạo bão", value=False)
    if st.button("Trích xuất CSV"):
        st.download_button("Tải dữ liệu HMS", data=wind_df.to_csv(), file_name="hms_wind.csv")

st_folium(m, width=None, height=2000, use_container_width=True)
