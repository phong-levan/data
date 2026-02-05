import streamlit as st
import xarray as xr
import rioxarray
import geopandas as gpd
from shapely.geometry import mapping
import matplotlib.pyplot as plt

# --- 1. TẢI SHAPEFILE VIỆT NAM ---
@st.cache_data
def load_vietnam_shape():
    # Đường dẫn tới file .shp bạn đã up lên GitHub
    shp_path = "weather/wind/shp/vietnam_border.shp" 
    gdf = gpd.read_file(shp_path)
    return gdf

# --- 2. XỬ LÝ CẮT DỮ LIỆU ---
def clip_data_to_vietnam(data_array, gdf):
    # Đảm bảo dữ liệu có hệ tọa độ (CRS)
    data_array.rio.write_crs("epsg:4326", inplace=True)
    
    # Cắt dữ liệu theo hình dạng của shapefile
    clipped = data_array.rio.clip(gdf.geometry.apply(mapping), gdf.crs, drop=True)
    return clipped

st.title("🗺️ Bản đồ Khí tượng Toàn lãnh thổ Việt Nam")

# Giả sử bạn có file NetCDF dữ liệu lưới (ERA5 hoặc tương đương)
# Ở đây mình minh họa bằng cách mở một file .nc
try:
    gdf_vn = load_vietnam_shape()
    
    # Mở dữ liệu lưới (nhiệt độ, mưa...)
    ds = xr.open_dataset("weather/wind/data_grid.nc") 
    var_name = st.selectbox("Chọn biến số:", list(ds.data_vars))
    
    # Thực hiện cắt
    clipped_da = clip_data_to_vietnam(ds[var_name], gdf_vn)
    
    # Hiển thị bản đồ
    fig, ax = plt.subplots(figsize=(10, 12))
    clipped_da.plot(ax=ax, cmap="jet")
    gdf_vn.boundary.plot(ax=ax, color="black", linewidth=1)
    st.pyplot(fig)

except Exception as e:
    st.error(f"Chưa tìm thấy file dữ liệu hoặc Shapefile: {e}")
