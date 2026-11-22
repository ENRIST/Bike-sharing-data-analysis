import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load data dengan relative path aman untuk lokal maupun Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "main_data.csv")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

main_df = load_data(DATA_PATH)

# --- SIDEBAR FILTERS ---
st.sidebar.title("🚲 Bike Sharing")
st.sidebar.header("Filter Data")

min_date = main_df['dteday'].min().date()
max_date = main_df['dteday'].max().date()

date_range = st.sidebar.date_input(
    label="Rentang Tanggal",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Penanganan aman saat pengguna baru memilih 1 tanggal di kalender
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, tuple) and len(date_range) == 1:
    start_date = end_date = date_range[0]
else:
    start_date = end_date = date_range

selected_seasons = st.sidebar.multiselect(
    label="Pilih Musim",
    options=['Spring', 'Summer', 'Fall', 'Winter'],
    default=['Spring', 'Summer', 'Fall', 'Winter']
)

selected_day_types = st.sidebar.multiselect(
    label="Pilih Tipe Hari",
    options=['Working Day', 'Weekend/Holiday'],
    default=['Working Day', 'Weekend/Holiday']
)

filtered_df = main_df[
    (main_df['dteday'].dt.date >= start_date) &
    (main_df['dteday'].dt.date <= end_date) &
    (main_df['season_label'].isin(selected_seasons)) &
    (main_df['day_type'].isin(selected_day_types))
]

if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan kombinasi filter. Silakan ubah pilihan pada sidebar.")
    st.stop()

# Agregasi ke level harian untuk KPI dan grafik Pertanyaan 1
daily_df = filtered_df.groupby(
    ['dteday', 'season_label', 'daily_weather_label', 'daily_temp_bin'],
    observed=True
)[['casual', 'registered', 'cnt']].sum().reset_index()

