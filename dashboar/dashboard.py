import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📊 E-Commerce Data Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    return df

df = load_data()

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("Filter Data")

category = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=df['product_category_name_english'].unique(),
    default=df['product_category_name_english'].unique()
)

df_filtered = df[df['product_category_name_english'].isin(category)]

# ===============================
# METRIC
# ===============================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", df_filtered['order_id'].nunique())
col2.metric("Total Revenue", f"${df_filtered['price'].sum():,.2f}")
col3.metric("Total Products", df_filtered['product_id'].nunique())

# ===============================
# TOP CATEGORY
# ===============================
st.subheader("🏆 Top 10 Kategori Produk")

category_sales = (
    df_filtered.groupby('product_category_name_english')['price']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots()
category_sales.plot(kind='bar', ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# ===============================
# TREND BULANAN
# ===============================
st.subheader("📈 Tren Order Bulanan")

monthly_orders = (
    df_filtered.groupby('month')['order_id']
    .nunique()
)

fig2, ax2 = plt.subplots()
monthly_orders.plot(ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# ===============================
# INSIGHT
# ===============================
st.subheader("💡 Insight")

st.write("""
- Penjualan didominasi oleh beberapa kategori utama
- Terjadi peningkatan order pada akhir tahun
- Terdapat fluktuasi order bulanan
""")

# ===============================
# RECOMMENDATION
# ===============================
st.subheader("🚀 Recommendations")

st.write("""
1. Fokus pada kategori dengan penjualan tinggi
2. Optimalkan kategori dengan performa rendah
3. Maksimalkan campaign pada akhir tahun
4. Buat strategi promo di bulan sepi
""")
