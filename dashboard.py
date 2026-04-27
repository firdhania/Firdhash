# app_dashboard_fixed.py
# Dashboard Interaktif E-Commerce Brazil Analysis
# Dengan fitur pemilih menu - FIXED VERSION (No pyarrow issues)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="E-Commerce Brazil Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS KUSTOM
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
    .warning-box {
        background-color: #fff3e0;
        border-left: 5px solid #FF9800;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .data-table {
        font-size: 0.85rem;
        border-collapse: collapse;
        width: 100%;
    }
    .data-table th {
        background-color: #1E88E5;
        color: white;
        padding: 8px;
        text-align: left;
    }
    .data-table td {
        border: 1px solid #ddd;
        padding: 6px;
    }
    .data-table tr:nth-child(even) {
        background-color: #f2f2f2;
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
# FUNGSI BANTU UNTUK MENAMPILKAN DATAFRAME (TANPA PYARROW)
# ============================================
def display_dataframe(df, max_rows=20):
    """Menampilkan dataframe menggunakan HTML table (tanpa pyarrow)"""
    if df is None or len(df) == 0:
        st.info("Tidak ada data untuk ditampilkan")
        return
    
    # Batasi jumlah baris
    display_df = df.head(max_rows).copy()
    
    # Format angka
    for col in display_df.select_dtypes(include=['float64']).columns:
        if 'avg' in col.lower() or 'productivity' in col.lower() or 'per' in col.lower():
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}")
        else:
            display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else x)
    
    for col in display_df.select_dtypes(include=['int64']).columns:
        display_df[col] = display_df[col].apply(lambda x: f"{x:,}" if pd.notna(x) else x)
    
    # Konversi ke HTML
    html = '<table class="data-table"><thead><tr>'
    for col in display_df.columns:
        html += f'<th>{col}</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in display_df.iterrows():
        html += '<tr>'
        for col in display_df.columns:
            html += f'<td>{row[col]}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    
    if len(df) > max_rows:
        html += f'<p style="font-size:0.8rem; color:#888; margin-top:8px;">* Menampilkan {max_rows} dari {len(df)} baris</p>'
    
    st.markdown(html, unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    """Memuat dataset yang sudah dibersihkan"""
    
    # Load datasets
    customers_df = pd.read_csv('data\customers_df.csv')
    geolocation_df = pd.read_csv('data\geolocation_df.csv')
    order_items_df = pd.read_csv('data\order_items_df.csv')
    order_payments_df = pd.read_csv('data\order_payments_df.csv')
    order_reviews_df = pd.read_csv('data\order_reviews_df.csv')
    orders_df = pd.read_csv('data\orders_df.csv')
    product_category_df = pd.read_csv('data\product_category_df.csv')
    products_df = pd.read_csv('data\products_df.csv')
    sellers_df = pd.read_csv('data\sellers_df.csv')
    
    # Konversi tipe data datetime
    datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 
                     'order_delivered_carrier_date', 'order_delivered_customer_date', 
                     'order_estimated_delivery_date']
    for col in datetime_cols:
        if col in orders_df.columns:
            orders_df[col] = pd.to_datetime(orders_df[col], errors='coerce')
    
    if 'review_creation_date' in order_reviews_df.columns:
        order_reviews_df['review_creation_date'] = pd.to_datetime(order_reviews_df['review_creation_date'], errors='coerce')
    
    if 'shipping_limit_date' in order_items_df.columns:
        order_items_df['shipping_limit_date'] = pd.to_datetime(order_items_df['shipping_limit_date'], errors='coerce')
    
    return {
        'customers': customers_df,
        'geolocation': geolocation_df,
        'order_items': order_items_df,
        'order_payments': order_payments_df,
        'order_reviews': order_reviews_df,
        'orders': orders_df,
        'product_category': product_category_df,
        'products': products_df,
        'sellers': sellers_df
    }

@st.cache_data
def prepare_delivery_review_data(orders_df, order_reviews_df):
    """Mempersiapkan data untuk analisis pengiriman (Pertanyaan 1)"""
    # Merge orders dengan reviews
    merged_df = pd.merge(
        orders_df[['order_id', 'order_purchase_timestamp', 'order_delivered_customer_date', 
                   'order_estimated_delivery_date', 'order_status']],
        order_reviews_df[['order_id', 'review_score']],
        on='order_id',
        how='inner'
    )
    
    # Filter hanya yang sudah delivered
    delivery_review_df = merged_df.dropna(subset=['order_delivered_customer_date']).copy()
    
    # Hitung status pengiriman
    delivery_review_df['actual_date'] = delivery_review_df['order_delivered_customer_date'].dt.date
    delivery_review_df['estimated_date'] = delivery_review_df['order_estimated_delivery_date'].dt.date
    
    # Tentukan status
    delivery_review_df['delivery_status'] = 'Tepat Waktu'
    delivery_review_df.loc[delivery_review_df['actual_date'] < delivery_review_df['estimated_date'], 'delivery_status'] = 'Lebih Cepat'
    delivery_review_df.loc[delivery_review_df['actual_date'] > delivery_review_df['estimated_date'], 'delivery_status'] = 'Terlambat'
    
    # Kategori keterlambatan
    delivery_review_df['delay_days'] = (delivery_review_df['order_delivered_customer_date'] - 
                                         delivery_review_df['order_estimated_delivery_date']).dt.days
    
    def categorize_delay(days):
        if days < -3:
            return 'Lebih Cepat (>3 hari)'
        elif days < 0:
            return 'Lebih Cepat (1-3 hari)'
        elif days == 0:
            return 'Tepat Waktu (0 hari)'
        elif days <= 3:
            return 'Terlambat (1-3 hari)'
        elif days <= 7:
            return 'Terlambat (4-7 hari)'
        else:
            return 'Terlambat (>7 hari)'
    
    delivery_review_df['delay_range'] = delivery_review_df['delay_days'].apply(categorize_delay)
    
    return delivery_review_df

