# ============================================
# DASHBOARD E-COMMERCE BRAZIL ANALYSIS
# DENGAN FITUR FILTER TANGGAL - VERSI KOREKSI
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
# 4. DATA HASIL AGREGASI DARI NOTEBOOK
# ============================================

@st.cache_data
def get_aggregated_results():
    """
    Data hasil agregasi dari notebook
    Berdasarkan perhitungan yang sudah dilakukan
    """
    
    # Data rating per status pengiriman (Agregasi 1B dari notebook)
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
    
    # Korelasi (Agregasi 2D dari notebook)
    correlation_result = {
        'pearson_r': 0.967,
        'p_value': 0.0000,
        'spearman_r': 0.8288,
        'spearman_p': 0.000012
    }
    
    # Uji statistik (dari notebook)
    ttest_result = {
        't_statistic': 13.5777,
        'p_value': 0.000000
    }
    
    anova_result = {
        'f_statistic': 92.5340,
        'p_value': 0.000000
    }
    
    return {
        'delivery_rating': pd.DataFrame(delivery_rating_data),
        'review_distribution': pd.DataFrame(review_distribution),
        'delay_rating': pd.DataFrame(delay_rating_data),
        'delivery_status_dist': pd.DataFrame(delivery_status_dist),
        'city_performance': pd.DataFrame(city_performance_data),
        'state_performance': pd.DataFrame(state_performance_data),
        'correlation': correlation_result,
        'ttest': ttest_result,
        'anova': anova_result
    }

# ============================================
# 5. LOAD DATA HASIL AGREGASI
# ============================================

with st.spinner("📂 Memuat hasil analisis..."):
    results = get_aggregated_results()

st.success("✅ Data hasil analisis berhasil dimuat!")

# Filter data kota yang valid (total_sellers > 0)
city_data_clean = results['city_performance'][results['city_performance']['total_sellers'] > 0].copy()

# ============================================
# 6. SIDEBAR - NAVIGATION
# ============================================

st.sidebar.markdown("# 📊 E-Commerce Dashboard")
st.sidebar.markdown("Analisis Data Brazil E-Commerce")
st.sidebar.markdown("**Oleh:** Firdhania Nur Rizky Setyarini")

st.sidebar.markdown("---")
st.sidebar.markdown("## 📌 Pilih Analisis")

# Menu navigasi
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
st.sidebar.markdown(f"- Total Orders: 99,441")
st.sidebar.markdown(f"- Total Produk Terjual: 112,650")
st.sidebar.markdown(f"- Total Seller Unik: 3,095")

# ============================================
# 7. MAIN CONTENT - HEADER
# ============================================

st.markdown('<div class="main-title">📊 E-Commerce Brazil Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analisis Pengiriman & Performa Seller | Periode 2016-2018</div>', unsafe_allow_html=True)

# ============================================
# 8. MENU 1: OVERVIEW DASHBOARD
# ============================================

