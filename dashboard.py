# ============================================
# DASHBOARD E-COMMERCE BRAZIL ANALYSIS
# DENGAN FITUR FILTER INTERAKTIF - FULLY FUNCTIONAL
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
from datetime import datetime
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
    .main-title { font-size: 2rem; font-weight: bold; color: #1E88E5; text-align: center; margin-bottom: 0.5rem; }
    .subtitle { font-size: 1rem; color: #666; text-align: center; margin-bottom: 2rem; }
    .metric-card { border-radius: 15px; padding: 1rem; color: white; text-align: center; }
    .metric-card-blue { background: linear-gradient(135deg, #1E88E5 0%, #42A5F5 100%); }
    .metric-card-green { background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%); }
    .metric-card-orange { background: linear-gradient(135deg, #E65100 0%, #FF9800 100%); }
    .metric-card-red { background: linear-gradient(135deg, #C62828 0%, #EF5350 100%); }
    .metric-card-purple { background: linear-gradient(135deg, #6A1B9A 0%, #AB47BC 100%); }
    .metric-value { font-size: 1.8rem; font-weight: bold; }
    .metric-label { font-size: 0.85rem; opacity: 0.9; }
    .insight-box { background-color: #e8f0fe; border-left: 5px solid #1E88E5; padding: 1rem; border-radius: 10px; margin: 1rem 0; }
    .insight-title { font-weight: bold; color: #1E88E5; margin-bottom: 0.5rem; }
    .success-box { background-color: #e8f5e9; border-left: 5px solid #4CAF50; padding: 1rem; border-radius: 10px; margin: 1rem 0; }
    footer { text-align: center; color: #888; font-size: 0.8rem; margin-top: 2rem; padding: 1rem; border-top: 1px solid #eee; }
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. LOAD DATASETS
# ============================================

st.markdown("## 📂 Memuat Data...")

if not os.path.exists('data'):
    os.makedirs('data')
    st.warning("Folder 'data' telah dibuat. Silakan masukkan file CSV ke dalam folder 'data'.")

# Dictionary untuk menyimpan semua dataframe
datasets = {}

file_config = {
    'orders': ('orders.csv', ';'),
    'order_reviews': ('order_reviews.csv', ';'),
    'sellers': ('sellers.csv', ';'),
    'order_items': ('order_items.csv', ';'),
    'customers': ('customers.csv', ';'),
    'geolocation': ('geolocation.csv', ';'),
    'order_payments': ('order_payments.csv', ';'),
    'product_category': ('product_category_name_translation.csv', ';'),
    'products': ('products.csv', ';')
}

for name, (filename, sep) in file_config.items():
    try:
        df = pd.read_csv(f'data/{filename}', sep=sep)
        datasets[name] = df
        st.success(f"✅ {filename} loaded ({len(df):,} rows)")
    except Exception as e:
        st.error(f"❌ Error loading {filename}: {e}")
        datasets[name] = pd.DataFrame()

# Assign ke variabel individual
orders_df = datasets['orders']
order_reviews_df = datasets['order_reviews']
sellers_df = datasets['sellers']
order_items_df = datasets['order_items']
customers_df = datasets['customers']
geolocation_df = datasets['geolocation']
order_payments_df = datasets['order_payments']
product_category_df = datasets['product_category']
products_df = datasets['products']

st.markdown("---")

# ============================================
# 5. PREPROCESSING - KONVERSI TANGGAL
# ============================================

# Konversi tanggal di orders_df
if not orders_df.empty and 'order_purchase_timestamp' in orders_df.columns:
    orders_df['order_date'] = pd.to_datetime(
        orders_df['order_purchase_timestamp'], 
        format='%d/%m/%Y %H:%M', 
        errors='coerce'
    )
    orders_df['year'] = orders_df['order_date'].dt.year
    orders_df['month'] = orders_df['order_date'].dt.month
    orders_df['order_date_only'] = orders_df['order_date'].dt.date

# Konversi review_score ke numeric
if not order_reviews_df.empty and 'review_score' in order_reviews_df.columns:
    order_reviews_df['review_score'] = pd.to_numeric(order_reviews_df['review_score'], errors='coerce')

# ============================================
# 6. DATA AGREGASI (HASIL DARI NOTEBOOK)
# ============================================

@st.cache_data
def get_aggregated_results():
    """Data hasil agregasi dari notebook - KONSISTEN dengan EDA"""
    
    delivery_rating_data = {
        'delivery_status': ['Lebih Cepat', 'Tepat Waktu', 'Terlambat'],
        'mean_rating': [4.22, 4.22, 4.09],
        'count': [17981, 72, 17468],
        'std': [1.23, 1.13, 1.34]
    }
    
    review_distribution = {
        'review_score': [1, 2, 3, 4, 5],
        'count': [11127, 3071, 8001, 18729, 56172],
        'percentage': [11.5, 3.2, 8.2, 19.3, 57.8]
    }
    
    delay_rating_data = {
        'delay_range': ['1-3 hari', '4-7 hari', '> 7 hari'],
        'mean_rating': [3.81, 3.52, 4.09],
        'count': [137, 125, 17206]
    }
    
    delivery_status_dist = {
        'delivery_status': ['Lebih Cepat', 'Tepat Waktu', 'Terlambat'],
        'count': [17981, 72, 17468],
        'percentage': [50.6, 0.2, 49.2]
    }
    
    city_performance_data = {
        'seller_city': ['sao paulo', 'curitiba', 'rio de janeiro', 'belo horizonte', 
                        'ribeirao preto', 'guarulhos', 'ibitinga', 'santo andre', 
                        'campinas', 'maringa', 'sao jose do rio preto', 'itaquaquecetuba',
                        'piracicaba', 'petropolis', 'salto', 'jacarei', 'praia grande',
                        'sumare', 'penapolis', 'pedreira'],
        'seller_state': ['SP', 'PR', 'RJ', 'MG', 'SP', 'SP', 'SP', 'SP', 
                         'SP', 'PR', 'SP', 'SP', 'SP', 'RJ', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP'],
        'total_sellers': [694, 127, 96, 68, 52, 50, 49, 45, 41, 40, 0, 9, 12, 6, 9, 7, 10, 5, 5, 3],
        'total_products_sold': [27357, 2955, 2356, 2522, 2208, 2309, 7621, 2886, 0, 2194, 2544, 
                                 1844, 2272, 983, 1326, 934, 1310, 599, 441, 260],
        'avg_products_per_seller': [39.4, 23.3, 24.5, 37.1, 42.5, 46.2, 155.5, 64.1, 
                                     0, 54.9, 0, 204.9, 189.3, 163.8, 147.3, 133.4, 131.0, 119.8, 88.2, 86.5]
    }
    
    state_performance_data = {
        'seller_state': ['SP', 'PR', 'RJ', 'MG'],
        'total_sellers': [991, 167, 102, 68],
        'total_products_sold': [52139, 5149, 3339, 2522]
    }
    
    return {
        'delivery_rating': pd.DataFrame(delivery_rating_data),
        'review_distribution': pd.DataFrame(review_distribution),
        'delay_rating': pd.DataFrame(delay_rating_data),
        'delivery_status_dist': pd.DataFrame(delivery_status_dist),
        'city_performance': pd.DataFrame(city_performance_data),
        'state_performance': pd.DataFrame(state_performance_data),
        'correlation': {'pearson_r': 0.967, 'p_value': 0.0000},
        'ttest': {'t_statistic': 13.5777, 'p_value': 0.000000},
        'anova': {'f_statistic': 92.5340, 'p_value': 0.000000}
    }

results = get_aggregated_results()
city_data_clean = results['city_performance'][results['city_performance']['total_sellers'] > 0].copy()

# ============================================
# 7. SIDEBAR - FILTER INTERAKTIF
# ============================================

st.sidebar.markdown("# 📊 E-Commerce Dashboard")
st.sidebar.markdown("Analisis Data Brazil E-Commerce")
st.sidebar.markdown("**Oleh:** Firdhania Nur Rizky Setyarini")
st.sidebar.markdown("---")
st.sidebar.markdown("## 🔧 Filter Interaktif")

# ========== FILTER 1: DATE RANGE ==========
st.sidebar.markdown("### 📅 Filter Periode")

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
else:
    start_date, end_date = min_date, max_date

# ========== FILTER 2: KOTA ==========
st.sidebar.markdown("### 🏙️ Filter Kota")

all_cities = sorted(city_data_clean['seller_city'].unique().tolist())
selected_cities = st.sidebar.multiselect(
    "Pilih Kota",
    options=all_cities,
    default=['sao paulo', 'curitiba', 'rio de janeiro']
)

# ========== FILTER 3: KETERLAMBATAN ==========
st.sidebar.markdown("### ⏰ Filter Rentang Keterlambatan")

delay_filter = st.sidebar.select_slider(
    "Pilih Rentang Keterlambatan",
    options=['Semua', '1-3 hari', '4-7 hari', '> 7 hari'],
    value='Semua'
)

# ========== FILTER 4: NEGARA BAGIAN ==========
st.sidebar.markdown("### 📍 Filter Negara Bagian")

all_states = sorted(results['state_performance']['seller_state'].unique().tolist())
selected_states = st.sidebar.multiselect(
    "Pilih Negara Bagian",
    options=all_states,
    default=['SP', 'PR', 'RJ', 'MG']
)

# ========== MENU NAVIGASI ==========
st.sidebar.markdown("---")
st.sidebar.markdown("## 📌 Pilih Analisis")

analysis_type = st.sidebar.radio(
    "Menu Analisis:",
    [
        "🏠 Overview Dashboard",
        "📦 Pertanyaan 1: Pengaruh Waktu Pengiriman",
        "⭐ Detail Rating",
        "📍 Pertanyaan 2: Analisis Seller & Lokasi",
        "📈 Kesimpulan & Rekomendasi"
    ]
)

# ========== TAMPILKAN FILTER AKTIF ==========
st.sidebar.markdown("---")
st.sidebar.markdown("### ✅ Filter Aktif")
st.sidebar.markdown(f"📅 {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
if selected_cities:
    st.sidebar.markdown(f"🏙️ {len(selected_cities)} kota dipilih")
if selected_states:
    st.sidebar.markdown(f"📍 {', '.join(selected_states)}")
st.sidebar.markdown(f"⏰ {delay_filter}")

# ============================================
# 8. FUNGSI FILTER DATA
# ============================================

def filter_orders_by_date(df, start_date, end_date):
    """Filter orders berdasarkan rentang tanggal"""
    if df.empty or 'order_date' not in df.columns:
        return df
    return df[
        (df['order_date'] >= pd.Timestamp(start_date)) & 
        (df['order_date'] <= pd.Timestamp(end_date))
    ]

def get_filtered_reviews(orders_df, reviews_df, start_date, end_date):
    """Get reviews yang sesuai dengan filter tanggal"""
    if orders_df.empty or reviews_df.empty:
        return reviews_df
    
    filtered_orders = filter_orders_by_date(orders_df, start_date, end_date)
    if filtered_orders.empty or 'order_id' not in filtered_orders.columns:
        return reviews_df
    
    filtered_order_ids = filtered_orders['order_id'].unique()
    if 'order_id' in reviews_df.columns:
        return reviews_df[reviews_df['order_id'].isin(filtered_order_ids)]
    return reviews_df

# Terapkan filter tanggal ke orders
filtered_orders = filter_orders_by_date(orders_df, start_date, end_date)

# Dapatkan reviews yang terfilter
filtered_reviews = get_filtered_reviews(orders_df, order_reviews_df, start_date, end_date)

# ============================================
# 9. MAIN CONTENT - HEADER
# ============================================

st.markdown('<div class="main-title">📊 E-Commerce Brazil Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analisis Pengiriman & Performa Seller | Periode 2016-2018</div>', unsafe_allow_html=True)

# ============================================
# 10. MENU 1: OVERVIEW DASHBOARD
# ============================================

if analysis_type == "🏠 Overview Dashboard":
    st.markdown("## 📈 Ringkasan Data")
    
    # Data yang sudah difilter
    filtered_city_data = city_data_clean[city_data_clean['seller_city'].isin(selected_cities)]
    filtered_state_data = results['state_performance'][results['state_performance']['seller_state'].isin(selected_states)]
    
    # Hitung rata-rata rating dari data terfilter
    if not filtered_reviews.empty and 'review_score' in filtered_reviews.columns:
        avg_rating_filtered = filtered_reviews['review_score'].mean()
        total_reviews_filtered = len(filtered_reviews)
    else:
        avg_rating_filtered = 4.09
        total_reviews_filtered = 0
    
    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders_filtered = len(filtered_orders)
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-value">{total_orders_filtered:,}</div>
            <div class="metric-label">Total Orders (Filtered)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-card-purple">
            <div class="metric-value">⭐ {avg_rating_filtered:.2f}</div>
            <div class="metric-label">Rata-rata Rating (Filtered)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_sellers_filtered = filtered_state_data['total_sellers'].sum() if not filtered_state_data.empty else 0
        st.markdown(f"""
        <div class="metric-card metric-card-orange">
            <div class="metric-value">{total_sellers_filtered:,}</div>
            <div class="metric-label">Total Seller (Filtered)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_products = len(order_items_df) if not order_items_df.empty else 0
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <div class="metric-value">{total_products:,}</div>
            <div class="metric-label">Total Produk Terjual</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tampilkan informasi filter aktif
    st.info(f"""
    📌 **Filter yang sedang aktif:**
    - 📅 Periode: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}
    - 🏙️ Kota terpilih: {len(selected_cities)} kota
    - 📍 Negara Bagian terpilih: {', '.join(selected_states) if selected_states else 'Semua'}
    - ⏰ Filter keterlambatan: {delay_filter}
    """)
    
    # Ringkasan Pengiriman (Rating per Status) - Data Agregasi
    st.markdown("---")
    st.markdown("## 📊 Rata-rata Rating per Status Pengiriman (Data Historis)")
    
    delivery_stats = results['delivery_rating']
    col1, col2, col3 = st.columns(3)
    
    for col, status in zip([col1, col2, col3], ['Lebih Cepat', 'Tepat Waktu', 'Terlambat']):
        data = delivery_stats[delivery_stats['delivery_status'] == status].iloc[0]
        color = "green" if status == 'Lebih Cepat' else "blue" if status == 'Tepat Waktu' else "red"
        st.markdown(f"""
        <div class="metric-card metric-card-{color}">
            <div class="metric-value">⭐ {data['mean_rating']:.2f}</div>
            <div class="metric-label">{status}<br>{data['count']:,} ({data['count']/delivery_stats['count'].sum()*100:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Top Cities (Filtered by City & State)
    st.markdown("---")
    st.markdown("## 🏙️ Top Kota (Berdasarkan Filter)")
    
    if not filtered_city_data.empty:
        st.dataframe(
            filtered_city_data.nlargest(5, 'total_products_sold')
            [['seller_city', 'seller_state', 'total_sellers', 'total_products_sold']]
            .style.format({'total_products_sold': '{:,.0f}', 'total_sellers': '{:,.0f}'})
        )
    else:
        st.warning("Tidak ada data untuk filter kota/negara bagian yang dipilih")
    
    # Top States (Filtered)
    st.markdown("## 🏆 Top Negara Bagian (Berdasarkan Filter)")
    if not filtered_state_data.empty:
        st.dataframe(
            filtered_state_data.sort_values('total_products_sold', ascending=False)
            [['seller_state', 'total_sellers', 'total_products_sold']]
            .style.format({'total_products_sold': '{:,.0f}', 'total_sellers': '{:,.0f}'})
        )
    else:
        st.warning("Tidak ada data untuk filter negara bagian yang dipilih")

# ============================================
# 11. MENU 2: PERTANYAAN 1 - PENGARUH WAKTU PENGIRIMAN
# ============================================

elif analysis_type == "📦 Pertanyaan 1: Pengaruh Waktu Pengiriman":
    st.markdown("# 📦 Pertanyaan 1: Pengaruh Waktu Pengiriman")
    st.markdown("**Bagaimana perbedaan rata-rata rating pelanggan antara pesanan yang lebih cepat, tepat waktu, dan terlambat?**")
    st.markdown("---")
    
    if delay_filter != 'Semua':
        st.info(f"⏰ Filter keterlambatan aktif: **{delay_filter}**")
        filtered_delay = results['delay_rating'][results['delay_rating']['delay_range'] == delay_filter]
        if not filtered_delay.empty:
            st.metric("Rating untuk filter ini", f"{filtered_delay['mean_rating'].values[0]:.2f}")
    
    # Bar chart rating per status
    delivery_stats = results['delivery_rating']
    
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
    
    # Insight
    mean_faster = delivery_stats[delivery_stats['delivery_status'] == 'Lebih Cepat']['mean_rating'].values[0]
    mean_late = delivery_stats[delivery_stats['delivery_status'] == 'Terlambat']['mean_rating'].values[0]
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown('<div class="insight-title">📌 Insight</div>', unsafe_allow_html=True)
    st.markdown(f"""
    - Rating tertinggi: **Lebih Cepat & Tepat Waktu ({mean_faster:.2f})**
    - Rating terendah: **Terlambat ({mean_late:.2f})**
    - Selisih rating: **{mean_faster - mean_late:.2f} poin**
    - Pengiriman lebih cepat memberikan kepuasan lebih tinggi
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Distribusi Rating
    st.markdown("## 📊 Distribusi Rating Pelanggan")
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

# ============================================
# 12. MENU 3: DETAIL RATING
# ============================================

elif analysis_type == "⭐ Detail Rating":
    st.markdown("# ⭐ Detail Analisis Rating Pelanggan")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rating_dist = results['delivery_rating']
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(rating_dist['delivery_status'], rating_dist['mean_rating'], 
                      color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax.set_ylim(0, 5.5)
        ax.set_ylabel('Rata-rata Rating', fontsize=12)
        ax.set_title('Rata-rata Rating per Status', fontsize=14)
        for bar, val in zip(bars, rating_dist['mean_rating']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{val:.2f}', 
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        status_dist = results['delivery_status_dist']
        fig, ax = plt.subplots(figsize=(8, 6))
        colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
        ax.pie(status_dist['count'], labels=status_dist['delivery_status'],
               autopct='%1.1f%%', colors=colors_pie, startangle=90)
        ax.set_title('Distribusi Status Pengiriman', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("## 📊 Uji Statistik")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("T-Test (Lebih Cepat vs Terlambat)", f"t = {results['ttest']['t_statistic']:.4f}")
        st.caption(f"p-value: {results['ttest']['p_value']:.6f}")
        st.success("✅ Signifikan - Ada perbedaan signifikan")
    with col2:
        st.metric("ANOVA (3 Kelompok)", f"F = {results['anova']['f_statistic']:.4f}")
        st.caption(f"p-value: {results['anova']['p_value']:.6f}")
        st.success("✅ Signifikan - Ada perbedaan di minimal satu pasang kelompok")

# ============================================
# 13. MENU 4: PERTANYAAN 2 - ANALISIS SELLER & LOKASI
# ============================================

elif analysis_type == "📍 Pertanyaan 2: Analisis Seller & Lokasi":
    st.markdown("# 📍 Pertanyaan 2: Hubungan Lokasi Seller dengan Volume Penjualan")
    st.markdown("---")
    
    # Terapkan filter ke data kota
    filtered_city_data = city_data_clean[city_data_clean['seller_city'].isin(selected_cities)]
    filtered_city_data = filtered_city_data[filtered_city_data['seller_state'].isin(selected_states)]
    
    st.markdown("## 🏙️ Top Kota (Berdasarkan Filter)")
    
    if not filtered_city_data.empty:
        top_cities = filtered_city_data.nlargest(10, 'total_products_sold').sort_values('total_products_sold', ascending=True)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors_h = plt.cm.Blues(np.linspace(0.3, 0.9, len(top_cities)))
        bars = ax.barh(top_cities['seller_city'].str.title(), top_cities['total_products_sold'], 
                       color=colors_h, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Total Produk Terjual', fontsize=12, fontweight='bold')
        ax.set_ylabel('Kota', fontsize=12, fontweight='bold')
        ax.set_title('Top Kota dengan Penjualan Tertinggi (Filtered)', fontsize=14, fontweight='bold')
        
        max_val = top_cities['total_products_sold'].max() or 1
        for bar, val in zip(bars, top_cities['total_products_sold']):
            ax.text(val + (max_val * 0.01), bar.get_y() + bar.get_height()/2, 
                    f'{val:,}', va='center', ha='left', fontsize=10, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.dataframe(top_cities[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold', 'avg_products_per_seller']]
                     .style.format({'total_products_sold': '{:,.0f}', 'total_sellers': '{:,.0f}', 'avg_products_per_seller': '{:.1f}'}))
    else:
        st.warning("Tidak ada data untuk filter kota/negara bagian yang dipilih")
    
    # Korelasi (menggunakan data keseluruhan)
    st.markdown("## 📈 Korelasi Jumlah Seller vs Total Penjualan")
    
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
        st.metric("Korelasi Pearson", f"{results['correlation']['pearson_r']:.4f}")
        st.caption(f"p-value: {results['correlation']['p_value']:.6f}")
    with col2:
        st.success("✅ Korelasi positif SANGAT KUAT dan signifikan")
        st.caption("Artinya: Semakin banyak seller, semakin tinggi penjualan")

    # Analisis Lokasi
    st.markdown("## 🌎 Analisis Lokasi Geografis")
    
    state_data = results['state_performance']
    total_sales_sp = state_data[state_data['seller_state'] == 'SP']['total_products_sold'].values[0]
    total_sales_all = state_data['total_products_sold'].sum()
    sp_pct = (total_sales_sp / total_sales_all * 100)
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown('<div class="insight-title">📌 Insight Geografis</div>', unsafe_allow_html=True)
    st.markdown(f"""
    - **SP (São Paulo)** mendominasi dengan **{sp_pct:.1f}%** dari total penjualan nasional
    - **SP** juga memiliki **74.6%** dari total seller
    - **Sao Paulo city** menyumbang **52.5%** dari total penjualan SP
    - **Ketimpangan geografis** sangat signifikan dalam aktivitas e-commerce
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# 14. MENU 5: KESIMPULAN & REKOMENDASI
# ============================================

elif analysis_type == "📈 Kesimpulan & Rekomendasi":
    st.markdown("# 📈 Kesimpulan & Rekomendasi")
    st.markdown("## Berdasarkan Analisis Data E-Commerce Brazil (2016-2018)")
    st.markdown("---")
    
    delivery_stats = results['delivery_rating']
    mean_faster = delivery_stats[delivery_stats['delivery_status'] == 'Lebih Cepat']['mean_rating'].values[0]
    mean_late = delivery_stats[delivery_stats['delivery_status'] == 'Terlambat']['mean_rating'].values[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Kesimpulan")
        st.markdown(f"""
        **Pertanyaan 1: Pengaruh Waktu Pengiriman**
        - Pengiriman lebih cepat: **{mean_faster:.2f}/5**
        - Pengiriman terlambat: **{mean_late:.2f}/5**
        - Selisih: **{mean_faster - mean_late:.2f} poin** (signifikan)
        
        **Pertanyaan 2: Hubungan Lokasi dengan Penjualan**
        - Korelasi: **r = {results['correlation']['pearson_r']:.3f}** (sangat kuat)
        - SP mendominasi: **74.6%** seller, **91.4%** penjualan
        - Kota terlaris: Sao Paulo (**27,357 produk**)
        - Produktivitas tertinggi: Itaquaquecetuba (**204.9 produk/seller**)
        """)
    
    with col2:
        st.markdown("### 💡 Rekomendasi")
        st.markdown("""
        **Optimasi Pengiriman:**
        1. Batasi keterlambatan maksimal 3 hari
        2. Prioritaskan pengiriman lebih cepat dari estimasi
        3. Evaluasi mitra logistik yang sering terlambat (>7 hari)
        4. Implementasi real-time tracking untuk customer
        
        **Ekspansi Seller:**
        1. Rekrut seller di luar SP (PR, RJ, MG)
        2. Jadikan Itaquaquecetuba sebagai model produktivitas
        3. Bangun hub logistik di Curitiba (PR)
        4. Berikan insentif untuk seller produktif (>150 produk/seller)
        """)
    
    # Metode Analisis
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
st.markdown("""
<footer>
    Dashboard Analisis Data E-Commerce Brazil | Periode 2016-2018<br>
    Data Source: Olist Brazilian E-Commerce Dataset<br>
    Analisis oleh: Firdhania Nur Rizky Setyarini
</footer>
""", unsafe_allow_html=True)