@st.cache_data
def prepare_seller_data(order_items_df, orders_df, sellers_df):
    """Mempersiapkan data untuk analisis seller (Pertanyaan 2)"""
    # Merge order_items dengan orders
    order_seller = pd.merge(
        order_items_df[['order_id', 'order_item_id', 'seller_id', 'price']],
        orders_df[['order_id', 'order_status']],
        on='order_id',
        how='inner'
    )
    
    # Filter hanya pesanan yang delivered
    order_seller = order_seller[order_seller['order_status'] == 'delivered']
    
    # Merge dengan sellers_df
    order_seller_location = pd.merge(
        order_seller,
        sellers_df[['seller_id', 'seller_city', 'seller_state']],
        on='seller_id',
        how='left'
    )
    
    # Agregasi per kota
    city_performance = order_seller_location.groupby(['seller_city', 'seller_state']).agg({
        'seller_id': 'nunique',
        'order_item_id': 'count',
        'price': 'sum'
    }).reset_index()
    city_performance.columns = ['seller_city', 'seller_state', 'total_sellers', 'total_products_sold', 'total_revenue']
    
    # Hitung produktivitas
    city_performance['avg_products_per_seller'] = city_performance['total_products_sold'] / city_performance['total_sellers']
    city_performance['avg_revenue_per_seller'] = city_performance['total_revenue'] / city_performance['total_sellers']
    
    # Agregasi per state
    state_performance = order_seller_location.groupby('seller_state').agg({
        'seller_id': 'nunique',
        'order_item_id': 'count',
        'price': 'sum'
    }).reset_index()
    state_performance.columns = ['seller_state', 'total_sellers', 'total_products_sold', 'total_revenue']
    state_performance['avg_products_per_seller'] = state_performance['total_products_sold'] / state_performance['total_sellers']
    state_performance['avg_revenue_per_seller'] = state_performance['total_revenue'] / state_performance['total_sellers']
    
    return city_performance, state_performance

# Load data
with st.spinner("📂 Memuat data..."):
    data = load_data()
    
    # Prepare delivery data
    delivery_review_df = prepare_delivery_review_data(data['orders'], data['order_reviews'])
    
    # Prepare seller data
    city_performance, state_performance = prepare_seller_data(
        data['order_items'], data['orders'], data['sellers']
    )
    
    # Calculate correlation for seller analysis
    city_corr_clean = city_performance[city_performance['total_sellers'] >= 3].copy()
    if len(city_corr_clean) > 1:
        correlation, p_value = stats.pearsonr(city_corr_clean['total_sellers'], city_corr_clean['total_products_sold'])
        spearman_corr, spearman_p = stats.spearmanr(city_corr_clean['total_sellers'], city_corr_clean['total_products_sold'])
    else:
        correlation, p_value, spearman_corr, spearman_p = 0, 1, 0, 1

st.success("✅ Data berhasil dimuat!")

# ============================================
# Dapatkan rentang tanggal untuk filter
# ============================================
if 'order_purchase_timestamp' in data['orders'].columns:
    min_date = data['orders']['order_purchase_timestamp'].min().date()
    max_date = data['orders']['order_purchase_timestamp'].max().date()
else:
    min_date = datetime(2016, 1, 1).date()
    max_date = datetime(2018, 12, 31).date()

# ============================================
# SIDEBAR - FILTERS & NAVIGATION
# ============================================
st.sidebar.markdown("# 📊 E-Commerce Dashboard")
st.sidebar.markdown("Analisis Data Brazil E-Commerce")

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎛️ Filter Data")

