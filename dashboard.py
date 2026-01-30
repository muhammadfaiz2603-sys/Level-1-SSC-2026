import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="SSC 2026 Explorer", layout="wide")

# Custom CSS for metric cards
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #d6d6d6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING (Hardcoded from your new CSV files)
# -----------------------------------------------------------------------------

# --- A. REGIONAL PERFORMANCE (Source: Region Performance Comparison.csv) ---
df_regional = pd.DataFrame({
    'Region': ['Central', 'East Coast', 'Northern', 'Sabah', 'Sarawak', 'Southern'],
    'Fail': [84, 20, 64, 42, 27, 70],
    'Pass': [48, 25, 64, 23, 33, 33],
    'Total Headcount': [132, 45, 128, 65, 60, 103]
})

# --- B. OUTLET PERFORMANCE (Combined from all individual regional CSVs) ---
# I have combined all your individual files (Central.csv, Northern.csv, etc.) here.
data_outlets = [
    # Central
    {'Outlet': 'AP', 'Pass': 1, 'Fail': 4, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'BG', 'Pass': 2, 'Fail': 2, 'Total': 4, 'Region': 'Central'},
    {'Outlet': 'BK', 'Pass': 2, 'Fail': 2, 'Total': 4, 'Region': 'Central'},
    {'Outlet': 'BV', 'Pass': 3, 'Fail': 2, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'EK', 'Pass': 2, 'Fail': 3, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'EV', 'Pass': 2, 'Fail': 3, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'LY', 'Pass': 2, 'Fail': 3, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'MF', 'Pass': 4, 'Fail': 2, 'Total': 6, 'Region': 'Central'},
    {'Outlet': 'MT', 'Pass': 4, 'Fail': 2, 'Total': 6, 'Region': 'Central'},
    {'Outlet': 'PR', 'Pass': 3, 'Fail': 2, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'PS', 'Pass': 0, 'Fail': 5, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'PU', 'Pass': 0, 'Fail': 5, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'PY', 'Pass': 2, 'Fail': 14, 'Total': 16, 'Region': 'Central'},
    {'Outlet': 'QS', 'Pass': 1, 'Fail': 4, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'SA', 'Pass': 3, 'Fail': 4, 'Total': 7, 'Region': 'Central'},
    {'Outlet': 'SL', 'Pass': 5, 'Fail': 0, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'SWKLAA', 'Pass': 1, 'Fail': 2, 'Total': 3, 'Region': 'Central'},
    {'Outlet': 'SWKLGC', 'Pass': 1, 'Fail': 3, 'Total': 4, 'Region': 'Central'},
    {'Outlet': 'SWSGKG', 'Pass': 2, 'Fail': 1, 'Total': 3, 'Region': 'Central'},
    {'Outlet': 'SWSGKW', 'Pass': 3, 'Fail': 2, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'SWSGSY', 'Pass': 1, 'Fail': 4, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'TG', 'Pass': 2, 'Fail': 5, 'Total': 7, 'Region': 'Central'},
    {'Outlet': 'UK', 'Pass': 0, 'Fail': 1, 'Total': 1, 'Region': 'Central'},
    {'Outlet': 'UP', 'Pass': 0, 'Fail': 5, 'Total': 5, 'Region': 'Central'},
    {'Outlet': 'WW', 'Pass': 2, 'Fail': 4, 'Total': 6, 'Region': 'Central'},
    # Northern
    {'Outlet': 'AC', 'Pass': 2, 'Fail': 5, 'Total': 7, 'Region': 'Northern'},
    {'Outlet': 'AJ', 'Pass': 5, 'Fail': 3, 'Total': 8, 'Region': 'Northern'},
    {'Outlet': 'AL', 'Pass': 4, 'Fail': 3, 'Total': 7, 'Region': 'Northern'},
    {'Outlet': 'AR', 'Pass': 0, 'Fail': 8, 'Total': 8, 'Region': 'Northern'},
    {'Outlet': 'AS', 'Pass': 0, 'Fail': 5, 'Total': 5, 'Region': 'Northern'},
    {'Outlet': 'BM', 'Pass': 2, 'Fail': 4, 'Total': 6, 'Region': 'Northern'},
    {'Outlet': 'GT', 'Pass': 7, 'Fail': 7, 'Total': 14, 'Region': 'Northern'},
    {'Outlet': 'KI', 'Pass': 2, 'Fail': 3, 'Total': 5, 'Region': 'Northern'},
    {'Outlet': 'LW', 'Pass': 3, 'Fail': 2, 'Total': 5, 'Region': 'Northern'},
    {'Outlet': 'PG', 'Pass': 5, 'Fail': 2, 'Total': 7, 'Region': 'Northern'},
    {'Outlet': 'QB', 'Pass': 6, 'Fail': 9, 'Total': 15, 'Region': 'Northern'},
    {'Outlet': 'SQ', 'Pass': 4, 'Fail': 1, 'Total': 5, 'Region': 'Northern'},
    {'Outlet': 'SU', 'Pass': 13, 'Fail': 0, 'Total': 13, 'Region': 'Northern'},
    {'Outlet': 'SWKDSW', 'Pass': 4, 'Fail': 0, 'Total': 4, 'Region': 'Northern'},
    {'Outlet': 'TM', 'Pass': 1, 'Fail': 5, 'Total': 6, 'Region': 'Northern'},
    {'Outlet': 'TS', 'Pass': 0, 'Fail': 7, 'Total': 7, 'Region': 'Northern'},
    {'Outlet': 'VM', 'Pass': 6, 'Fail': 0, 'Total': 6, 'Region': 'Northern'},
    # Southern
    {'Outlet': 'BP', 'Pass': 2, 'Fail': 5, 'Total': 7, 'Region': 'Southern'},
    {'Outlet': 'JB', 'Pass': 2, 'Fail': 9, 'Total': 11, 'Region': 'Southern'},
    {'Outlet': 'KJ', 'Pass': 0, 'Fail': 7, 'Total': 7, 'Region': 'Southern'},
    {'Outlet': 'KP', 'Pass': 2, 'Fail': 2, 'Total': 4, 'Region': 'Southern'},
    {'Outlet': 'MP', 'Pass': 4, 'Fail': 0, 'Total': 4, 'Region': 'Southern'},
    {'Outlet': 'NL', 'Pass': 6, 'Fail': 2, 'Total': 8, 'Region': 'Southern'},
    {'Outlet': 'PD', 'Pass': 5, 'Fail': 7, 'Total': 12, 'Region': 'Southern'},
    {'Outlet': 'SC', 'Pass': 1, 'Fail': 5, 'Total': 6, 'Region': 'Southern'},
    {'Outlet': 'SG', 'Pass': 3, 'Fail': 3, 'Total': 6, 'Region': 'Southern'},
    {'Outlet': 'SR', 'Pass': 0, 'Fail': 7, 'Total': 7, 'Region': 'Southern'},
    {'Outlet': 'SWJHBX', 'Pass': 1, 'Fail': 3, 'Total': 4, 'Region': 'Southern'},
    {'Outlet': 'SWJHDS', 'Pass': 0, 'Fail': 5, 'Total': 5, 'Region': 'Southern'},
    {'Outlet': 'SWJHEL', 'Pass': 0, 'Fail': 5, 'Total': 5, 'Region': 'Southern'},
    {'Outlet': 'SWJHGP', 'Pass': 2, 'Fail': 3, 'Total': 5, 'Region': 'Southern'},
    {'Outlet': 'SWNSLJ', 'Pass': 1, 'Fail': 3, 'Total': 4, 'Region': 'Southern'},
    {'Outlet': 'SWNSLT', 'Pass': 0, 'Fail': 3, 'Total': 3, 'Region': 'Southern'},
    {'Outlet': 'WE', 'Pass': 4, 'Fail': 1, 'Total': 5, 'Region': 'Southern'},
    # East Coast
    {'Outlet': 'EC', 'Pass': 4, 'Fail': 3, 'Total': 7, 'Region': 'East Coast'},
    {'Outlet': 'KA', 'Pass': 7, 'Fail': 0, 'Total': 7, 'Region': 'East Coast'},
    {'Outlet': 'KM', 'Pass': 2, 'Fail': 4, 'Total': 6, 'Region': 'East Coast'},
    {'Outlet': 'KT', 'Pass': 3, 'Fail': 1, 'Total': 4, 'Region': 'East Coast'},
    {'Outlet': 'MM', 'Pass': 3, 'Fail': 0, 'Total': 3, 'Region': 'East Coast'},
    {'Outlet': 'SWPHCH', 'Pass': 0, 'Fail': 4, 'Total': 4, 'Region': 'East Coast'},
    {'Outlet': 'SWPHLK', 'Pass': 1, 'Fail': 3, 'Total': 4, 'Region': 'East Coast'},
    {'Outlet': 'SWTRGD', 'Pass': 0, 'Fail': 5, 'Total': 5, 'Region': 'East Coast'},
    {'Outlet': 'SWTRMY', 'Pass': 5, 'Fail': 0, 'Total': 5, 'Region': 'East Coast'},
    # Sabah
    {'Outlet': 'HS', 'Pass': 6, 'Fail': 0, 'Total': 6, 'Region': 'Sabah'},
    {'Outlet': 'IG', 'Pass': 7, 'Fail': 12, 'Total': 19, 'Region': 'Sabah'},
    {'Outlet': 'PQ', 'Pass': 2, 'Fail': 5, 'Total': 7, 'Region': 'Sabah'},
    {'Outlet': 'SS', 'Pass': 0, 'Fail': 10, 'Total': 10, 'Region': 'Sabah'},
    {'Outlet': 'SWLBFP', 'Pass': 0, 'Fail': 4, 'Total': 4, 'Region': 'Sabah'},
    {'Outlet': 'SWSBCC', 'Pass': 0, 'Fail': 3, 'Total': 3, 'Region': 'Sabah'},
    {'Outlet': 'SWSBCM', 'Pass': 3, 'Fail': 2, 'Total': 5, 'Region': 'Sabah'},
    {'Outlet': 'SWSBKK', 'Pass': 1, 'Fail': 3, 'Total': 4, 'Region': 'Sabah'},
    {'Outlet': 'TW', 'Pass': 4, 'Fail': 3, 'Total': 7, 'Region': 'Sabah'},
    # Sarawak
    {'Outlet': 'CK', 'Pass': 4, 'Fail': 3, 'Total': 7, 'Region': 'Sarawak'},
    {'Outlet': 'MB', 'Pass': 5, 'Fail': 0, 'Total': 5, 'Region': 'Sarawak'},
    {'Outlet': 'MR', 'Pass': 1, 'Fail': 4, 'Total': 5, 'Region': 'Sarawak'},
    {'Outlet': 'SB', 'Pass': 5, 'Fail': 0, 'Total': 5, 'Region': 'Sarawak'},
    {'Outlet': 'SP', 'Pass': 8, 'Fail': 4, 'Total': 12, 'Region': 'Sarawak'},
    {'Outlet': 'SWSWDM', 'Pass': 2, 'Fail': 3, 'Total': 5, 'Region': 'Sarawak'},
    {'Outlet': 'SWSWER', 'Pass': 1, 'Fail': 4, 'Total': 5, 'Region': 'Sarawak'},
    {'Outlet': 'SY', 'Pass': 1, 'Fail': 5, 'Total': 6, 'Region': 'Sarawak'},
    {'Outlet': 'VC', 'Pass': 6, 'Fail': 4, 'Total': 10, 'Region': 'Sarawak'},
]
df_outlets = pd.DataFrame(data_outlets)

