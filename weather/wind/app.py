# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components

# --- CẤU HÌNH HỆ THỐNG ---
st.set_page_config(
    page_title="Hệ thống Quan trắc Gió - HMS Integration", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CSS: FIX CỨNG MÀN HÌNH, TRÀN VIỀN & CHỐNG CUỘN TRANG ---
st.markdown("""
    <style>
    /* Xóa sạch lề mặc định của Streamlit */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
    }
    /* Ẩn các thành phần thừa để tối ưu không gian */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Khóa chiều cao màn hình tuyệt đối */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden;
        height: 100vh;
        width: 100vw;
    }
    
    /* Ép Iframe chiếm trọn vẹn khung nhìn */
    iframe {
        height: 100vh !important;
        width: 100vw !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NHÚNG WEB QUAN TRẮC GIÓ (222.255.11.82) ---
# URL đích đến trang MapWind của Cục Khí tượng Thủy văn
target_url = "http://222.255.11.82/Modules/Gio/MapWind.aspx"

# Sử dụng component iframe để nhúng trực tiếp
components.iframe(target_url, height=2000) # Chiều cao lớn để CSS tự động cắt theo 100vh