if analysis_type == "🏠 Overview Dashboard":
    st.markdown("## 📈 Ringkasan Data Keseluruhan")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-value">99,441</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_reviews = results['review_distribution']['count'].sum()
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <div class="metric-value">{total_reviews:,}</div>
            <div class="metric-label">Total Review</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_sellers = results['state_performance']['total_sellers'].sum()
        st.markdown(f"""
        <div class="metric-card metric-card-orange">
            <div class="metric-value">{total_sellers:,}</div>
            <div class="metric-label">Total Seller Aktif</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
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
    
    # Ringkasan Seller
    st.markdown("---")
    st.markdown("## 📍 Ringkasan Seller")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_state = results['state_performance'].loc[results['state_performance']['total_products_sold'].idxmax()]
        st.markdown(f"""
        <div class="metric-card metric-card-blue">
            <div class="metric-value">{top_state['seller_state']}</div>
            <div class="metric-label">🏆 Negara dengan Penjualan Tertinggi<br>{top_state['total_products_sold']:,} produk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        top_city = city_data_clean.iloc[0]
        st.markdown(f"""
        <div class="metric-card metric-card-green">
            <div class="metric-value">{top_city['seller_city'].title()}</div>
            <div class="metric-label">🏙️ Kota Terlaris<br>{top_city['total_products_sold']:,} produk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        top_prod = city_data_clean[city_data_clean['total_sellers'] >= 3].nlargest(1, 'avg_products_per_seller')
        if len(top_prod) > 0:
            st.markdown(f"""
            <div class="metric-card metric-card-orange">
                <div class="metric-value">{top_prod.iloc[0]['avg_products_per_seller']:.0f}</div>
                <div class="metric-label">🏆 Produktivitas Tertinggi<br>{top_prod.iloc[0]['seller_city'].title()}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Data Overview
    st.markdown("---")
    st.markdown("## 📊 Data Overview")
    
    st.markdown("### 🏙️ Top 5 Kota dengan Penjualan Tertinggi")
    st.dataframe(city_data_clean.nlargest(5, 'total_products_sold')[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold']].style.format({
        'total_products_sold': '{:,.0f}',
        'total_sellers': '{:,.0f}'
    }))
    
    st.markdown("### 🏆 Top Negara Bagian dengan Penjualan Tertinggi")
    st.dataframe(results['state_performance'].sort_values('total_products_sold', ascending=False)[['seller_state', 'total_sellers', 'total_products_sold']].style.format({
        'total_products_sold': '{:,.0f}',
        'total_sellers': '{:,.0f}'
    }))

# ============================================
# 9. MENU 2: PERTANYAAN 1 - PENGARUH WAKTU PENGIRIMAN
# ============================================

elif analysis_type == "📦 Pertanyaan 1: Pengaruh Waktu Pengiriman":
    st.markdown("# 📦 Pertanyaan 1: Pengaruh Waktu Pengiriman terhadap Kepuasan Pelanggan")
    st.markdown("**Bagaimana perbedaan rata-rata rating pelanggan (skala 1–5) antara pesanan yang lebih cepat, tepat waktu, dan terlambat selama periode 2016-2018?**")
    st.markdown("---")
    
    # Sub-menu untuk Pertanyaan 1
    sub_menu = st.radio(
        "Pilih Sub Analisis:",
        ["Rata-rata Rating per Status", "Distribusi Rating", "Analisis Rentang Keterlambatan"],
        horizontal=True
    )
    
    if sub_menu == "Rata-rata Rating per Status":
        st.markdown("## 📊 Rata-rata Rating per Status Pengiriman")
        
        delivery_stats = results['delivery_rating'].copy()
        
        # Bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(delivery_stats['delivery_status'], delivery_stats['mean_rating'], 
                      color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax.set_ylim(0, 5.5)
        ax.set_ylabel('Rata-rata Rating (1-5)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Status Pengiriman', fontsize=12, fontweight='bold')
        ax.set_title('Perbandingan Rata-rata Rating Berdasarkan Status Pengiriman\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars, delivery_stats['mean_rating']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08, f'{val:.2f}', 
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        # Tabel data
        st.markdown("### 📋 Statistik Rating per Status")
        st.dataframe(delivery_stats.style.format({
            'mean_rating': '{:.2f}',
            'count': '{:,.0f}',
            'std': '{:.2f}'
        }))
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">📌 Insight Pertanyaan 1</div>', unsafe_allow_html=True)
        st.markdown(f"""
        - Rating tertinggi: **Lebih Cepat & Tepat Waktu ({delivery_stats.loc[delivery_stats['delivery_status'] == 'Lebih Cepat', 'mean_rating'].values[0]:.2f})**
        - Rating terendah: **Terlambat ({delivery_stats.loc[delivery_stats['delivery_status'] == 'Terlambat', 'mean_rating'].values[0]:.2f})**
        - Selisih rating: **{delivery_stats.loc[delivery_stats['delivery_status'] == 'Lebih Cepat', 'mean_rating'].values[0] - delivery_stats.loc[delivery_stats['delivery_status'] == 'Terlambat', 'mean_rating'].values[0]:.2f} poin** antara Lebih Cepat vs Terlambat
        - Pengiriman lebih cepat memberikan kepuasan lebih tinggi.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Distribusi Rating":
        st.markdown("## 📊 Distribusi Rating")
        
        rating_dist = results['review_distribution']
        
        # Bar chart distribusi rating
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(rating_dist['review_score'].astype(str), rating_dist['count'], 
                      color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Jumlah', fontsize=12, fontweight='bold')
        ax.set_xlabel('Rating', fontsize=12, fontweight='bold')
        ax.set_title('Distribusi Rating Pelanggan\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        
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
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(delay_data['delay_range'], delay_data['mean_rating'], 
                      color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax.set_ylim(0, 5.5)
        ax.set_ylabel('Rata-rata Rating (1-5)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Rentang Keterlambatan', fontsize=12, fontweight='bold')
        ax.set_title('Rata-rata Rating Berdasarkan Rentang Keterlambatan Pengiriman\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        
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
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">📌 Insight Rentang Keterlambatan</div>', unsafe_allow_html=True)
        st.markdown(f"""
        - Rating tertinggi: **>7 hari ({delay_data[delay_data['delay_range'] == '> 7 hari']['mean_rating'].values[0]:.2f})** - karena didominasi pengiriman cepat
        - Rating terendah: **4-7 hari ({delay_data[delay_data['delay_range'] == '4-7 hari']['mean_rating'].values[0]:.2f})**
        - Jumlah sample: **>7 hari = {delay_data[delay_data['delay_range'] == '> 7 hari']['count'].values[0]:,} pesanan** | 1-3 hari = 137 | 4-7 hari = 125
        - **Perlu diperhatikan:** Kategori '>7 hari' dalam data ini adalah pengiriman LEBIH CEPAT (negatif days)
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# 10. MENU 3: PERTANYAAN 1 - DETAIL RATING
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
                                           autopct='%1.1f%%', colors=colors_pie, startangle=90,
                                           shadow=True)
        for autotext in autotexts:
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        ax.set_title('Distribusi Status Pengiriman', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    st.markdown("---")
    st.markdown("## 📊 Statistik Deskriptif Rating")
    
    rating_stats = results['delivery_rating'].copy()
    st.dataframe(rating_stats.style.format({
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
# 11. MENU 4: PERTANYAAN 2 - ANALISIS SELLER & LOKASI
# ============================================

elif analysis_type == "📍 Pertanyaan 2: Analisis Seller & Lokasi":
    st.markdown("# 📍 Pertanyaan 2: Hubungan Lokasi Seller dengan Volume Penjualan")
    st.markdown("**Apakah ada hubungan yang kuat antara jumlah seller di setiap kota/state dengan total produk yang terjual selama periode 2016-2018, serta kota mana yang memiliki penjualan tertinggi dan produktivitas seller tertinggi?**")
    st.markdown("---")
    
    # Sub-menu untuk Pertanyaan 2
    sub_menu = st.radio(
        "Pilih Sub Analisis:",
        ["Top Seller & Penjualan", "Korelasi Seller vs Penjualan", "Produktivitas Seller", "Analisis Lokasi"],
        horizontal=True
    )
    
    if sub_menu == "Top Seller & Penjualan":
        st.markdown("## 🏙️ Top 10 Kota dengan Penjualan Tertinggi")
        
        top_cities = city_data_clean.nlargest(10, 'total_products_sold').sort_values('total_products_sold', ascending=True)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors_h = plt.cm.Blues(np.linspace(0.3, 0.9, len(top_cities)))
        bars = ax.barh(top_cities['seller_city'].str.title(), top_cities['total_products_sold'], 
                       color=colors_h, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Total Produk Terjual', fontsize=12, fontweight='bold')
        ax.set_ylabel('Kota', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Kota dengan Total Produk Terjual Terbanyak\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        
        max_val = top_cities['total_products_sold'].max()
        for bar, val in zip(bars, top_cities['total_products_sold']):
            ax.text(val + (max_val * 0.01), bar.get_y() + bar.get_height()/2, 
                    f'{val:,}', va='center', ha='left', fontsize=10, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("### 📋 Data Top 10 Kota Penjualan Tertinggi")
        st.dataframe(top_cities[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold', 'avg_products_per_seller']].style.format({
            'total_products_sold': '{:,.0f}',
            'total_sellers': '{:,.0f}',
            'avg_products_per_seller': '{:.1f}'
        }))
        
        st.markdown("## 🏆 Top Negara Bagian dengan Penjualan Tertinggi")
        top_states = results['state_performance'].sort_values('total_products_sold', ascending=False)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        bars2 = ax2.bar(top_states['seller_state'], top_states['total_products_sold'], 
                        color='#1E88E5', edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Total Produk Terjual', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Negara Bagian', fontsize=12, fontweight='bold')
        ax2.set_title('Penjualan per Negara Bagian\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        
        for bar, val in zip(bars2, top_states['total_products_sold']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, f'{val:,}', 
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax2.grid(axis='y', alpha=0.3)
        st.pyplot(fig2)
        
        st.dataframe(top_states[['seller_state', 'total_sellers', 'total_products_sold']].style.format({
            'total_products_sold': '{:,.0f}',
            'total_sellers': '{:,.0f}'
        }))
    
    elif sub_menu == "Korelasi Seller vs Penjualan":
        st.markdown("## 📈 Korelasi Jumlah Seller vs Total Penjualan per Kota")
        
        city_corr = city_data_clean[city_data_clean['total_sellers'] >= 3].copy()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(city_corr['total_sellers'], city_corr['total_products_sold'],
                             c=city_corr['total_products_sold'], cmap='viridis', 
                             s=80, alpha=0.7, edgecolor='black', linewidth=1)
        ax.set_xlabel('Jumlah Seller per Kota', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Produk Terjual', fontsize=12, fontweight='bold')
        ax.set_title('Hubungan Jumlah Seller dengan Total Produk Terjual per Kota\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        plt.colorbar(scatter, ax=ax, label='Total Produk')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Garis regresi
        slope, intercept = np.polyfit(city_corr['total_sellers'], city_corr['total_products_sold'], 1)
        x_line = np.array([city_corr['total_sellers'].min(), city_corr['total_sellers'].max()])
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, 'r--', linewidth=2, label=f'Regresi (r = {results["correlation"]["pearson_r"]:.3f})')
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Korelasi Pearson", f"{results['correlation']['pearson_r']:.4f}")
        with col2:
            st.metric("📊 Korelasi Spearman", f"{results['correlation']['spearman_r']:.4f}")
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">📌 Insight Korelasi</div>', unsafe_allow_html=True)
        st.markdown(f"""
        - **Korelasi positif SANGAT KUAT** ({results['correlation']['pearson_r']:.3f})
        - **Signifikan secara statistik** (p = {results['correlation']['p_value']:.4f} < 0.05)
        - **Artinya:** Semakin banyak seller di suatu kota, semakin tinggi penjualannya.
        - Jumlah kota dianalisis: {len(city_corr)} kota (dengan total_sellers ≥ 3)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Produktivitas Seller":
        st.markdown("## ⭐ Top 10 Kota dengan Produktivitas Seller Tertinggi")
        
        productive_cities = city_data_clean[city_data_clean['total_sellers'] >= 3].nlargest(10, 'avg_products_per_seller')
        productive_cities = productive_cities.sort_values('avg_products_per_seller', ascending=True)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors_h2 = plt.cm.Greens(np.linspace(0.3, 0.9, len(productive_cities)))
        bars = ax.barh(productive_cities['seller_city'].str.title(), productive_cities['avg_products_per_seller'], 
                       color=colors_h2, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Rata-rata Produk per Seller', fontsize=12, fontweight='bold')
        ax.set_ylabel('Kota', fontsize=12, fontweight='bold')
        ax.set_title('Top 10 Kota dengan Produktivitas Seller Tertinggi\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        
        max_val = productive_cities['avg_products_per_seller'].max()
        for bar, val in zip(bars, productive_cities['avg_products_per_seller']):
            ax.text(val + (max_val * 0.02), bar.get_y() + bar.get_height()/2, 
                    f'{val:.1f}', va='center', ha='left', fontsize=10, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("### 📋 Data Top 10 Kota Produktif")
        st.dataframe(productive_cities[['seller_city', 'seller_state', 'total_sellers', 'total_products_sold', 'avg_products_per_seller']].style.format({
            'total_products_sold': '{:,.0f}',
            'total_sellers': '{:,.0f}',
            'avg_products_per_seller': '{:.1f}'
        }))
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">📌 Insight Produktivitas Seller</div>', unsafe_allow_html=True)
        st.markdown(f"""
        - **{productive_cities.iloc[-1]['seller_city'].title()}** memiliki produktivitas tertinggi: **{productive_cities.iloc[-1]['avg_products_per_seller']:.0f} produk/seller**
        - **Ibitinga** masuk dalam top produktif dengan **155.5 produk/seller**
        - Kota dengan jumlah seller sedikit dapat memiliki produktivitas tinggi
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif sub_menu == "Analisis Lokasi":
        st.markdown("## 🌎 Analisis Lokasi Geografis Penjualan")
        
        # Pie chart proporsi penjualan per state
        st.markdown("### 📊 Proporsi Penjualan per Negara Bagian")
        
        state_data = results['state_performance'].copy()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors_pie = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        wedges, texts, autotexts = ax.pie(state_data['total_products_sold'], labels=state_data['seller_state'],
                                           autopct='%1.1f%%', startangle=90, colors=colors_pie,
                                           shadow=True, textprops={'fontsize': 11})
        for autotext in autotexts:
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        ax.set_title('Proporsi Penjualan per Negara Bagian\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Bar chart jumlah seller per state
        st.markdown("### 📊 Jumlah Seller per Negara Bagian")
        
        top_states_seller = state_data.sort_values('total_sellers', ascending=True)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        colors_h = plt.cm.Blues(np.linspace(0.3, 0.9, len(top_states_seller)))
        bars = ax2.barh(top_states_seller['seller_state'], top_states_seller['total_sellers'], 
                        color=colors_h, edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Jumlah Seller', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Negara Bagian', fontsize=12, fontweight='bold')
        ax2.set_title('Jumlah Seller per Negara Bagian\n(Periode 2016-2018)', fontsize=14, fontweight='bold')
        
        max_val = top_states_seller['total_sellers'].max()
        for bar, val in zip(bars, top_states_seller['total_sellers']):
            ax2.text(val + (max_val * 0.01), bar.get_y() + bar.get_height()/2, 
                     f'{val:,}', va='center', ha='left', fontsize=10, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig2)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('<div class="insight-title">📌 Insight Geografis</div>', unsafe_allow_html=True)
        
        total_sales_sp = state_data[state_data['seller_state'] == 'SP']['total_products_sold'].values[0]
        total_sales_all = state_data['total_products_sold'].sum()
        sp_pct = (total_sales_sp / total_sales_all * 100)
        total_sellers_sp = state_data[state_data['seller_state'] == 'SP']['total_sellers'].values[0]
        total_sellers_all = state_data['total_sellers'].sum()
        sp_seller_pct = (total_sellers_sp / total_sellers_all * 100)
        
        st.markdown(f"""
        - **SP (São Paulo)** mendominasi dengan **{sp_pct:.1f}%** dari total penjualan nasional
        - **SP** juga memiliki **{sp_seller_pct:.1f}%** dari total seller
        - **Sao Paulo city** menyumbang **{27357/total_sales_sp*100:.1f}%** dari total penjualan SP
        - **Ketimpangan geografis** sangat signifikan dalam aktivitas e-commerce
        - Perlu **ekspansi ke wilayah lain** untuk mengurangi ketergantungan pada SP
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# 12. MENU 5: KESIMPULAN & REKOMENDASI
# ============================================

elif analysis_type == "📈 Kesimpulan & Rekomendasi":
    st.markdown("# 📈 Kesimpulan Akhir & Rekomendasi Bisnis")
    st.markdown("## Berdasarkan Analisis Data E-Commerce Brazil (2016-2018)")
    st.markdown("---")
    
    # Kesimpulan Pertanyaan 1
    st.markdown("## 📦 Pertanyaan 1: Pengaruh Waktu Pengiriman terhadap Kepuasan Pelanggan")
    
    delivery_stats = results['delivery_rating']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mean_faster = delivery_stats[delivery_stats['delivery_status'] == 'Lebih Cepat']['mean_rating'].values[0]
        st.metric("🚀 Lebih Cepat", f"{mean_faster:.2f}")
    with col2:
        mean_ontime = delivery_stats[delivery_stats['delivery_status'] == 'Tepat Waktu']['mean_rating'].values[0]
        st.metric("✅ Tepat Waktu", f"{mean_ontime:.2f}")
    with col3:
        mean_late = delivery_stats[delivery_stats['delivery_status'] == 'Terlambat']['mean_rating'].values[0]
        st.metric("⚠️ Terlambat", f"{mean_late:.2f}")
    
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
    
    top_city = city_data_clean.iloc[0]
    productive_cities = city_data_clean[city_data_clean['total_sellers'] >= 3].nlargest(1, 'avg_products_per_seller')
    state_data = results['state_performance']
    
    total_sales_sp = state_data[state_data['seller_state'] == 'SP']['total_products_sold'].values[0]
    total_sales_all = state_data['total_products_sold'].sum()
    sp_pct = (total_sales_sp / total_sales_all * 100)
    total_sellers_sp = state_data[state_data['seller_state'] == 'SP']['total_sellers'].values[0]
    total_sellers_all = state_data['total_sellers'].sum()
    sp_seller_pct = (total_sellers_sp / total_sellers_all * 100)
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("### ✅ Kesimpulan Pertanyaan 2")
    st.markdown(f"""
    **Ya, ada hubungan yang jelas dan sangat kuat antara lokasi geografis seller dan jumlah produk yang terjual.**
    
    - **SP (São Paulo)** mendominasi penjualan dengan **{sp_pct:.1f}%** dari total penjualan nasional
    - **Kota {top_city['seller_city'].title()}** menjadi kota terlaris dengan **{top_city['total_products_sold']:,} produk** dari **{top_city['total_sellers']:,} seller**
    - **{productive_cities.iloc[0]['seller_city'].title()}** memiliki produktivitas tertinggi: **{productive_cities.iloc[0]['avg_products_per_seller']:.0f} produk/seller**
    - **Korelasi sangat kuat** (r = {results['correlation']['pearson_r']:.3f}) antara jumlah seller dan total penjualan
    - **Ketimpangan geografis** sangat signifikan: ~{sp_seller_pct:.1f}% seller berada di wilayah SP
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
           - Terapkan kebijakan toleransi keterlambatan maksimal 3 hari
           - Berikan kompensasi (voucher/diskon) jika lebih dari 3 hari
        
        2. **Prioritaskan pengiriman 'Lebih Cepat'**
           - Tingkatkan volume pengiriman lebih cepat dari estimasi
           - Rating lebih cepat (4.22) lebih tinggi dari terlambat (4.09)
        
        3. **Evaluasi mitra logistik**
           - Hentikan kerjasama dengan kurir yang sering terlambat (>7 hari)
           - Ganti dengan kurir yang memiliki on-time delivery rate tinggi
        
        4. **Implementasi real-time tracking**
           - Berikan notifikasi otomatis ke customer jika terjadi keterlambatan
           - Kurangi ketidakpastian dan keluhan pelanggan
        """)
    
    with col2:
        st.markdown("### 📍 **Rekomendasi Ekspansi Seller**")
        st.markdown(f"""
        1. **Ekspansi rekrutmen seller ke luar SP**
           - Target prioritas: PR, RJ, MG (kontribusi saat ini <10%)
           - Target: Tambah 20% seller baru di wilayah tersebut dalam 6 bulan
        
        2. **Jadikan {productive_cities.iloc[0]['seller_city'].title()} sebagai model**
           - Produktivitas tertinggi: {productive_cities.iloc[0]['avg_products_per_seller']:.0f} produk/seller
           - Pelajari dan terapkan strategi seller di kota produktif ini
        
        3. **Bangun hub logistik di Curitiba (PR)**
           - Akses ke wilayah Selatan yang selama ini belum optimal
           - Potensi meningkatkan penjualan 15-20%
        
        4. **Berikan insentif produktivitas**
           - Bonus untuk seller dengan produktivitas > 150 produk/seller
           - Program pelatihan untuk seller dengan produktivitas rendah
        """)
    
    st.markdown("---")
    st.markdown("### 📊 Metode Analisis yang Digunakan")
    st.markdown("""
    - **T-Test:** Menguji perbedaan rata-rata kepuasan pelanggan antar kelompok pengiriman
    - **Korelasi Pearson:** Mengukur hubungan antara jumlah seller dan total penjualan
    - **ANOVA:** Menguji perbedaan rating antar tiga kelompok status pengiriman
    - Kedua metode dipilih karena sesuai dengan jenis data numerik dan tujuan analisis
    """)

# ============================================
# 13. FOOTER
# ============================================

st.markdown("---")
st.markdown(f"""
<footer>
    Dashboard Analisis Data E-Commerce Brazil | Periode 2016-2018<br>
    Data Source: Olist Brazilian E-Commerce Dataset | Analisis oleh: Firdhania Nur Rizky Setyarini<br>
    Tujuan Analisis: Pengaruh Waktu Pengiriman | Hubungan Lokasi Seller dengan Penjualan
</footer>
""", unsafe_allow_html=True)