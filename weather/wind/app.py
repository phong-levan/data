# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
import json
import os
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Hệ thống Khí tượng Việt Nam", layout="wide")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden; height: 100vh; }
    .main .block-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; }
    header, footer, #MainMenu {visibility: hidden;}
    .stSlider {
        position: fixed; bottom: 30px; left: 10%; right: 10%;
        z-index: 10001; background: rgba(255, 255, 255, 0.9);
        padding: 10px 20px; border-radius: 15px; border: 2px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. TẢI DỮ LIỆU RANH GIỚI NỘI BỘ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GEO_PATH = os.path.join(BASE_DIR, "vietnam.json")

@st.cache_data
def load_geojson():
    if os.path.exists(GEO_PATH):
        with open(GEO_PATH, encoding='utf-8') as f:
            return json.load(f)
    return None

# --- 3. LẤY DỮ LIỆU KHÍ TƯỢNG (GRID) ---
@st.cache_data(ttl=3600)
def get_weather_grid():
    # Danh sách tọa độ lưới đại diện phủ khắp VN
    lats = [8.5, 10.5, 12.5, 14.5, 16.5, 18.5, 20.5, 22.5]
    lons = [103.5, 105.5, 107.5, 109.5, 111.5, 113.5]
    
    data = []
    for lt in lats:
        for ln in lons:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lt}&longitude={ln}&current=temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m&timezone=Asia%2FBangkok"
            try:
                res = requests.get(url, timeout=5).json()['current']
                data.append({
                    'lat': lt, 'lon': ln,
                    'temp': res['temperature_2m'], 'rain': res['precipitation'],
                    'hum': res['relative_humidity_2m'], 'pres': res['surface_pressure'],
                    'wind': res['wind_speed_10m']
                })
            except: continue
    return pd.DataFrame(data)

# --- 4. GIAO DIỆN VÀ BẢN ĐỒ ---
with st.sidebar:
    st.header("⚙️ Tùy chọn lớp")
    var_choice = st.selectbox("Yếu tố:", ["Nhiệt độ (°C)", "Lượng mưa (mm)", "Độ ẩm (%)", "Khí áp (hPa)", "Gió (km/h)"])
    var_map = {"Nhiệt độ (°C)": "temp", "Lượng mưa (mm)": "rain", "Độ ẩm (%)": "hum", "Khí áp (hPa)": "pres", "Gió (km/h)": "wind"}

# Thanh cuộn thời gian
time_steps = [(datetime.now() - timedelta(hours=i)) for i in range(24)]
time_steps.reverse()
st.select_slider("Đồng bộ thời gian:", options=time_steps, format_func=lambda x: x.strftime("%H:00 %d/%m"), key="slider")

# Tạo bản đồ
m = folium.Map(location=[16.0, 108.0], zoom_start=6, tiles="CartoDB positron")

# Vẽ ranh giới Việt Nam (nếu có file)
vn_geo = load_geojson()
if vn_geo:
    folium.GeoJson(vn_geo, style_function=lambda x: {'color': 'red', 'weight': 2, 'fillOpacity': 0}).add_to(m)
else:
    st.error("Thiếu file vietnam.json trong thư mục!")

# Vẽ dữ liệu khí tượng
df = get_weather_grid()
for _, row in df.iterrows():
    val = row[var_map[var_choice]]
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=12,
        popup=f"{var_choice}: {val}",
        color='blue' if val < 20 else 'orange',
        fill=True, fill_opacity=0.6
    ).add_to(m)

st_folium(m, width=2000, height=1200, use_container_width=True)
