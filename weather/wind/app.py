import streamlit as st
import streamlit.components.v1 as components

# Tọa độ bao quát Việt Nam và Biển Đông
lat, lon, zoom = 16.0, 108.0, 5 
api_key = "0kgGyKktQw84FeBLRRFKE9YW1wkLLaAg"

st.title("Hệ thống Giám sát Khí tượng Toàn vùng")

# Nhúng bản đồ Windy qua API (Dạng Map Forecast)
windy_script = f"""
    <iframe width="100%" height="600" 
        src="https://www.windy.com/img/js/leaflet-api.js?key={api_key}" 
        frameborder="0">
    </iframe>
"""
# Lưu ý: Với Streamlit, cách nhúng Iframe chuyên sâu nhất là dùng URL nhúng có tham số
windy_url = f"https://www.windy.com/?wind,{lat},{lon},{zoom},m:eU0aj6U"
components.iframe(windy_url, height=700)
