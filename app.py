import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. PŘÍPRAVA DAT (Už jsem to přepsal z obrázků, nemáš zač 😉) ---

android_data = {
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'MAU': [45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000],
    'New Users': [4790, 4896, 4987, 5088, 5187, 5285, 5384, 5482, 5581, 5679, 5778, 5876],
    'Sessions': [765000, 850000, 935000, 1020000, 1105000, 1120000, 1200000, 1280000, 1445000, 1530000, 1615000, 1700000],
    'Courses Purchased': [18000, 20500, 22660, 25200, 27235, 31500, 33000, 34800, 39100, 40500, 40850, 46000],
    'Income': [540000, 615000, 679800, 756000, 817050, 945000, 990000, 1044000, 1173000, 1215000, 1225500, 1380000],
    'Maintenance Cost': [15000] * 12,
    'Acquisition Cost': [23950, 24480, 24935, 25440, 25933, 26425, 26918, 27410, 27903, 28395, 28888, 29380]
}

ios_data = {
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'MAU': [25000, 28000, 31000, 34000, 37000, 40000, 43000, 46000, 49000, 52000, 55000, 58000],
    'New Users': [2756, 2898, 2967, 3085, 3190, 3296, 3401, 3507, 3612, 3718, 3823, 3929],
    'Sessions': [500000, 560000, 620000, 680000, 740000, 760000, 817000, 874000, 980000, 1040000, 1100000, 1160000],
    'Courses Purchased': [17500, 20160, 22320, 24820, 27195, 28800, 30100, 34500, 36505, 39520, 40700, 42804],
    'Income': [525000, 604800, 669600, 744600, 815850, 864000, 903000, 1035000, 1095150, 1185600, 1221000, 1284120],
    'Maintenance Cost': [15000] * 12,
    'Acquisition Cost': [16536, 17388, 17802, 18508, 19141, 19774, 20407, 21040, 21673, 22306, 22939, 23572]
}

df_android = pd.DataFrame(android_data)
df_android['Platform'] = 'Android'
df_ios = pd.DataFrame(ios_data)
df_ios['Platform'] = 'iOS'

# Spojení do jednoho velkého dataframe
df = pd.concat([df_android, df_ios])

# --- 2. VÝPOČTY (Tady děláme magii s čísly) ---

# Total Costs
df['Total Cost'] = df['Maintenance Cost'] + df['Acquisition Cost']
# Profit
df['Profit'] = df['Income'] - df['Total Cost']
# ROI (%) = (Net Profit / Cost) * 100
df['ROI %'] = ((df['Income'] - df['Total Cost']) / df['Total Cost']) * 100
# ARPU (Average Revenue Per User) - Income / MAU
df['ARPU'] = df['Income'] / df['MAU']
# Conversion Rate (Courses Purchased / MAU) - kolik % aktivních uživatelů nakoupí
df['Conversion Rate %'] = (df['Courses Purchased'] / df['MAU']) * 100
# Average Order Value (AOV) - Income / Courses Purchased
df['Avg Course Price'] = df['Income'] / df['Courses Purchased']

# --- 3. UI APLIKACE (Streamlit) ---

st.set_page_config(page_title="Deep Dive Analysis", layout="wide")

st.title("📊 Deep Dive Analysis: iOS vs Android")
st.markdown("*Analýza efektivity platforem pro vzdělávací aplikaci*")

# Sidebar filtry
st.sidebar.header("Nastavení")
selected_metric = st.sidebar.selectbox(
    "Vyber metriku k porovnání:",
    ["Income", "Profit", "ROI %", "ARPU", "Conversion Rate %", "Courses Purchased", "MAU"]
)

# --- HLAVNÍ METRIKY (KPIs) ---
st.header("1. Rychlý přehled (Totals)")
col1, col2, col3 = st.columns(3)

total_income = df.groupby('Platform')['Income'].sum()
total_profit = df.groupby('Platform')['Profit'].sum()
avg_roi = df.groupby('Platform')['ROI %'].mean()

with col1:
    st.metric("Total Income iOS", f"{total_income['iOS']:,.0f} Kč", delta="vs Android")
    st.metric("Total Income Android", f"{total_income['Android']:,.0f} Kč")
with col2:
    st.metric("Total Profit iOS", f"{total_profit['iOS']:,.0f} Kč")
    st.metric("Total Profit Android", f"{total_profit['Android']:,.0f} Kč")
with col3:
    st.metric("Avg ROI iOS", f"{avg_roi['iOS']:.1f} %")
    st.metric("Avg ROI Android", f"{avg_roi['Android']:.1f} %")

st.info("💡 **První postřeh:** Android má vyšší absolutní čísla (více uživatelů), ale podívejme se na efektivitu níže.")

# --- GRAFY ---
st.header(f"2. Vývoj v čase: {selected_metric}")

fig = px.line(df, x='Month', y=selected_metric, color='Platform', markers=True,
              title=f"{selected_metric} over Time", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Scatter plot: Efektivita (Income vs MAU)
st.subheader("Efektivita uživatelů")
fig_scatter = px.scatter(df, x='MAU', y='Income', color='Platform', size='Profit',
                         hover_data=['Month', 'ROI %'], title="Income vs MAU (Velikost bubliny = Profit)")
st.plotly_chart(fig_scatter, use_container_width=True)

# --- KPI SEKCE ---
st.header("3. Návrh KPI a Interpretace")
col_kpi1, col_kpi2 = st.columns(2)

with col_kpi1:
    st.markdown("### 🏆 Vítěz: iOS")
    st.markdown("""
    Ačkoliv má Android **více uživatelů (MAU)**, iOS je brutálně efektivnější.
    - **ARPU (Příjem na uživatele):** iOS uživatelé utrácejí výrazně více.
    - **Konverze:** iOS má mnohem vyšší % nákupů vzhledem k počtu uživatelů.
    - **Retence (z doplňkových dat):** iOS 87% vs Android 69%.
    """)

with col_kpi2:
    st.markdown("### 🎯 Navrhovaná KPIs")
    st.markdown("""
    1. **ARPU (Average Revenue Per User)** - Ukazuje kvalitu uživatelské základny.
    2. **Conversion Rate (Prodej / MAU)** - Jak dobře aplikace prodává.
    3. **Retention Rate (3-month)** - Klíčové pro dlouhodobý profit, kde iOS drtí Android.
    """)

# --- DODATEČNÁ DATA & FUNNEL ---
st.header("4. Funnel & Purchase Path Optimization")

# Funnel Data
funnel_data = dict(
    number=[100, 70, 45, 25, 19],
    stage=["1. General Desc", "2. Detailed Desc", "3. Registration", "4. Payment Method", "5. Transaction"]
)
fig_funnel = px.funnel(funnel_data, x='number', y='stage', title="Nákupní trychtýř (Conversion Funnel)")
st.plotly_chart(fig_funnel, use_container_width=True)

st.error("⚠️ **Kritický bod:** Mezi krokem 3 (Registrace) a 4 (Výběr platby) ztrácíme 20 procentních bodů (45% -> 25%). Tady to lidé vzdávají. Je registrace moc složitá? Nebo se leknou ceny před platbou?")

# Závěrečná tabulka pro geeky
with st.expander("Zobrazit raw data (pro kontrolu)"):
    st.dataframe(df)