# --- C. LOB COMPARISON (Source: LOB COMPARISON.csv) ---
df_lob = pd.DataFrame({
    'Result': [
        'Apple Watch & iPhone (Fail)', 
        'Apple Watch & iPhone (Pass)', 
        'iPad (Fail)', 
        'iPad (Pass)', 
        'Mac (Fail)', 
        'Mac (Pass)'
    ],
    'Central': [48, 84, 0, 0, 0, 0],
    'Sarawak': [27, 33, 0, 0, 0, 0],
    'Sabah': [42, 23, 0, 0, 0, 0],
    'East Coast': [20, 25, 0, 0, 0, 0],
    'Southern': [70, 33, 0, 0, 0, 0],
    'Northern': [64, 64, 0, 0, 0, 0]
})

# Function to clean and structure LOB data
def process_lob_data(df):
    # Melt to long format
    df_long = df.melt(id_vars=['Result'], var_name='Region', value_name='Count')
    
    # Extract Status (Pass/Fail) and Product
    # Logic: Split by " (" to separate "iPhone" from "Pass)"
    df_long['Status'] = df_long['Result'].apply(lambda x: 'Pass' if '(Pass)' in x else 'Fail')
    df_long['Product'] = df_long['Result'].apply(lambda x: x.split(' (')[0])
    
    # Filter out 0 counts to make charts cleaner
    df_long = df_long[df_long['Count'] > 0]
    
    return df_long

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    html.Img(src=dash.get_asset_url('Main Banner.png'), style={'width': '100%'})
    st.header("SSC 2026 Dashboard : Explorer")
    view_selection = st.selectbox(
        "Select Dataset:",
        ["Regional Performance", "Outlet Performance", "LOB Comparison"]
    )
    st.markdown("---")
    st.caption("© 2026 SSC 2026 | Insight Team")

