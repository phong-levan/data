# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Hệ thống Giám sát Khí tượng Toàn vùng", layout="wide")

st.markdown("""
    <style>
    /* Làm cho ứng dụng tràn viền hoàn toàn */
    .main .block-container { padding: 0 !important; max-width: 100% !important; }
    iframe { width: 100%; height: 92vh; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. ĐỊNH NGHĨA CÁC LỚP DỮ LIỆU WINDY ---
# Các tham số này khớp với các lớp "nguyên trạng" trên Windy
layers = {
    "Trường Gió (Wind)": "wind",
    "Lượng mưa (Rain)": "rain",
    "Nhiệt độ (Temp)": "temp",
    "Khí áp (Pressure)": "pressure",
    "Độ ẩm (Clouds/RH)": "clouds"
}

# --- 2. THANH ĐIỀU KHIỂN ---
with st.sidebar:
    st.header("🌐 Theo dõi Toàn vùng")
    selected_label = st.radio("Chọn yếu tố cần quan sát:", list(layers.keys()))
    layer_slug = layers[selected_label]
    
    st.divider()
    st.info("Bản đồ bao phủ toàn bộ lãnh thổ Việt Nam và khu vực Biển Đông, xung quanh.")

# --- 3. NHÚNG BẢN ĐỒ TOÀN VÙNG (IFRAME WINDY) ---
# Tọa độ 16.0, 108.0 và zoom 5 sẽ bao phủ từ miền Bắc xuống tận phía Nam và ra xa ngoài khơi
windy_url = f"https://www.windy.com/?{layer_slug},16.000,108.000,5"

components.iframe(windy_url)

st.caption(f"Đang hiển thị dữ liệu {selected_label} thực tế từ Windy.com")