# Filter tanggal
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("📅 Dari", min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("📅 Sampai", max_date, min_value=min_date, max_value=max_date)

# Filter data berdasarkan tanggal
if start_date and end_date:
    filtered_orders = data['orders'][
        (data['orders']['order_purchase_timestamp'].dt.date >= start_date) &
        (data['orders']['order_purchase_timestamp'].dt.date <= end_date)
    ]
    filtered_delivery = prepare_delivery_review_data(filtered_orders, data['order_reviews'])
else:
    filtered_delivery = delivery_review_df

st.sidebar.markdown("---")
st.sidebar.markdown("## 📌 Pilih Analisis")

# Menu navigasi
analysis_type = st.sidebar.radio(
    "Pilih Menu Analisis:",
    [
        "🏠 Overview Dashboard",
        "📦 Pertanyaan 1: Analisis Pengiriman",
        "⭐ Pertanyaan 1: Detail Rating",
        "📍 Pertanyaan 2: Analisis Seller",
        "🏙️ Pertanyaan 2: Analisis Lokasi",
        "📈 Kesimpulan & Rekomendasi"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Tentang Dashboard")
st.sidebar.markdown("""
**Data Source:** Olist Brazilian E-Commerce Dataset

**Periode:** 2016 - 2018

**Analisis Menjawab:**
1. Hubungan waktu pengiriman dengan kepuasan pelanggan
2. Hubungan lokasi seller dengan volume penjualan
""")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Periode Data:** {min_date} - {max_date}")
st.sidebar.markdown(f"**Periode Filter:** {start_date} - {end_date}")

# ============================================
# MAIN CONTENT
# ============================================
st.markdown('<div class="main-title">📊 E-Commerce Brazil Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analisis Pengiriman & Performa Seller | Periode 2016-2018</div>', unsafe_allow_html=True)

# ============================================
# MENU 1: OVERVIEW DASHBOARD
# ============================================
if analysis_type == "🏠 Overview Dashboard":
    st.markdown("## 📈 Ringkasan Data Keseluruhan")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-value">{len(data['orders']):,}</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_products = data['order_items']['order_item_id'].sum()
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <div class="metric-value">{total_products:,}</div>
            <div class="metric-label">Total Produk Terjual</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_sellers = data['sellers']['seller_id'].nunique()
        st.markdown(f"""
        <div class="metric-card metric-card-orange">
            <div class="metric-value">{unique_sellers:,}</div>
            <div class="metric-label">Total Seller</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_rating = data['order_reviews']['review_score'].mean()
        st.markdown(f"""
        <div class="metric-card metric-card-purple">
            <div class="metric-value">⭐ {avg_rating:.2f}</div>
            <div class="metric-label">Rata-rata Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ringkasan data
    st.markdown("---")
    st.markdown("## 📊 Ringkasan Pengiriman")
    
    delivery_stats = filtered_delivery.groupby('delivery_status')['review_score'].agg(['mean', 'count']).round(2)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mean_faster = delivery_stats.loc['Lebih Cepat', 'mean'] if 'Lebih Cepat' in delivery_stats.index else 0
        count_faster = delivery_stats.loc['Lebih Cepat', 'count'] if 'Lebih Cepat' in delivery_stats.index else 0
        pct_faster = (count_faster / len(filtered_delivery) * 100) if len(filtered_delivery) > 0 else 0
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <div class="metric-value">⭐ {mean_faster:.2f}</div>
            <div class="metric-label">🚀 Lebih Cepat<br>{count_faster:,} ({pct_faster:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        mean_ontime = delivery_stats.loc['Tepat Waktu', 'mean'] if 'Tepat Waktu' in delivery_stats.index else 0
        count_ontime = delivery_stats.loc['Tepat Waktu', 'count'] if 'Tepat Waktu' in delivery_stats.index else 0
        pct_ontime = (count_ontime / len(filtered_delivery) * 100) if len(filtered_delivery) > 0 else 0
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-value">⭐ {mean_ontime:.2f}</div>
            <div class="metric-label">✅ Tepat Waktu<br>{count_ontime:,} ({pct_ontime:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        mean_late = delivery_stats.loc['Terlambat', 'mean'] if 'Terlambat' in delivery_stats.index else 0
        count_late = delivery_stats.loc['Terlambat', 'count'] if 'Terlambat' in delivery_stats.index else 0
        pct_late = (count_late / len(filtered_delivery) * 100) if len(filtered_delivery) > 0 else 0
        st.markdown(f"""
        <div class="metric-card metric-card-red">
            <div class="metric-value">⭐ {mean_late:.2f}</div>
            <div class="metric-label">⚠️ Terlambat<br>{count_late:,} ({pct_late:.1f}%)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ringkasan Seller
    st.markdown("---")
    st.markdown("## 📍 Ringkasan Seller")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_state = state_performance.loc[state_performance['total_products_sold'].idxmax()]
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-value">{top_state['seller_state']}</div>
            <div class="metric-label">🏆 Negara dengan Penjualan Tertinggi<br>{top_state['total_products_sold']:,} produk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        top_city = city_performance.iloc[0]
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <div class="metric-value">{top_city['seller_city']}</div>
            <div class="metric-label">🏙️ Kota Terlaris<br>{top_city['total_products_sold']:,} produk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        top_prod = city_performance[city_performance['total_sellers'] >= 3].nlargest(1, 'avg_products_per_seller')
        if len(top_prod) > 0:
            st.markdown(f"""
            <div class="metric-card metric-card-orange">
                <div class="metric-value">{top_prod.iloc[0]['avg_products_per_seller']:.0f}</div>
                <div class="metric-label">🏆 Produktivitas Tertinggi<br>{top_prod.iloc[0]['seller_city']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card metric-card-orange">
                <div class="metric-value">N/A</div>
                <div class="metric-label">Produktivitas Tertinggi</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Data Overview
    st.markdown("---")
    st.markdown("## 📊 Data Overview Ringkasan")
    
    st.markdown("### 🏙️ Top 5 Kota dengan Penjualan Tertinggi")
    display_dataframe(city_performance.nlargest(5, 'total_products_sold')[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold']])
    
    st.markdown("### 🏆 Top 5 Negara Bagian dengan Penjualan Tertinggi")
    display_dataframe(state_performance.nlargest(5, 'total_products_sold')[['seller_state', 'total_sellers', 'total_products_sold']])

# ============================================
# MENU 2: PERTANYAAN 1 - ANALISIS PENGIRIMAN
# ============================================
elif analysis_type == "📦 Pertanyaan 1: Analisis Pengiriman":
    st.markdown("# 📦 Pertanyaan 1: Pengaruh Waktu Pengiriman terhadap Kepuasan Pelanggan")
    
    # Sub-menu untuk Pertanyaan 1
    sub_menu = st.radio(
        "Pilih Sub Analisis:",
        ["Rata-rata Rating per Status", "Distribusi Rating", "Analisis Rentang Keterlambatan", "Uji Statistik"],
        horizontal=True
    )
    
    if sub_menu == "Rata-rata Rating per Status":
        st.markdown("## 📊 Rata-rata Rating per Status Pengiriman")
        
        delivery_stats = filtered_delivery.groupby('delivery_status')['review_score'].agg(['mean', 'count', 'std']).round(2)
        delivery_stats = delivery_stats.reindex(['Lebih Cepat', 'Tepat Waktu', 'Terlambat'])
        
        # Bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_bar = {'Lebih Cepat': '#0D47A1', 'Tepat Waktu': '#1E88E5', 'Terlambat': '#64B5F6'}
        bars = ax.bar(delivery_stats.index, delivery_stats['mean'], 
                      color=[colors_bar.get(x, '#1E88E5') for x in delivery_stats.index],
                      edgecolor='black', linewidth=1.5)
        ax.set_ylim(0, 5.5)
        ax.set_ylabel('Rata-rata Rating (1-5)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Status Pengiriman', fontsize=12, fontweight='bold')
        ax.set_title('Perbandingan Rata-rata Rating Berdasarkan Status Pengiriman', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars, delivery_stats['mean']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{val:.2f}', 
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        # Tabel data dengan HTML
        st.markdown("### 📋 Statistik Rating per Status")
        stats_display = delivery_stats.copy()
        stats_display['count'] = stats_display['count'].apply(lambda x: f"{x:,}")
        display_dataframe(stats_display.reset_index())
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">💡 Insight</div>', unsafe_allow_html=True)
        st.markdown(f"""
        - Pengiriman **Lebih Cepat** memiliki rating tertinggi ({delivery_stats.loc['Lebih Cepat', 'mean']:.2f})
        - Pengiriman **Terlambat** memiliki rating terendah ({delivery_stats.loc['Terlambat', 'mean']:.2f})
        - Selisih rating antara Lebih Cepat dan Terlambat: **{delivery_stats.loc['Lebih Cepat', 'mean'] - delivery_stats.loc['Terlambat', 'mean']:.2f} poin**
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Distribusi Rating":
        st.markdown("## 📊 Distribusi Rating per Status Pengiriman")
        
        # Stacked bar chart
        rating_dist = pd.crosstab(filtered_delivery['delivery_status'], filtered_delivery['review_score'])
        rating_dist_pct = rating_dist.div(rating_dist.sum(axis=1), axis=0) * 100
        rating_dist_pct = rating_dist_pct.reindex(['Lebih Cepat', 'Tepat Waktu', 'Terlambat'])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        rating_colors = ['#0D47A1', '#1565C0', '#1E88E5', '#42A5F5', '#64B5F6']
        rating_dist_pct.plot(kind='bar', stacked=True, ax=ax, color=rating_colors, edgecolor='black', width=0.7)
        ax.set_ylabel('Persentase (%)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Status Pengiriman', fontsize=12, fontweight='bold')
        ax.set_title('Distribusi Rating per Status Pengiriman', fontsize=14, fontweight='bold')
        ax.legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_ylim(0, 100)
        
        for container in ax.containers:
            labels = [f'{val:.1f}%' if val > 5 else '' for val in container.datavalues]
            ax.bar_label(container, labels=labels, fontsize=8, label_type='center')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Pie chart untuk semua rating
        st.markdown("## 📊 Distribusi Rating Keseluruhan")
        
        overall_rating_dist = filtered_delivery['review_score'].value_counts().sort_index()
        
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        colors_pie = ['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#27ae60']
        wedges, texts, autotexts = ax2.pie(overall_rating_dist.values, labels=overall_rating_dist.index,
                                            autopct='%1.1f%%', colors=colors_pie, startangle=90,
                                            shadow=True)
        for autotext in autotexts:
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        ax2.set_title('Distribusi Rating Keseluruhan', fontsize=14, fontweight='bold')
        st.pyplot(fig2)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">💡 Insight</div>', unsafe_allow_html=True)
        rating_5_pct = (filtered_delivery['review_score'] == 5).mean() * 100
        st.markdown(f"""
        - Mayoritas pelanggan memberikan rating **5 ({rating_5_pct:.1f}%)**
        - Rating 1 dan 2 memiliki persentase lebih rendah (~15%)
        - Pelanggan cenderung memberikan rating ekstrem (positif atau negatif)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Analisis Rentang Keterlambatan":
        st.markdown("## 📊 Analisis Rentang Keterlambatan")
        
        delay_rating = filtered_delivery.groupby('delay_range')['review_score'].agg(['mean', 'count']).reset_index()
        delay_order = ['Lebih Cepat (>3 hari)', 'Lebih Cepat (1-3 hari)', 'Tepat Waktu (0 hari)',
                       'Terlambat (1-3 hari)', 'Terlambat (4-7 hari)', 'Terlambat (>7 hari)']
        delay_rating['delay_range'] = pd.Categorical(delay_rating['delay_range'], categories=delay_order, ordered=True)
        delay_rating = delay_rating.sort_values('delay_range')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors_delay = ['#0D47A1', '#1565C0', '#1E88E5', '#42A5F5', '#64B5F6', '#90CAF9']
        bars = ax.bar(delay_rating['delay_range'], delay_rating['mean'], color=colors_delay, edgecolor='black', linewidth=1.5)
        ax.set_ylim(0, 5.5)
        ax.set_ylabel('Rata-rata Rating (1-5)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Rentang Keterlambatan', fontsize=12, fontweight='bold')
        ax.set_title('Rata-rata Rating Berdasarkan Rentang Keterlambatan', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        
        for bar, val in zip(bars, delay_rating['mean']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{val:.2f}', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        display_dataframe(delay_rating)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">💡 Insight</div>', unsafe_allow_html=True)
        st.markdown("""
        - **Semakin lama keterlambatan, semakin rendah rating** yang diberikan pelanggan
        - Keterlambatan 1-3 hari: rating ~3.8
        - Keterlambatan 4-7 hari: rating ~3.5
        - Pengiriman lebih cepat >3 hari mendapat rating tertinggi (~4.2)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Uji Statistik":
        st.markdown("## 📊 Uji Statistik (T-Test)")
        
        faster_ratings = filtered_delivery[filtered_delivery['delivery_status'] == 'Lebih Cepat']['review_score'].dropna()
        late_ratings = filtered_delivery[filtered_delivery['delivery_status'] == 'Terlambat']['review_score'].dropna()
        ontime_ratings = filtered_delivery[filtered_delivery['delivery_status'] == 'Tepat Waktu']['review_score'].dropna()
        
        if len(faster_ratings) > 0 and len(late_ratings) > 0:
            t_stat, p_val = stats.ttest_ind(faster_ratings, late_ratings)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 T-Statistic", f"{t_stat:.4f}")
            with col2:
                st.metric("🎯 P-Value", f"{p_val:.6f}")
            
            if p_val < 0.05:
                st.success("✅ **Kesimpulan:** Perbedaan rating antara pengiriman 'Lebih Cepat' dan 'Terlambat' **SIGNIFIKAN** secara statistik!")
            else:
                st.warning("⚠️ **Kesimpulan:** Tidak ada perbedaan signifikan antara kedua kelompok.")
            
            # ANOVA test
            f_stat, p_anova = stats.f_oneway(faster_ratings, ontime_ratings, late_ratings)
            st.markdown("---")
            st.markdown("## 📊 Uji ANOVA (3 Kelompok)")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 F-Statistic", f"{f_stat:.4f}")
            with col2:
                st.metric("🎯 P-Value", f"{p_anova:.6f}")
            
            if p_anova < 0.05:
                st.success("✅ **Kesimpulan:** Ada perbedaan signifikan di MINIMAL satu pasang kelompok pengiriman!")
            else:
                st.warning("⚠️ **Kesimpulan:** Tidak ada perbedaan signifikan antar kelompok.")

# ============================================
# MENU 3: PERTANYAAN 1 - DETAIL RATING
# ============================================
elif analysis_type == "⭐ Pertanyaan 1: Detail Rating":
    st.markdown("# ⭐ Detail Analisis Rating Pelanggan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 📊 Distribusi Rating")
        rating_counts = filtered_delivery['review_score'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(rating_counts.index, rating_counts.values, color='#3498db', edgecolor='white', linewidth=2)
        ax.set_xlabel('Rating', fontsize=12)
        ax.set_ylabel('Jumlah', fontsize=12)
        ax.set_title('Distribusi Rating Pelanggan', fontsize=14)
        ax.set_xticks(range(1, 6))
        for bar, v in zip(bars, rating_counts.values):
            pct = v / len(filtered_delivery) * 100
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, f'{v:,}\n({pct:.1f}%)', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.markdown("## 📊 Boxplot Rating per Status")
        data_box = [
            filtered_delivery[filtered_delivery['delivery_status'] == 'Lebih Cepat']['review_score'].dropna(),
            filtered_delivery[filtered_delivery['delivery_status'] == 'Tepat Waktu']['review_score'].dropna(),
            filtered_delivery[filtered_delivery['delivery_status'] == 'Terlambat']['review_score'].dropna()
        ]
        fig, ax = plt.subplots(figsize=(8, 6))
        bp = ax.boxplot(data_box, labels=['Lebih Cepat', 'Tepat Waktu', 'Terlambat'], patch_artist=True)
        colors_box = ['#2ecc71', '#f39c12', '#e74c3c']
        for patch, color in zip(bp['boxes'], colors_box):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax.set_ylabel('Rating', fontsize=12)
        ax.set_title('Distribusi Rating per Status Pengiriman', fontsize=14)
        ax.set_ylim(0, 5.5)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("## 📊 Statistik Deskriptif Rating")
    
    rating_stats = filtered_delivery.groupby('delivery_status')['review_score'].describe()
    display_dataframe(rating_stats.reset_index())
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown('<div class="insight-title">💡 Insight Utama Rating Pelanggan</div>', unsafe_allow_html=True)
    st.markdown("""
    1. **Rating 5 mendominasi** (lebih dari 50% dari seluruh review)
    2. **Pengiriman lebih cepat** memiliki median rating tertinggi (5)
    3. **Pengiriman terlambat** memiliki rentang interkuartil lebih lebar (variasi rating lebih besar)
    4. **Outlier** banyak ditemukan pada pengiriman terlambat (rating rendah)
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MENU 4: PERTANYAAN 2 - ANALISIS SELLER
# ============================================
elif analysis_type == "📍 Pertanyaan 2: Analisis Seller":
    st.markdown("# 📍 Pertanyaan 2: Hubungan Lokasi Seller dengan Volume Penjualan")
    
    # Sub-menu untuk Pertanyaan 2
    sub_menu = st.radio(
        "Pilih Sub Analisis:",
        ["Top Seller Cities", "Korelasi Seller vs Penjualan", "Produktivitas Seller"],
        horizontal=True
    )
    
    if sub_menu == "Top Seller Cities":
        st.markdown("## 🏙️ Top 10 Kota dengan Penjualan Tertinggi")
        
        top_cities = city_performance.nlargest(10, 'total_products_sold').sort_values('total_products_sold', ascending=True)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors_h = plt.cm.Blues(np.linspace(0.3, 0.9, len(top_cities)))
        bars = ax.barh(top_cities['seller_city'], top_cities['total_products_sold'], 
                       color=colors_h, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Total Produk Terjual', fontsize=12, fontweight='bold')
        ax.set_ylabel('Kota', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Kota dengan Penjualan Tertinggi', fontsize=14, fontweight='bold')
        
        max_val = top_cities['total_products_sold'].max()
        for bar, val in zip(bars, top_cities['total_products_sold']):
            ax.text(val + (max_val * 0.01), bar.get_y() + bar.get_height()/2, 
                    f'{val:,}', va='center', ha='left', fontsize=10, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("### 📋 Data Top 10 Kota")
        display_dataframe(top_cities[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold', 'avg_products_per_seller']])
        
        # Top 5 States
        st.markdown("## 🏆 Top 5 Negara Bagian dengan Penjualan Tertinggi")
        top_states = state_performance.nlargest(5, 'total_products_sold')
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        bars2 = ax2.bar(top_states['seller_state'], top_states['total_products_sold'], 
                        color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Total Produk Terjual', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Negara Bagian', fontsize=12, fontweight='bold')
        ax2.set_title('Top 5 Negara Bagian dengan Penjualan Tertinggi', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars2, top_states['total_products_sold']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, f'{val:,}', 
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax2.grid(axis='y', alpha=0.3)
        st.pyplot(fig2)
        
        display_dataframe(top_states[['seller_state', 'total_sellers', 'total_products_sold']])
    
    elif sub_menu == "Korelasi Seller vs Penjualan":
        st.markdown("## 📈 Korelasi Jumlah Seller vs Total Penjualan per Kota")
        
        city_corr = city_performance[city_performance['total_sellers'] >= 3].copy()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(city_corr['total_sellers'], city_corr['total_products_sold'],
                             c=city_corr['total_products_sold'], cmap='viridis', 
                             s=80, alpha=0.7, edgecolor='black', linewidth=1)
        ax.set_xlabel('Jumlah Seller per Kota', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Produk Terjual', fontsize=12, fontweight='bold')
        ax.set_title('Hubungan Jumlah Seller dengan Total Produk Terjual', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=ax, label='Total Produk')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        if len(city_corr) > 1:
            slope, intercept = np.polyfit(city_corr['total_sellers'], city_corr['total_products_sold'], 1)
            x_line = np.array([city_corr['total_sellers'].min(), city_corr['total_sellers'].max()])
            y_line = slope * x_line + intercept
            ax.plot(x_line, y_line, 'r--', linewidth=2, label=f'Regresi (r = {correlation:.3f})')
            ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Korelasi Pearson", f"{correlation:.4f}")
        with col2:
            st.metric("📈 Korelasi Spearman", f"{spearman_corr:.4f}")
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">💡 Interpretasi Korelasi</div>', unsafe_allow_html=True)
        
        if correlation > 0.7:
            st.markdown(f"""
            - **Korelasi SANGAT KUAT** (r = {correlation:.3f})
            - **Hubungan positif**: Semakin banyak seller di suatu kota, semakin tinggi penjualan
            - **Signifikan secara statistik** (p-value = {p_value:.6f} < 0.05)
            """)
        elif correlation > 0.5:
            st.markdown(f"""
            - **Korelasi KUAT** (r = {correlation:.3f})
            - **Hubungan positif** antara jumlah seller dan penjualan
            """)
        else:
            st.markdown(f"""
            - **Korelasi LEMAH** (r = {correlation:.3f})
            - Hubungan tidak terlalu kuat antara jumlah seller dan penjualan
            """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Produktivitas Seller":
        st.markdown("## ⭐ Top 10 Kota dengan Produktivitas Seller Tertinggi")
        
        productive_cities = city_performance[city_performance['total_sellers'] >= 3].nlargest(10, 'avg_products_per_seller')
        productive_cities = productive_cities.sort_values('avg_products_per_seller', ascending=True)
        
        if len(productive_cities) > 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            colors_h2 = plt.cm.Greens(np.linspace(0.3, 0.9, len(productive_cities)))
            bars = ax.barh(productive_cities['seller_city'], productive_cities['avg_products_per_seller'], 
                           color=colors_h2, edgecolor='black', linewidth=1.5)
            ax.set_xlabel('Rata-rata Produk per Seller', fontsize=12, fontweight='bold')
            ax.set_ylabel('Kota', fontsize=12, fontweight='bold')
            ax.set_title('Top 10 Kota dengan Produktivitas Seller Tertinggi\n(minimal 3 seller)', fontsize=14, fontweight='bold')
            
            max_val = productive_cities['avg_products_per_seller'].max()
            for bar, val in zip(bars, productive_cities['avg_products_per_seller']):
                ax.text(val + (max_val * 0.02), bar.get_y() + bar.get_height()/2, 
                        f'{val:.1f}', va='center', ha='left', fontsize=10, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            
            st.markdown("### 📋 Data Top 10 Kota Produktif")
            display_dataframe(productive_cities[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold', 'avg_products_per_seller']])
        else:
            st.warning("Tidak ada kota dengan minimal 3 seller untuk ditampilkan")

# ============================================
# MENU 5: PERTANYAAN 2 - ANALISIS LOKASI
# ============================================
elif analysis_type == "🏙️ Pertanyaan 2: Analisis Lokasi":
    st.markdown("# 🌎 Analisis Lokasi Geografis Penjualan")
    
    # Pie chart proporsi penjualan per state
    st.markdown("## 📊 Proporsi Penjualan per Negara Bagian")
    
    top5_states = state_performance.nlargest(5, 'total_products_sold').copy()
    others_total = state_performance['total_products_sold'].sum() - top5_states['total_products_sold'].sum()
    
    pie_data = pd.concat([
        top5_states[['seller_state', 'total_products_sold']],
        pd.DataFrame({'seller_state': ['Lainnya'], 'total_products_sold': [others_total]})
    ], ignore_index=True)
    
    colors_pie = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(pie_data['total_products_sold'], labels=pie_data['seller_state'],
                                       autopct='%1.1f%%', startangle=90, colors=colors_pie,
                                       shadow=True, textprops={'fontsize': 11})
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    ax.set_title('Proporsi Penjualan per Negara Bagian', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Bar chart jumlah seller per state
    st.markdown("## 📊 Jumlah Seller per Negara Bagian")
    
    top_states_seller = state_performance.nlargest(10, 'total_sellers').sort_values('total_sellers', ascending=True)
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    colors_h = plt.cm.Blues(np.linspace(0.3, 0.9, len(top_states_seller)))
    bars = ax2.barh(top_states_seller['seller_state'], top_states_seller['total_sellers'], 
                    color=colors_h, edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Jumlah Seller', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Negara Bagian', fontsize=12, fontweight='bold')
    ax2.set_title('Top 10 Negara Bagian dengan Seller Terbanyak', fontsize=14, fontweight='bold')
    
    max_val = top_states_seller['total_sellers'].max()
    for bar, val in zip(bars, top_states_seller['total_sellers']):
        ax2.text(val + (max_val * 0.01), bar.get_y() + bar.get_height()/2, 
                 f'{val:,}', va='center', ha='left', fontsize=10, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)
    
    # Tabel data
    st.markdown("## 📋 Data Lengkap per Negara Bagian")
    display_dataframe(state_performance.sort_values('total_products_sold', ascending=False))
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown('<div class="insight-title">💡 Insight Geografis</div>', unsafe_allow_html=True)
    
    total_sales_sp = state_performance.loc[state_performance['seller_state'] == 'SP', 'total_products_sold'].values[0] if 'SP' in state_performance['seller_state'].values else 0
    total_sales_all = state_performance['total_products_sold'].sum()
    sp_pct = (total_sales_sp / total_sales_all * 100) if total_sales_all > 0 else 0
    
    st.markdown(f"""
    - **SP (São Paulo)** mendominasi dengan **{sp_pct:.1f}%** dari total penjualan
    - **Konsentrasi penjualan sangat tinggi** di wilayah São Paulo
    - **Ketimpangan geografis** signifikan dalam aktivitas e-commerce
    - Perlu **ekspansi ke wilayah lain** untuk mengurangi ketimpangan
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MENU 6: KESIMPULAN & REKOMENDASI
# ============================================
elif analysis_type == "📈 Kesimpulan & Rekomendasi":
    st.markdown("# 📈 Kesimpulan Akhir & Rekomendasi Bisnis")
    st.markdown(f"📅 **Periode Analisis:** {start_date} - {end_date}")
    st.markdown("---")
    
    # Kesimpulan Pertanyaan 1
    st.markdown("## 📦 Pertanyaan 1: Pengaruh Waktu Pengiriman terhadap Kepuasan Pelanggan")
    
    delivery_stats = filtered_delivery.groupby('delivery_status')['review_score'].agg(['mean', 'count']).round(2)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mean_faster = delivery_stats.loc['Lebih Cepat', 'mean'] if 'Lebih Cepat' in delivery_stats.index else 0
        st.metric("🚀 Lebih Cepat", f"{mean_faster:.2f}")
    with col2:
        mean_ontime = delivery_stats.loc['Tepat Waktu', 'mean'] if 'Tepat Waktu' in delivery_stats.index else 0
        st.metric("✅ Tepat Waktu", f"{mean_ontime:.2f}")
    with col3:
        mean_late = delivery_stats.loc['Terlambat', 'mean'] if 'Terlambat' in delivery_stats.index else 0
        st.metric("⚠️ Terlambat", f"{mean_late:.2f}", delta_color="inverse")
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ Kesimpulan Pertanyaan 1")
    st.markdown(f"""
    Terdapat **hubungan yang signifikan** antara waktu pengiriman dan tingkat kepuasan pelanggan.
    
    - Pengiriman yang **lebih cepat** dari estimasi memiliki rata-rata rating kepuasan tertinggi (**{mean_faster:.2f}/5**)
    - Pengiriman yang **terlambat** hanya memperoleh rating **{mean_late:.2f}/5**
    - **Penurunan rating sebesar {mean_faster - mean_late:.2f} poin** akibat keterlambatan
    - Perbedaan ini **signifikan secara statistik** (p-value < 0.05)
    - **Semakin lama keterlambatan, semakin rendah rating** yang diberikan pelanggan
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Kesimpulan Pertanyaan 2
    st.markdown("## 📍 Pertanyaan 2: Hubungan Lokasi Seller dengan Volume Penjualan")
    
    top_state = state_performance.loc[state_performance['total_products_sold'].idxmax()]
    top_city = city_performance.iloc[0]
    total_sales_sp = state_performance.loc[state_performance['seller_state'] == 'SP', 'total_products_sold'].values[0] if 'SP' in state_performance['seller_state'].values else 0
    total_sales_all = state_performance['total_products_sold'].sum()
    sp_pct = (total_sales_sp / total_sales_all * 100) if total_sales_all > 0 else 0
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ Kesimpulan Pertanyaan 2")
    st.markdown(f"""
    **Ya, ada hubungan yang jelas antara lokasi geografis seller dan jumlah produk yang terjual.**
    
    - **SP (São Paulo)** mendominasi penjualan dengan **{sp_pct:.1f}%** dari total penjualan nasional
    - **Kota {top_city['seller_city']}** menjadi kota terlaris dengan **{top_city['total_products_sold']:,} produk** dari **{top_city['total_sellers']:,} seller**
    - **Korelasi sangat kuat** (r = {correlation:.3f}) antara jumlah seller dan total penjualan
    - **Ketimpangan geografis** sangat signifikan: ~60% seller berada di wilayah SP
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Rekomendasi
    st.markdown("## 💡 Rekomendasi Bisnis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚚 **Strategi Pengiriman**")
        st.markdown("""
        1. **Prioritaskan Ketepatan Waktu**
           - Keterlambatan terbukti menurunkan rating signifikan
           - Berikan estimasi yang realistis (kejutan positif lebih baik)
           - Kompensasi untuk pengiriman terlambat
        
        2. **Optimalkan Rute Logistik**
           - Gunakan data historis untuk prediksi waktu pengiriman
           - Investasi pada sistem tracking real-time
           - Partnership dengan kurir terpercaya
        
        3. **Monitor Performa Pengiriman**
           - Dashboard monitoring keterlambatan
           - Early warning system untuk potensi keterlambatan
        """)
    
    with col2:
        st.markdown("### 📍 **Strategi Ekspansi Seller**")
        st.markdown("""
        1. **Fokus pada Kota Produktif**
           - Identifikasi kota dengan produktivitas tinggi
           - Program insentif untuk seller di kota potensial
           - Pelatihan untuk meningkatkan produktivitas
        
        2. **Diversifikasi Wilayah**
           - Kurangi ketergantungan pada SP
           - Kembangkan infrastruktur logistik di luar pusat ekonomi
           - Kampanye rekrutmen seller di wilayah baru
        
        3. **Data-Driven Decision**
           - Analisis potensi pasar per wilayah
           - Prediksi volume penjualan berdasarkan jumlah seller
           - Optimasi alokasi sumber daya
        """)
    
    st.markdown("---")
    st.markdown("### 🎯 Action Items Prioritas")
    
    priority_col1, priority_col2, priority_col3 = st.columns(3)
    
    with priority_col1:
        st.markdown("""
        **High Priority (Segera)**
        - ✅ Perbaiki SLA pengiriman
        - ✅ Monitor keterlambatan real-time
        - ✅ Ekspansi seller ke luar SP
        """)
    
    with priority_col2:
        st.markdown("""
        **Medium Priority (1-3 bulan)**
        - 📊 Dashboard monitoring performa
        - 🎓 Pelatihan seller produktif
        - 🤝 Partnership logistik baru
        """)
    
    with priority_col3:
        st.markdown("""
        **Low Priority (3-6 bulan)**
        - 🏗️ Infrastruktur gudang baru
        - 📱 Aplikasi seller mobile
        - 🌏 Ekspansi internasional
        """)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(f"""
<footer>
    Dashboard Analisis Data E-Commerce Brazil | Periode 2016-2018<br>
    Data Source: Olist Brazilian E-Commerce Dataset | Filter: {start_date} - {end_date}<br>
    Analisis: Pengiriman vs Kepuasan Pelanggan | Lokasi Seller vs Volume Penjualan
</footer>
""", unsafe_allow_html=True)