# -----------------------------------------------------------------------------
# 4. MAIN LOGIC
# -----------------------------------------------------------------------------

st.title(f"📊 {view_selection}")

# Initialize variables
fig = None
display_df = None
total_vol = 0
total_pass = 0
total_fail = 0

# --- LOGIC: REGIONAL VIEW ---
if view_selection == "Regional Performance":
    display_df = df_regional
    
    total_pass = display_df['Pass'].sum()
    total_fail = display_df['Fail'].sum()
    total_vol = display_df['Total Headcount'].sum()
    
    # Chart
    chart_df = display_df.melt(id_vars=['Region'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
    fig = px.bar(chart_df, x='Region', y='Count', color='Status', barmode='group',
                 text_auto=True,
                 color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'},
                 title="Pass vs Fail by Region")

# --- LOGIC: OUTLET VIEW ---
elif view_selection == "Outlet Performance":
    
    # Add a sub-filter because there are too many outlets to show all at once
    selected_region_filter = st.selectbox("Filter by Region:", ["All"] + list(df_outlets['Region'].unique()))
    
    if selected_region_filter != "All":
        display_df = df_outlets[df_outlets['Region'] == selected_region_filter]
    else:
        display_df = df_outlets

    total_pass = display_df['Pass'].sum()
    total_fail = display_df['Fail'].sum()
    total_vol = display_df['Total'].sum()
    
    # Chart
    chart_df = display_df.melt(id_vars=['Outlet'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
    
    # Sort by Volume so biggest outlets are first
    chart_df = chart_df.sort_values(by='Count', ascending=False)
    
    fig = px.bar(chart_df, x='Outlet', y='Count', color='Status', barmode='group',
                 text_auto=True,
                 color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'},
                 title=f"Outlet Performance ({selected_region_filter})")

# --- LOGIC: LOB VIEW ---
elif view_selection == "LOB Comparison":
    processed_lob = process_lob_data(df_lob)
    display_df = processed_lob[['Region', 'Product', 'Status', 'Count']]
    
    total_pass = processed_lob[processed_lob['Status'] == 'Pass']['Count'].sum()
    total_fail = processed_lob[processed_lob['Status'] == 'Fail']['Count'].sum()
    total_vol = total_pass + total_fail
    
    # Chart
    fig = px.bar(processed_lob, x='Product', y='Count', color='Status', 
                 color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'},
                 text_auto=True,
                 facet_col='Region', title="Product Performance by Region")
    fig.update_xaxes(matches=None) # Allows x-axis labels to fit better

# -----------------------------------------------------------------------------
# 5. DASHBOARD LAYOUT (KPIs -> Chart -> Table)
# -----------------------------------------------------------------------------

pass_rate = (total_pass / total_vol) * 100 if total_vol > 0 else 0

# Row 1: KPI Cards
st.subheader("1. Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Volume", f"{total_vol:,}")
col2.metric("Total Pass", f"{total_pass:,}")
col3.metric("Total Fail", f"{total_fail:,}")
col4.metric("Pass Rate", f"{pass_rate:.1f}%")

st.markdown("---")

# Row 2: Charts
st.subheader("2. Graphical Analysis")
if fig:
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 3: Data Table
st.subheader("3. Source Data")
with st.expander("View Data Table", expanded=True):
    st.dataframe(display_df, use_container_width=True)
