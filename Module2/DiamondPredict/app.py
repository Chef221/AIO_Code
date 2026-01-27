import streamlit as st
import numpy as np
import joblib

# --- 1. LOAD MODEL & SCALER ----
theta = np.load(r'C:\Code_AI\AIO_Code\Module2\DiamondPredict\my_diamond_theta.npy')
scaler = joblib.load(r'C:\Code_AI\AIO_Code\Module2\DiamondPredict\my_scaler.pkl')

# --- 2. GIAO DIỆN NHẬP LIỆU ---
st.title('💎 Ứng dụng Dự đoán Giá Kim Cương')
st.write('Nhập thông số viên kim cương để định giá:')

# Chia cột cho đẹp
col1, col2 = st.columns(2)

with col1: 
    carat = st.number_input('Trọng lượng (Carat)', min_value=0.1, max_value=5.0, value=0.5)
    depth = st.number_input('Độ sâu (Depth %)', min_value=40.0, max_value=80.0, value=61.5)
    table = st.number_input('Mặt bàn (Table %)', min_value=40.0, max_value=80.0, value=55.0)
with col2:
    # Kích thước x, y, z
    x = st.number_input('Chiều dài (x)', min_value=0.0, value=4.0)
    y = st.number_input('Chiều rộng (y)', min_value=0.0, value=4.0)
    z = st.number_input('Độ sâu (z)', min_value=0.0, value=2.5)

# Các biến phân loại (Categorical)
st.subheader("Chất lượng")
cut_option = st.selectbox('Chất lượng cắt (Cut)', ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'])
color_option = st.selectbox('Màu sắc (Color)', ['J', 'I', 'H', 'G', 'F', 'E', 'D'])
clarity_option = st.selectbox('Độ tinh khiết (Clarity)', ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF'])

# --- 3. XỬ LÝ DỮ LIỆU (PRE-PROCESSING) ---
if st.button('Dự đoán giá tiền'):
    # A. Mapping từ chữ sang số 
    cut_mapping = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
    color_mapping = {'J': 0, 'I': 1, 'H': 2, 'G': 3, 'F': 4, 'E': 5, 'D': 6}
    clarity_mapping = {'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7}
    
    cut_val = cut_mapping[cut_option]
    color_val = color_mapping[color_option]
    clarity_val = clarity_mapping[clarity_option]
    
    # B. Tạo mảng dữ liệu thô
    # Thứ tự phải đúng y hệt lúc train: [carat, cut, color, clarity, depth, table, x, y, z]
    raw_input = np.array([[carat, cut_val, color_val, clarity_val, depth, table, x, y, z]])    
    # C. Scale dữ liệu (QUAN TRỌNG NHẤT)
    scaled_input = scaler.transform(raw_input)
    
    # D. Thêm Bias Unit (x0 = 1) vào đầu
    final_input = np.c_[np.ones(1), scaled_input] 
    
    # --- 4. DỰ ĐOÁN (PREDICT) ---
    prediction = final_input.dot(theta)
    
    # Lấy giá trị ra (vì kết quả là mảng 1 phần tử)
    price = prediction[0]

    st.success(f'💰 Giá dự đoán: ${price:,.2f} USD')

