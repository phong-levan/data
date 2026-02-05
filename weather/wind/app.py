# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
from datetime import datetime, timedelta

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(page_title="Hệ thống Khí tượng Quốc gia - Phong Le", layout="wide")

# CSS: Giao diện tràn viền và Thanh cuộn cố định
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden; height: 100vh; width: 100vw; }
    .main .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; }
    header, footer, #MainMenu {visibility: hidden;}
    .stSlider {
        position: fixed; bottom: 30px; left: 10%; right: 10%;
        z-index: 10001; background: rgba(255, 255, 255, 0.9);
        padding: 10px 20px; border-radius: 15px; border: 2px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ĐỊNH NGHĨA KHUNG LƯỚI VIỆT NAM ---
# Tạo một lưới tọa độ bao phủ lãnh thổ VN (giãn cách 2 độ để web chạy nhanh)
LAT_RANGE = [8, 12, 16, 20, 23]
LON_RANGE = [103, 105, 107, 109, 111, 113]
VN_BOUNDARY_URL = "https://raw.githubusercontent.com/tony1212/Vietnam-States-Shell-Json/master/Vietnam.json"

@st.cache_data(ttl=3600)
def fetch_grid_weather(selected_hour):
    """Lấy dữ liệu 5 biến từ Open-Meteo cho toàn bộ lưới VN"""
    data_list = []
    for lat in LAT_RANGE:
        for lon in LON_RANGE:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m&timezone=Asia%2FBangkok"
            try:
                res = requests.get(url, timeout=5).json()['current']
                data_list.append({
                    'lat': lat, 'lon': lon,
                    'temp': res['temperature_2m'],
                    'rain': res['precipitation'],
                    'hum': res['relative_humidity_2m'],
                    'pres': res['surface_pressure'],
                    'wind': res['wind_speed_10m']
                })
            except: continue
    return pd.DataFrame(data_list)

# --- 2. THANH CUỘN THỜI GIAN ĐỒNG BỘ ---
now = datetime.now()
time_steps = [now - timedelta(hours=i) for i in range(24)]
time_steps.reverse()

selected_time = st.select_slider(
    "Đồng bộ thời gian quan trắc toàn quốc:",
    options=time_steps,
    format_func=lambda x: x.strftime("%H:00 %d/%m/%Y"),
    key="global_slider"
)

# --- 3. HIỂN THỊ BẢN ĐỒ ---
# Lấy biến số người dùng muốn xem
with st.sidebar:
    st.header("📍 Lớp dữ liệu")
    var_choice = st.radio("Chọn yếu tố hiển thị:", 
                         ["Nhiệt độ (°C)", "Lượng mưa (mm)", "Độ ẩm (%)", "Khí áp (hPa)", "Gió (km/h)"])
    var_map = {"Nhiệt độ (°C)": "temp", "Lượng mưa (mm)": "rain", "Độ ẩm (%)": "hum", "Khí áp (hPa)": "pres", "Gió (km/h)": "wind"}
    target_var = var_map[var_choice]

# Khởi tạo bản đồ Folium
m = folium.Map(location=[16.5, 107.5], zoom_start=6, tiles="CartoDB positron")

# Thêm ranh giới Việt Nam "sẵn có" làm khuôn
folium.GeoJson(
    VN_BOUNDARY_URL,
    name="Biên giới Việt Nam",
    style_function=lambda x: {'fillColor': '#00000000', 'color': 'red', 'weight': 2}
).add_to(m)

# Đổ dữ liệu lưới lên bản đồ
grid_data = fetch_grid_weather(selected_time)
for _, row in grid_data.iterrows():
    # Hiển thị vòng tròn màu sắc theo giá trị (giả lập heatmap cắt theo lãnh thổ)
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=15,
        color='blue' if row[target_var] < 20 else 'orange',
        fill=True,
        fill_opacity=0.4,
        popup=f"{var_choice}: {row[target_var]}"
    ).add_to(m)

st_folium(m, width=2000, height=1200, use_container_width=True)