# --- HEADER & KPI METRICS ---
st.title("Bike Sharing Analytics Dashboard (2011–2012)")
st.markdown(
    "Dashboard interaktif untuk mengevaluasi pengaruh musim, cuaca, suhu, serta pola jam operasional "
    "terhadap performa penyewaan sepeda Capital Bikeshare."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penyewaan", f"{daily_df['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{daily_df['cnt'].mean():,.0f}")
col3.metric("Pengguna Registered", f"{daily_df['registered'].sum():,}")
col4.metric("Pengguna Casual", f"{daily_df['casual'].sum():,}")

st.divider()

# --- BAGIAN 1: PERTANYAAN 1 (MUSIM & CUACA) ---
st.subheader("1. Pengaruh Musim dan Kondisi Cuaca terhadap Penyewaan Harian")
c1, c2 = st.columns(2)

with c1:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    season_avg = daily_df.groupby('season_label')['cnt'].mean().sort_values(ascending=False).reset_index()
    colors_season = [
        '#1f77b4' if i == 0 else ('#d62728' if i == len(season_avg) - 1 and len(season_avg) > 1 else '#d3d3d3')
        for i in range(len(season_avg))
    ]
    bars = ax.bar(season_avg['season_label'], season_avg['cnt'], color=colors_season, width=0.55)
    ax.set_title("Rata-rata Penyewaan Harian per Musim", fontsize=12, fontweight='bold')
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan Harian")
    ax.set_ylim(0, max(season_avg['cnt'].max() * 1.18, 100))
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,.0f}", (bar.get_x() + bar.get_width() / 2, h + season_avg['cnt'].max() * 0.02),
                    ha='center', fontsize=10, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    st.pyplot(fig)
    plt.close(fig)

with c2:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    weather_avg = daily_df.groupby('daily_weather_label')['cnt'].mean().sort_values(ascending=False).reset_index()
    colors_weather = [
        '#1f77b4' if i == 0 else ('#d62728' if i == len(weather_avg) - 1 and len(weather_avg) > 1 else '#d3d3d3')
        for i in range(len(weather_avg))
    ]
    bars = ax.bar(weather_avg['daily_weather_label'], weather_avg['cnt'], color=colors_weather, width=0.5)
    ax.set_title("Rata-rata Penyewaan Harian per Kondisi Cuaca", fontsize=12, fontweight='bold')
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Harian")
    ax.set_ylim(0, max(weather_avg['cnt'].max() * 1.18, 100))
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,.0f}", (bar.get_x() + bar.get_width() / 2, h + weather_avg['cnt'].max() * 0.02),
                    ha='center', fontsize=10, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# --- BAGIAN 2: PERTANYAAN 2 (POLA PER JAM & TIPE PENGGUNA) ---
st.subheader("2. Pola Penyewaan per Jam & Segmen Pengguna (Working Day vs Weekend/Holiday)")
c3, c4 = st.columns([1.4, 1])

with c3:
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    hourly_avg = filtered_df.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()
    sns.lineplot(
        data=hourly_avg, x='hr', y='cnt', hue='day_type',
        palette={'Working Day': '#1f77b4', 'Weekend/Holiday': '#ff7f0e'},
        marker='o', linewidth=2.2, ax=ax
    )
    ax.set_title("Rata-rata Penyewaan per Jam (00.00–23.00)", fontsize=12, fontweight='bold')
    ax.set_xlabel("Jam Operasional")
    ax.set_ylabel("Rata-rata Penyewaan per Jam")
    ax.set_xticks(range(0, 24, 2))
    ax.set_ylim(0, max(hourly_avg['cnt'].max() * 1.15, 50))
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(title="Tipe Hari")
    ax.spines[['top', 'right']].set_visible(False)
    st.pyplot(fig)
    plt.close(fig)

with c4:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    user_avg = filtered_df.groupby('day_type')[['registered', 'casual']].mean().reset_index().melt(
        id_vars='day_type', var_name='Tipe Pengguna', value_name='Rata-rata per Jam'
    )
    user_avg['Tipe Pengguna'] = user_avg['Tipe Pengguna'].map({'registered': 'Registered', 'casual': 'Casual'})
    sns.barplot(
        data=user_avg, x='day_type', y='Rata-rata per Jam', hue='Tipe Pengguna',
        palette={'Registered': '#1f77b4', 'Casual': '#ff7f0e'}, ax=ax
    )
    ax.set_title("Rata-rata Registered vs Casual per Jam", fontsize=12, fontweight='bold')
    ax.set_xlabel("Tipe Hari")
    ax.set_ylabel("Rata-rata Penyewaan per Jam")
    ax.set_ylim(0, max(user_avg['Rata-rata per Jam'].max() * 1.2, 20))
    for p in ax.patches:
        h = p.get_height()
        if pd.notna(h) and h > 0:
            ax.annotate(f"{h:.1f}", (p.get_x() + p.get_width() / 2, h + user_avg['Rata-rata per Jam'].max() * 0.025),
                        ha='center', fontsize=9, fontweight='bold')
    ax.legend(title="Tipe Pengguna")
    ax.spines[['top', 'right']].set_visible(False)
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# --- BAGIAN 3: ANALISIS LANJUTAN (CLUSTERING & BINNING) ---
st.subheader("3. Analisis Lanjutan: Klaster Waktu Operasional & Binning Suhu Harian")
c5, c6 = st.columns([1.3, 1])

with c5:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    cluster_order = ['Morning Rush (06-09)', 'Midday (10-15)', 'Evening Rush (16-19)', 'Night/Early Morning (20-05)']
    sns.barplot(
        data=filtered_df, x='time_cluster', y='cnt', hue='day_type',
        order=cluster_order, estimator='mean', errorbar=None,
        palette={'Working Day': '#1f77b4', 'Weekend/Holiday': '#ff7f0e'}, ax=ax
    )
    ax.set_title("Rata-rata Penyewaan per Klaster Waktu", fontsize=12, fontweight='bold')
    ax.set_xlabel("Klaster Waktu")
    ax.set_ylabel("Rata-rata Penyewaan per Jam")
    ax.tick_params(axis='x', rotation=12)
    cluster_max = filtered_df.groupby(['time_cluster', 'day_type'])['cnt'].mean().max()
    ax.set_ylim(0, max(cluster_max * 1.18, 50))
    for p in ax.patches:
        h = p.get_height()
        if pd.notna(h) and h > 0:
            ax.annotate(f"{h:.0f}", (p.get_x() + p.get_width() / 2, h + cluster_max * 0.02),
                        ha='center', fontsize=9, fontweight='bold')
    ax.legend(title="Tipe Hari")
    ax.spines[['top', 'right']].set_visible(False)
    st.pyplot(fig)
    plt.close(fig)

with c6:
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    temp_order = ['Cool (<15°C)', 'Mild (15-25°C)', 'Warm (>25°C)']
    temp_avg = daily_df.groupby('daily_temp_bin', observed=False)['cnt'].mean().reindex(temp_order).dropna().reset_index()
    color_map_temp = {'Cool (<15°C)': '#d3d3d3', 'Mild (15-25°C)': '#6baed6', 'Warm (>25°C)': '#1f77b4'}
    colors_temp = [color_map_temp[t] for t in temp_avg['daily_temp_bin']]
    bars = ax.bar(temp_avg['daily_temp_bin'], temp_avg['cnt'], color=colors_temp, width=0.55)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Kategori Suhu", fontsize=12, fontweight='bold')
    ax.set_xlabel("Kategori Suhu Harian")
    ax.set_ylabel("Rata-rata Penyewaan Harian")
    ax.set_ylim(0, max(temp_avg['cnt'].max() * 1.18, 100))
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:,.0f}", (bar.get_x() + bar.get_width() / 2, h + temp_avg['cnt'].max() * 0.02),
                    ha='center', fontsize=10, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    st.pyplot(fig)
    plt.close(fig)

st.caption("Sumber data: Kaggle (Capital Bikeshare System (2011–2012)) | Proyek Analisis Data")