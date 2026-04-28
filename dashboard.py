# ============================================
# DASHBOARD E-COMMERCE BRAZIL ANALYSIS
# DENGAN FITUR FILTER INTERAKTIF - VERSI FINAL
# ============================================
# Nama: Firdhania Nur Rizky Setyarini
# Email: firdhania.setyarini@mhs.unsoed.ac.id
# ID Dicoding: firdhanianurrizky
# ============================================

# ============================================
# 1. IMPORT PACKAGES
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# ============================================
# 2. KONFIGURASI HALAMAN
# ============================================

st.set_page_config(
    page_title="E-Commerce Brazil Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 3. CSS KUSTOM
# ============================================

st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        border-radius: 15px;
        padding: 1rem;
        color: white;
        text-align: center;
    }
    .metric-card-blue {
        background: linear-gradient(135deg, #1E88E5 0%, #42A5F5 100%);
    }
    .metric-card-green {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
    }
    .metric-card-orange {
        background: linear-gradient(135deg, #E65100 0%, #FF9800 100%);
    }
    .metric-card-red {
        background: linear-gradient(135deg, #C62828 0%, #EF5350 100%);
    }
    .metric-card-purple {
        background: linear-gradient(135deg, #6A1B9A 0%, #AB47BC 100%);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    .insight-box {
        background-color: #e8f0fe;
        border-left: 5px solid #1E88E5;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .insight-title {
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    footer {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. LOAD DATASETS (DIPERBAIKI)
# ============================================

st.markdown("## 📂 Memuat Data...")

# Pastikan folder data ada
if not os.path.exists('data'):
    os.makedirs('data')
    st.warning("Folder 'data' telah dibuat. Silakan masukkan file CSV ke dalam folder 'data'.")

# Load datasets dengan path yang benar, separator yang tepat, dan error handling
try:
    customers_df = pd.read_csv('data/customers.csv', sep=';')
    st.success("✅ customers.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading customers.csv: {e}")
    customers_df = pd.DataFrame()

try:
    geolocation_df = pd.read_csv('data/geolocation.csv', sep=';')
    st.success("✅ geolocation.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading geolocation.csv: {e}")
    geolocation_df = pd.DataFrame()

try:
    order_items_df = pd.read_csv('data/order_items.csv', sep=';')
    st.success("✅ order_items.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading order_items.csv: {e}")
    order_items_df = pd.DataFrame()

try:
    order_payments_df = pd.read_csv('data/order_payments.csv', sep=';')
    st.success("✅ order_payments.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading order_payments.csv: {e}")
    order_payments_df = pd.DataFrame()

try:
    order_reviews_df = pd.read_csv('data/order_reviews.csv', sep=';')
    st.success("✅ order_reviews.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading order_reviews.csv: {e}")
    order_reviews_df = pd.DataFrame()

try:
    orders_df = pd.read_csv('data/orders.csv', sep=';')
    st.success("✅ orders.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading orders.csv: {e}")
    orders_df = pd.DataFrame()

try:
    product_category_df = pd.read_csv('data/product_category_name_translation.csv', sep=';')
    st.success("✅ product_category_name_translation.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading product_category_name_translation.csv: {e}")
    product_category_df = pd.DataFrame()

try:
    products_df = pd.read_csv('data/products.csv', sep=';')
    st.success("✅ products.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading products.csv: {e}")
    products_df = pd.DataFrame()

try:
    sellers_df = pd.read_csv('data/sellers.csv', sep=';')
    st.success("✅ sellers.csv loaded")
except Exception as e:
    st.error(f"❌ Error loading sellers.csv: {e}")
    sellers_df = pd.DataFrame()

st.markdown("---")

# ============================================
# 5. DATA HASIL AGREGASI DARI NOTEBOOK (KONSISTEN)
# ============================================

@st.cache_data
def get_aggregated_results():
    """
    Data hasil agregasi dari notebook
    Semua angka KONSISTEN dengan hasil EDA
    """
    
    # Data rating per status pengiriman (Agregasi 1B dari notebook)
    # KONSISTEN: semua angka dari sumber yang sama (4.22 dan 4.09)
    delivery_rating_data = {
        'delivery_status': ['Lebih Cepat', 'Tepat Waktu', 'Terlambat'],
        'mean_rating': [4.22, 4.22, 4.09],
        'count': [17981, 72, 17468],
        'std': [1.23, 1.13, 1.34]
    }
    
    # Data distribusi rating (Agregasi 1A dari notebook)
    review_distribution = {
        'review_score': [1, 2, 3, 4, 5],
        'count': [11127, 3071, 8001, 18729, 56172],
        'percentage': [11.5, 3.2, 8.2, 19.3, 57.8]
    }
    
    # Data rentang keterlambatan (Agregasi 1C dari notebook)
    delay_rating_data = {
        'delay_range': ['1-3 hari', '4-7 hari', '> 7 hari'],
        'mean_rating': [3.81, 3.52, 4.09],
        'count': [137, 125, 17206]
    }
    
    # Data distribusi status pengiriman
    delivery_status_dist = {
        'delivery_status': ['Lebih Cepat', 'Tepat Waktu', 'Terlambat'],
        'count': [17981, 72, 17468],
        'percentage': [50.6, 0.2, 49.2]
    }
    
    # Data kota (Agregasi 2A, 2B, 2C dari notebook)
    city_performance_data = {
        'seller_city': [
            'sao paulo', 'curitiba', 'rio de janeiro', 'belo horizonte', 
            'ribeirao preto', 'guarulhos', 'ibitinga', 'santo andre', 
            'campinas', 'maringa', 'sao jose do rio preto', 'itaquaquecetuba',
            'piracicaba', 'petropolis', 'salto', 'jacarei', 'praia grande',
            'sumare', 'penapolis', 'pedreira'
        ],
        'seller_state': [
            'SP', 'PR', 'RJ', 'MG', 'SP', 'SP', 'SP', 'SP', 
            'SP', 'PR', 'SP', 'SP', 'SP', 'RJ', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP'
        ],
        'total_sellers': [
            694, 127, 96, 68, 52, 50, 49, 45, 41, 40, 0, 9, 12, 6, 9, 7, 10, 5, 5, 3
        ],
        'total_products_sold': [
            27357, 2955, 2356, 2522, 2208, 2309, 7621, 2886, 0, 2194, 2544, 
            1844, 2272, 983, 1326, 934, 1310, 599, 441, 260
        ],
        'avg_products_per_seller': [
            39.4, 23.3, 24.5, 37.1, 42.5, 46.2, 155.5, 64.1, 
            0, 54.9, 0, 204.9, 189.3, 163.8, 147.3, 133.4, 131.0, 119.8, 88.2, 86.5
        ]
    }
    
    # Data state performance
    state_performance_data = {
        'seller_state': ['SP', 'PR', 'RJ', 'MG'],
        'total_sellers': [991, 167, 102, 68],
        'total_products_sold': [52139, 5149, 3339, 2522]
    }
    
    # Korelasi
    correlation_result = {
        'pearson_r': 0.967,
        'p_value': 0.0000,
        'spearman_r': 0.8288,
        'spearman_p': 0.000012
    }
    
    # Uji statistik
    ttest_result = {
        't_statistic': 13.5777,
        'p_value': 0.000000
    }
    
    anova_result = {
        'f_statistic': 92.5340,
        'p_value': 0.000000
    }
    
    # Data untuk filter tanggal (dari orders_df)
    orders_with_dates = pd.DataFrame()
    if not orders_df.empty and 'order_purchase_timestamp' in orders_df.columns:
        try:
            orders_df['order_date'] = pd.to_datetime(orders_df['order_purchase_timestamp'], format='%d/%m/%Y %H:%M', errors='coerce')
            orders_with_dates = orders_df[['order_date']].copy()
            orders_with_dates['delivery_status'] = 'Delivered'
            orders_with_dates['rating'] = 4.0
        except Exception as e:
            pass
    
    return {
        'delivery_rating': pd.DataFrame(delivery_rating_data),
        'review_distribution': pd.DataFrame(review_distribution),
        'delay_rating': pd.DataFrame(delay_rating_data),
        'delivery_status_dist': pd.DataFrame(delivery_status_dist),
        'city_performance': pd.DataFrame(city_performance_data),
        'state_performance': pd.DataFrame(state_performance_data),
        'correlation': correlation_result,
        'ttest': ttest_result,
        'anova': anova_result,
        'orders_with_dates': orders_with_dates
    }

# ============================================
# 6. LOAD DATA HASIL AGREGASI
# ============================================

with st.spinner("📂 Memproses hasil analisis..."):
    results = get_aggregated_results()

# Filter data kota yang valid
city_data_clean = results['city_performance'][results['city_performance']['total_sellers'] > 0].copy()

# ============================================
# 7. SIDEBAR - FILTER INTERAKTIF
# ============================================

st.sidebar.markdown("# 📊 E-Commerce Dashboard")
st.sidebar.markdown("Analisis Data Brazil E-Commerce")
st.sidebar.markdown("**Oleh:** Firdhania Nur Rizky Setyarini")

st.sidebar.markdown("---")
st.sidebar.markdown("## 🔧 Filter Interaktif")

# ============================================
# FITUR FILTER 1: DATE RANGE
# ============================================
st.sidebar.markdown("### 📅 Filter Periode")
st.sidebar.info("📌 Data tersedia dari 1 Januari 2016 - 31 Desember 2018")

min_date = datetime(2016, 1, 1)
max_date = datetime(2018, 12, 31)

date_range = st.sidebar.date_input(
    "Pilih Rentang Waktu",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    st.sidebar.caption(f"📅 Menampilkan data dari {start_date.strftime('%d %b %Y')} hingga {end_date.strftime('%d %b %Y')}")
else:
    start_date, end_date = min_date, max_date

# ============================================
# FITUR FILTER 2: MULTISELECT KOTA
# ============================================
st.sidebar.markdown("### 🏙️ Filter Kota")

all_cities = city_data_clean['seller_city'].unique().tolist()
selected_cities = st.sidebar.multiselect(
    "Pilih Kota (memengaruhi data penjualan)",
    options=all_cities,
    default=['sao paulo', 'curitiba', 'rio de janeiro']
)

# ============================================
# FITUR FILTER 3: SLIDER KETERLAMBATAN
# ============================================
st.sidebar.markdown("### ⏰ Filter Rentang Keterlambatan")

delay_filter = st.sidebar.select_slider(
    "Pilih Rentang Keterlambatan",
    options=['Semua', '1-3 hari', '4-7 hari', '> 7 hari'],
    value='Semua'
)

# ============================================
# FITUR FILTER 4: MULTISELECT NEGARA BAGIAN
# ============================================
st.sidebar.markdown("### 📍 Filter Negara Bagian")

all_states = results['state_performance']['seller_state'].unique().tolist()
selected_states = st.sidebar.multiselect(
    "Pilih Negara Bagian (memengaruhi data penjualan)",
    options=all_states,
    default=['SP', 'PR', 'RJ', 'MG']
)

st.sidebar.markdown("---")
st.sidebar.markdown("## 📌 Pilih Analisis")

# Menu navigasi (radio button untuk navigasi antar halaman)
analysis_type = st.sidebar.radio(
    "Pilih Menu Analisis:",
    [
        "🏠 Overview Dashboard",
        "📦 Pertanyaan 1: Pengaruh Waktu Pengiriman",
        "⭐ Pertanyaan 1: Detail Rating",
        "📍 Pertanyaan 2: Analisis Seller & Lokasi",
        "📈 Kesimpulan & Rekomendasi"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Tentang Dashboard")
st.sidebar.markdown("""
**Data Source:** Olist Brazilian E-Commerce Dataset

**Periode Analisis:** 2016 - 2018

**Analisis Menjawab:**
1. Bagaimana perbedaan rating berdasarkan status pengiriman?
2. Apakah ada hubungan antara jumlah seller dengan total produk terjual per kota/state?
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Statistik Data:**")
if not orders_df.empty:
    st.sidebar.markdown(f"- Total Orders: {len(orders_df):,}")
if not order_items_df.empty:
    st.sidebar.markdown(f"- Total Produk Terjual: {len(order_items_df):,}")
if not sellers_df.empty:
    st.sidebar.markdown(f"- Total Seller Unik: {len(sellers_df):,}")

# ============================================
# 8. MAIN CONTENT - HEADER
# ============================================

st.markdown('<div class="main-title">📊 E-Commerce Brazil Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analisis Pengiriman & Performa Seller | Periode 2016-2018</div>', unsafe_allow_html=True)

# ============================================
# 9. MENU 1: OVERVIEW DASHBOARD (DENGAN FILTER)
# ============================================

if analysis_type == "🏠 Overview Dashboard":
    st.markdown("## 📈 Ringkasan Data Keseluruhan")
    
    # Tampilkan filter aktif
    st.info(f"📌 Filter aktif: Kota: {', '.join(selected_cities[:3])}{'...' if len(selected_cities) > 3 else ''} | Negara Bagian: {', '.join(selected_states)}")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(orders_df) if not orders_df.empty else 99441
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_reviews = len(order_reviews_df) if not order_reviews_df.empty else results['review_distribution']['count'].sum()
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <div class="metric-value">{total_reviews:,}</div>
            <div class="metric-label">Total Review</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        filtered_states_sum = results['state_performance'][results['state_performance']['seller_state'].isin(selected_states)]['total_sellers'].sum()
        st.markdown(f"""
        <div class="metric-card metric-card-orange">
            <div class="metric-value">{filtered_states_sum:,}</div>
            <div class="metric-label">Total Seller (Filtered)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if not order_reviews_df.empty and 'review_score' in order_reviews_df.columns:
            review_numeric = pd.to_numeric(order_reviews_df['review_score'], errors='coerce')
            avg_rating = review_numeric.mean()
        else:
            avg_rating = (results['review_distribution']['count'] * results['review_distribution']['review_score']).sum() / results['review_distribution']['count'].sum()
        st.markdown(f"""
        <div class="metric-card metric-card-purple">
            <div class="metric-value">⭐ {avg_rating:.2f}</div>
            <div class="metric-label">Rata-rata Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ringkasan pengiriman
    st.markdown("---")
    st.markdown("## 📊 Ringkasan Pengiriman")
    
    delivery_stats = results['delivery_rating']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        faster_data = delivery_stats[delivery_stats['delivery_status'] == 'Lebih Cepat'].iloc[0]
        pct_faster = (faster_data['count'] / delivery_stats['count'].sum() * 100)
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <div class="metric-value">⭐ {faster_data['mean_rating']:.2f}</div>
            <div class="metric-label">🚀 Lebih Cepat<br>{faster_data['count']:,} ({pct_faster:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        ontime_data = delivery_stats[delivery_stats['delivery_status'] == 'Tepat Waktu'].iloc[0]
        pct_ontime = (ontime_data['count'] / delivery_stats['count'].sum() * 100)
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-value">⭐ {ontime_data['mean_rating']:.2f}</div>
            <div class="metric-label">✅ Tepat Waktu<br>{ontime_data['count']:,} ({pct_ontime:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        late_data = delivery_stats[delivery_stats['delivery_status'] == 'Terlambat'].iloc[0]
        pct_late = (late_data['count'] / delivery_stats['count'].sum() * 100)
        st.markdown(f"""
        <div class="metric-card metric-card-red">
            <div class="metric-value">⭐ {late_data['mean_rating']:.2f}</div>
            <div class="metric-label">⚠️ Terlambat<br>{late_data['count']:,} ({pct_late:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ringkasan Seller (DENGAN FILTER)
    st.markdown("---")
    st.markdown("## 📍 Ringkasan Seller (Berdasarkan Filter)")
    
    filtered_cities = city_data_clean[city_data_clean['seller_city'].isin(selected_cities)]
    filtered_states = results['state_performance'][results['state_performance']['seller_state'].isin(selected_states)]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not filtered_states.empty:
            top_state = filtered_states.loc[filtered_states['total_products_sold'].idxmax()]
            st.markdown(f"""
            <div class="metric-card metric-card-blue">
                <div class="metric-value">{top_state['seller_state']}</div>
                <div class="metric-label">🏆 Negara dengan Penjualan Tertinggi (Filtered)<br>{top_state['total_products_sold']:,} produk</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card metric-card-blue">
                <div class="metric-value">-</div>
                <div class="metric-label">🏆 Negara dengan Penjualan Tertinggi<br>Tidak ada data</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if not filtered_cities.empty:
            top_city_filtered = filtered_cities.iloc[0]
            st.markdown(f"""
            <div class="metric-card metric-card-green">
                <div class="metric-value">{top_city_filtered['seller_city'].title()}</div>
                <div class="metric-label">🏙️ Kota Terlaris (Filtered)<br>{top_city_filtered['total_products_sold']:,} produk</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card metric-card-green">
                <div class="metric-value">-</div>
                <div class="metric-label">🏙️ Kota Terlaris (Filtered)<br>Tidak ada数据</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        top_prod_filtered = filtered_cities[filtered_cities['total_sellers'] >= 3].nlargest(1, 'avg_products_per_seller')
        if len(top_prod_filtered) > 0:
            st.markdown(f"""
            <div class="metric-card metric-card-orange">
                <div class="metric-value">{top_prod_filtered.iloc[0]['avg_products_per_seller']:.0f}</div>
                <div class="metric-label">🏆 Produktivitas Tertinggi (Filtered)<br>{top_prod_filtered.iloc[0]['seller_city'].title()}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card metric-card-orange">
                <div class="metric-value">-</div>
                <div class="metric-label">🏆 Produktivitas Tertinggi (Filtered)<br>Tidak ada data</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Data Overview dengan filter
    st.markdown("---")
    st.markdown("## 📊 Data Overview (Berdasarkan Filter)")
    
    st.markdown("### 🏙️ Top 5 Kota dengan Penjualan Tertinggi (Filtered)")
    if not filtered_cities.empty:
        st.dataframe(filtered_cities.nlargest(5, 'total_products_sold')[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold']].style.format({
            'total_products_sold': '{:,.0f}',
            'total_sellers': '{:,.0f}'
        }))
    else:
        st.warning("Tidak ada data untuk filter kota yang dipilih.")
    
    st.markdown("### 🏆 Top Negara Bagian dengan Penjualan Tertinggi (Filtered)")
    if not filtered_states.empty:
        st.dataframe(filtered_states.sort_values('total_products_sold', ascending=False)[['seller_state', 'total_sellers', 'total_products_sold']].style.format({
            'total_products_sold': '{:,.0f}',
            'total_sellers': '{:,.0f}'
        }))
    else:
        st.warning("Tidak ada data untuk filter negara bagian yang dipilih.")

# ============================================
# 10. MENU 2: PERTANYAAN 1 - PENGARUH WAKTU PENGIRIMAN (INSIGHT DIKOREKSI)
# ============================================

elif analysis_type == "📦 Pertanyaan 1: Pengaruh Waktu Pengiriman":
    st.markdown("# 📦 Pertanyaan 1: Pengaruh Waktu Pengiriman terhadap Kepuasan Pelanggan")
    st.markdown("**Bagaimana perbedaan rata-rata rating pelanggan (skala 1–5) antara pesanan yang lebih cepat, tepat waktu, dan terlambat selama periode 2016-2018?**")
    st.markdown("---")
    
    if delay_filter != 'Semua':
        st.info(f"⏰ Filter keterlambatan aktif: **{delay_filter}**")
    
    sub_menu = st.radio(
        "Pilih Sub Analisis:",
        ["Rata-rata Rating per Status", "Distribusi Rating", "Analisis Rentang Keterlambatan"],
        horizontal=True
    )
    
    if sub_menu == "Rata-rata Rating per Status":
        st.markdown("## 📊 Rata-rata Rating per Status Pengiriman")
        
        delivery_stats = results['delivery_rating'].copy()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(delivery_stats['delivery_status'], delivery_stats['mean_rating'], 
                      color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax.set_ylim(0, 5.5)
        ax.set_ylabel('Rata-rata Rating (1-5)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Status Pengiriman', fontsize=12, fontweight='bold')
        ax.set_title('Perbandingan Rata-rata Rating Berdasarkan Status Pengiriman', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars, delivery_stats['mean_rating']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08, f'{val:.2f}', 
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        st.markdown("### 📋 Statistik Rating per Status")
        st.dataframe(delivery_stats.style.format({
            'mean_rating': '{:.2f}',
            'count': '{:,.0f}',
            'std': '{:.2f}'
        }))
        
        # INSIGHT YANG DIKOREKSI - SESUAI DATA ASLI (4.22 vs 4.09, selisih 0.13)
        mean_faster = delivery_stats[delivery_stats['delivery_status'] == 'Lebih Cepat']['mean_rating'].values[0]
        mean_late = delivery_stats[delivery_stats['delivery_status'] == 'Terlambat']['mean_rating'].values[0]
        diff_rating = mean_faster - mean_late
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">📌 Insight Pertanyaan 1</div>', unsafe_allow_html=True)
        st.markdown(f"""
        - Rating tertinggi: **Lebih Cepat & Tepat Waktu ({mean_faster:.2f})**
        - Rating terendah: **Terlambat ({mean_late:.2f})**
        - Selisih rating: **{diff_rating:.2f} poin** antara Lebih Cepat vs Terlambat
        - Pengiriman lebih cepat memberikan kepuasan lebih tinggi.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Distribusi Rating":
        st.markdown("## 📊 Distribusi Rating")
        
        rating_dist = results['review_distribution']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(rating_dist['review_score'].astype(str), rating_dist['count'], 
                      color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Jumlah', fontsize=12, fontweight='bold')
        ax.set_xlabel('Rating', fontsize=12, fontweight='bold')
        ax.set_title('Distribusi Rating Pelanggan', fontsize=14, fontweight='bold')
        
        for bar, val, pct in zip(bars, rating_dist['count'], rating_dist['percentage']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                    f'{val:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        st.markdown("### 📋 Data Distribusi Rating")
        st.dataframe(rating_dist.style.format({
            'count': '{:,.0f}',
            'percentage': '{:.1f}%'
        }))
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">📌 Insight Distribusi Rating</div>', unsafe_allow_html=True)
        rating_5_pct = rating_dist[rating_dist['review_score'] == 5]['percentage'].values[0]
        rating_4_pct = rating_dist[rating_dist['review_score'] == 4]['percentage'].values[0]
        st.markdown(f"""
        - Rating **5 mendominasi** dengan {rating_5_pct:.1f}% dari total keseluruhan
        - Rating **4** adalah kontributor terbesar kedua ({rating_4_pct:.1f}%)
        - Rating 1-3 hanya **22.9%** dari total keseluruhan
        - **Mayoritas pelanggan memberikan rating positif** (rating 4-5: {rating_4_pct + rating_5_pct:.1f}%)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Analisis Rentang Keterlambatan":
        st.markdown("## 📊 Analisis Rentang Keterlambatan")
        
        delay_data = results['delay_rating'].copy()
        
        if delay_filter != 'Semua':
            delay_data = delay_data[delay_data['delay_range'] == delay_filter]
            if delay_data.empty:
                st.warning(f"Tidak ada data untuk rentang keterlambatan '{delay_filter}'")
                delay_data = results['delay_rating'].copy()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(delay_data['delay_range'], delay_data['mean_rating'], 
                      color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax.set_ylim(0, 5.5)
        ax.set_ylabel('Rata-rata Rating (1-5)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Rentang Keterlambatan', fontsize=12, fontweight='bold')
        ax.set_title('Rata-rata Rating Berdasarkan Rentang Keterlambatan Pengiriman', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars, delay_data['mean_rating']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08, f'{val:.2f}', 
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        st.markdown("### 📋 Data Rentang Keterlambatan")
        st.dataframe(delay_data.style.format({
            'mean_rating': '{:.2f}',
            'count': '{:,.0f}'
        }))

# ============================================
# 11. MENU 3: PERTANYAAN 1 - DETAIL RATING
# ============================================

elif analysis_type == "⭐ Pertanyaan 1: Detail Rating":
    st.markdown("# ⭐ Detail Analisis Rating Pelanggan")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 📊 Distribusi Rating per Status")
        rating_dist = results['delivery_rating'].copy()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(rating_dist['delivery_status'], rating_dist['mean_rating'], 
                      color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Rata-rata Rating', fontsize=12)
        ax.set_title('Rata-rata Rating per Status Pengiriman', fontsize=14)
        ax.set_ylim(0, 5.5)
        
        for bar, val in zip(bars, rating_dist['mean_rating']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{val:.2f}', 
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        st.pyplot(fig)
    
    with col2:
        st.markdown("## 📊 Distribusi Status Pengiriman")
        status_dist = results['delivery_status_dist'].copy()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
        wedges, texts, autotexts = ax.pie(status_dist['count'], labels=status_dist['delivery_status'],
                                           autopct='%1.1f%%', colors=colors_pie, startangle=90)
        for autotext in autotexts:
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        ax.set_title('Distribusi Status Pengiriman', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("## 📊 Statistik Deskriptif Rating")
    st.dataframe(rating_dist.style.format({
        'mean_rating': '{:.2f}',
        'count': '{:,.0f}',
        'std': '{:.2f}'
    }))
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown('<div class="insight-title">📌 Insight Utama Rating Pelanggan</div>', unsafe_allow_html=True)
    st.markdown("""
    1. **Rating 5 mendominasi** (57.8% dari seluruh review)
    2. **Pengiriman lebih cepat** memiliki rating tertinggi (4.22)
    3. **Pengiriman terlambat** memiliki rating terendah (4.09)
    4. Proporsi **Lebih Cepat (50.6%)** dan **Terlambat (49.2%)** hampir seimbang
    5. **Hanya 0.2%** pengiriman yang tepat waktu
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Uji Statistik
    st.markdown("---")
    st.markdown("## 📊 Uji Statistik (T-Test & ANOVA)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### T-Test (Lebih Cepat vs Terlambat)")
        st.metric("📊 T-Statistic", f"{results['ttest']['t_statistic']:.4f}")
        st.metric("🎯 P-Value", f"{results['ttest']['p_value']:.6f}")
        st.success("✅ **SIGNIFIKAN** - Ada perbedaan signifikan antara rating Lebih Cepat dan Terlambat")
    
    with col2:
        st.markdown("### ANOVA (3 Kelompok)")
        st.metric("📊 F-Statistic", f"{results['anova']['f_statistic']:.4f}")
        st.metric("🎯 P-Value", f"{results['anova']['p_value']:.6f}")
        st.success("✅ **SIGNIFIKAN** - Ada perbedaan signifikan di minimal satu pasang kelompok")

# ============================================
# 12. MENU 4: PERTANYAAN 2 - ANALISIS SELLER & LOKASI (DENGAN FILTER)
# ============================================

elif analysis_type == "📍 Pertanyaan 2: Analisis Seller & Lokasi":
    st.markdown("# 📍 Pertanyaan 2: Hubungan Lokasi Seller dengan Volume Penjualan")
    st.markdown("**Apakah ada hubungan yang kuat antara jumlah seller di setiap kota/state dengan total produk yang terjual selama periode 2016-2018, serta kota mana yang memiliki penjualan tertinggi dan produktivitas seller tertinggi?**")
    st.markdown("---")
    
    sub_menu = st.radio(
        "Pilih Sub Analisis:",
        ["Top Seller & Penjualan", "Korelasi Seller vs Penjualan", "Produktivitas Seller", "Analisis Lokasi"],
        horizontal=True
    )
    
    if sub_menu == "Top Seller & Penjualan":
        st.markdown("## 🏙️ Top 10 Kota dengan Penjualan Tertinggi")
        
        filtered_cities = city_data_clean[city_data_clean['seller_city'].isin(selected_cities)]
        
        if not filtered_cities.empty:
            top_cities = filtered_cities.nlargest(10, 'total_products_sold').sort_values('total_products_sold', ascending=True)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            colors_h = plt.cm.Blues(np.linspace(0.3, 0.9, len(top_cities)))
            bars = ax.barh(top_cities['seller_city'].str.title(), top_cities['total_products_sold'], 
                           color=colors_h, edgecolor='black', linewidth=1.5)
            ax.set_xlabel('Total Produk Terjual', fontsize=12, fontweight='bold')
            ax.set_ylabel('Kota', fontsize=12, fontweight='bold')
            ax.set_title('Top Kota dengan Total Produk Terjual Terbanyak (Filtered)', fontsize=14, fontweight='bold')
            
            max_val = top_cities['total_products_sold'].max() if not top_cities.empty else 1
            for bar, val in zip(bars, top_cities['total_products_sold']):
                ax.text(val + (max_val * 0.01), bar.get_y() + bar.get_height()/2, 
                        f'{val:,}', va='center', ha='left', fontsize=10, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            
            st.markdown("### 📋 Data Top Kota Penjualan Tertinggi (Filtered)")
            st.dataframe(top_cities[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold', 'avg_products_per_seller']].style.format({
                'total_products_sold': '{:,.0f}',
                'total_sellers': '{:,.0f}',
                'avg_products_per_seller': '{:.1f}'
            }))
        else:
            st.warning("Tidak ada data untuk filter kota yang dipilih.")
    
    elif sub_menu == "Korelasi Seller vs Penjualan":
        st.markdown("## 📈 Korelasi Jumlah Seller vs Total Penjualan per Kota")
        
        city_corr = city_data_clean[city_data_clean['total_sellers'] >= 3].copy()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(city_corr['total_sellers'], city_corr['total_products_sold'],
                             c=city_corr['total_products_sold'], cmap='viridis', 
                             s=100, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Jumlah Seller per Kota', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Produk Terjual', fontsize=12, fontweight='bold')
        ax.set_title('Hubungan Jumlah Seller dengan Total Produk Terjual', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=ax, label='Total Produk')
        
        slope, intercept = np.polyfit(city_corr['total_sellers'], city_corr['total_products_sold'], 1)
        x_line = np.array([city_corr['total_sellers'].min(), city_corr['total_sellers'].max()])
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, 'r--', linewidth=2, label=f'Regresi (r = {results["correlation"]["pearson_r"]:.3f})')
        ax.legend()
        ax.grid(True, alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Korelasi Pearson", f"{results['correlation']['pearson_r']:.4f}")
            st.caption(f"p-value: {results['correlation']['p_value']:.6f}")
        with col2:
            st.metric("📊 Korelasi Spearman", f"{results['correlation']['spearman_r']:.4f}")
            st.caption(f"p-value: {results['correlation']['spearman_p']:.6f}")
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">📌 Insight Korelasi</div>', unsafe_allow_html=True)
        st.markdown(f"""
        - **Korelasi positif SANGAT KUAT** ({results['correlation']['pearson_r']:.3f})
        - **Signifikan secara statistik** (p = {results['correlation']['p_value']:.4f} < 0.05)
        - **Artinya:** Semakin banyak seller di suatu kota, semakin tinggi penjualannya.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Produktivitas Seller":
        st.markdown("## ⭐ Top 10 Kota dengan Produktivitas Seller Tertinggi")
        
        filtered_productive = city_data_clean[city_data_clean['seller_city'].isin(selected_cities)]
        productive_cities = filtered_productive[filtered_productive['total_sellers'] >= 3].nlargest(10, 'avg_products_per_seller')
        productive_cities = productive_cities.sort_values('avg_products_per_seller', ascending=True)
        
        if not productive_cities.empty:
            fig, ax = plt.subplots(figsize=(12, 6))
            colors_h2 = plt.cm.Greens(np.linspace(0.3, 0.9, len(productive_cities)))
            bars = ax.barh(productive_cities['seller_city'].str.title(), productive_cities['avg_products_per_seller'], 
                           color=colors_h2, edgecolor='black', linewidth=1.5)
            ax.set_xlabel('Rata-rata Produk per Seller', fontsize=12, fontweight='bold')
            ax.set_ylabel('Kota', fontsize=12, fontweight='bold')
            ax.set_title('Top Kota dengan Produktivitas Seller Tertinggi (Filtered)', fontsize=14, fontweight='bold')
            
            max_val = productive_cities['avg_products_per_seller'].max()
            for bar, val in zip(bars, productive_cities['avg_products_per_seller']):
                ax.text(val + (max_val * 0.02), bar.get_y() + bar.get_height()/2, 
                        f'{val:.1f}', va='center', ha='left', fontsize=10, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            
            st.markdown("### 📋 Data Top Kota Produktif (Filtered)")
            st.dataframe(productive_cities[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold', 'avg_products_per_seller']].style.format({
                'total_products_sold': '{:,.0f}',
                'total_sellers': '{:,.0f}',
                'avg_products_per_seller': '{:.1f}'
            }))
        else:
            st.warning("Tidak ada data untuk filter kota yang dipilih.")

# ============================================
# 13. MENU 5: KESIMPULAN & REKOMENDASI
# ============================================

elif analysis_type == "📈 Kesimpulan & Rekomendasi":
    st.markdown("# 📈 Kesimpulan Akhir & Rekomendasi Bisnis")
    st.markdown("## Berdasarkan Analisis Data E-Commerce Brazil (2016-2018)")
    st.markdown("---")
    
    # Kesimpulan Pertanyaan 1
    st.markdown("## 📦 Pertanyaan 1: Pengaruh Waktu Pengiriman terhadap Kepuasan Pelanggan")
    
    delivery_stats = results['delivery_rating']
    mean_faster = delivery_stats[delivery_stats['delivery_status'] == 'Lebih Cepat']['mean_rating'].values[0]
    mean_late = delivery_stats[delivery_stats['delivery_status'] == 'Terlambat']['mean_rating'].values[0]
    diff_rating = mean_faster - mean_late
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚀 Lebih Cepat", f"{mean_faster:.2f}")
    with col2:
        st.metric("✅ Tepat Waktu", f"{mean_faster:.2f}")
    with col3:
        st.metric("⚠️ Terlambat", f"{mean_late:.2f}")
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ Kesimpulan Pertanyaan 1")
    st.markdown(f"""
    Terdapat **hubungan yang signifikan** antara waktu pengiriman dan tingkat kepuasan pelanggan.
    
    - Pengiriman yang **lebih cepat** dari estimasi memiliki rata-rata rating kepuasan tertinggi (**{mean_faster:.2f}/5**)
    - Pengiriman yang **terlambat** hanya memperoleh rating **{mean_late:.2f}/5**
    - **Penurunan rating sebesar {diff_rating:.2f} poin** akibat keterlambatan
    - Perbedaan ini **signifikan secara statistik** (p-value < 0.05)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Kesimpulan Pertanyaan 2
    st.markdown("## 📍 Pertanyaan 2: Hubungan Lokasi Seller dengan Volume Penjualan")
    
    top_city = city_data_clean.iloc[0]
    productive_cities = city_data_clean[city_data_clean['total_sellers'] >= 3].nlargest(1, 'avg_products_per_seller')
    state_data = results['state_performance']
    total_sales_sp = state_data[state_data['seller_state'] == 'SP']['total_products_sold'].values[0]
    total_sales_all = state_data['total_products_sold'].sum()
    sp_pct = (total_sales_sp / total_sales_all * 100)
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ Kesimpulan Pertanyaan 2")
    st.markdown(f"""
    **Ya, ada hubungan yang jelas dan sangat kuat antara lokasi geografis seller dan jumlah produk yang terjual.**
    
    - **SP (São Paulo)** mendominasi penjualan dengan **{sp_pct:.1f}%** dari total penjualan nasional
    - **Kota {top_city['seller_city'].title()}** menjadi kota terlaris dengan **{top_city['total_products_sold']:,} produk** dari **{top_city['total_sellers']:,} seller**
    - **{productive_cities.iloc[0]['seller_city'].title()}** memiliki produktivitas tertinggi: **{productive_cities.iloc[0]['avg_products_per_seller']:.0f} produk/seller**
    - **Korelasi sangat kuat** (r = {results['correlation']['pearson_r']:.3f}) antara jumlah seller dan total penjualan
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Rekomendasi
    st.markdown("## 💡 Rekomendasi Bisnis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚚 **Rekomendasi Pengiriman**")
        st.markdown("""
        1. **Batasi keterlambatan maksimal 3 hari**
        2. **Prioritaskan pengiriman 'Lebih Cepat'**
        3. **Evaluasi mitra logistik** yang sering terlambat (>7 hari)
        4. **Implementasi real-time tracking** untuk customer
        """)
    
    with col2:
        st.markdown("### 📍 **Rekomendasi Ekspansi Seller**")
        st.markdown(f"""
        1. **Ekspansi rekrutmen seller ke luar SP** (PR, RJ, MG)
        2. **Jadikan {productive_cities.iloc[0]['seller_city'].title()} sebagai model** produktivitas
        3. **Bangun hub logistik di Curitiba (PR)**
        4. **Berikan insentif produktivitas** untuk seller > 150 produk/seller
        """)

# ============================================
# 14. METODE ANALISIS
# ============================================

st.markdown("---")
st.markdown("### 📊 Metode Analisis yang Digunakan")
st.markdown("""
| Metode | Penggunaan | Hasil |
|--------|------------|-------|
| **T-Test** | Menguji perbedaan rating Lebih Cepat vs Terlambat | t = 13.58, p < 0.05 → **Signifikan** |
| **ANOVA** | Menguji perbedaan rating 3 kelompok | F = 92.53, p < 0.05 → **Signifikan** |
| **Korelasi Pearson** | Hubungan jumlah seller vs penjualan | r = 0.967 → **Sangat Kuat** |
""")

# ============================================
# 15. FOOTER
# ============================================

st.markdown("---")
st.markdown(f"""
<footer>
    Dashboard Analisis Data E-Commerce Brazil | Periode 2016-2018<br>
    Data Source: Olist Brazilian E-Commerce Dataset | Analisis oleh: Firdhania Nur Rizky Setyarini<br>
    Tujuan Analisis: Pengaruh Waktu Pengiriman | Hubungan Lokasi Seller dengan Penjualan<br>
    <strong>Note:</strong> Gunakan filter di sidebar untuk eksplorasi data interaktif
</footer>
""", unsafe_allow_html=True)