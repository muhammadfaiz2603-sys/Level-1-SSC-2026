import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Level 1 Dashboard", layout="wide")

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
# 2. DATA LOADING & PREPARATION
# -----------------------------------------------------------------------------

# 1. Regional Performance
df_regional = pd.DataFrame({
    'Region': ['Central', 'Northern', 'Southern', 'East Coast', 'Sabah', 'Sarawak'],
    'Pass': [73, 48, 49, 55, 42, 36],
    'Fail': [25, 16, 13, 12, 8, 14],
    'Total Headcount': [98, 64, 62, 67, 50, 50]
})

# 2. Outlet Performance
df_outlet = pd.DataFrame({
    'Outlet': ['MT', 'PY', 'EV', 'MF'],
    'Pass': [4, 5, 3, 1],
    'Fail': [2, 3, 2, 4]
})

# 3. LOB Comparison
# Note: Fixed capitalization for 'Sarawak' to match other datasets
df_lob = pd.DataFrame({
    'Result': [
        'iPhone (Pass)', 'iPhone (Fail)', 'Mac (Pass)', 'Mac (Fail)',
        'iPad (Pass)', 'iPad (Fail)', 'Apple Watch (Pass)', 'Apple Watch (Fail)'
    ],
    'Central': [20, 45, 12, 24, 23, 12, 11, 7],
    'Northern': [45, 56, 9, 11, 11, 8, 45, 3],
    'Sarawak': [23, 12, 56, 7, 44, 4, 67, 99],
    'Sabah': [12, 54, 34, 6, 8, 22, 5, 66]
})

def process_lob_data(df):
    """Clean and structure LOB data for visualization."""
    df_long = df.melt(id_vars=['Result'], var_name='Region', value_name='Count')
    df_long['Status'] = df_long['Result'].apply(lambda x: 'Pass' if '(Pass)' in x else 'Fail')
    df_long['Product'] = df_long['Result'].apply(lambda x: x.split(' (')[0])
    return df_long

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("SSC 2026 Dashboard : Explorer")
    view_selection = st.selectbox(
        "Select Dataset:",
        ["Regional Performance", "Outlet Performance", "LOB Comparison"]
    )
    st.markdown("---")
    st.caption("© 2026 SSC 2026 | Insight Team")

# -----------------------------------------------------------------------------
# 4. MAIN LOGIC & KPI CALCULATION
# -----------------------------------------------------------------------------

st.title(f"📊 {view_selection}")

# Initialize variables to avoid empty state errors
fig = None
display_df = None

if view_selection == "Regional Performance":
    display_df = df_regional
    
    # KPIs
    total_pass = display_df['Pass'].sum()
    total_fail = display_df['Fail'].sum()
    total_vol = display_df['Total Headcount'].sum()
    
    # Chart
    chart_df = display_df.melt(id_vars=['Region'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
    fig = px.bar(chart_df, x='Region', y='Count', color='Status', barmode='group',
                 text_auto=True, # Added text labels
                 color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'}, 
                 title="Pass vs Fail by Region")

elif view_selection == "Outlet Performance":
    display_df = df_outlet
    
    # KPIs
    total_pass = display_df['Pass'].sum()
    total_fail = display_df['Fail'].sum()
    total_vol = total_pass + total_fail
    
    # Chart
    chart_df = display_df.melt(id_vars=['Outlet'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
    fig = px.bar(chart_df, x='Outlet', y='Count', color='Status', barmode='group',
                 text_auto=True, # Added text labels
                 color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'}, 
                 title="Pass vs Fail by Outlet")

elif view_selection == "LOB Comparison":
    raw_df = df_lob
    processed_lob = process_lob_data(df_lob)
    
    # We want to display the CLEAN data in the table, not the raw messy strings
    display_df = processed_lob[['Region', 'Product', 'Status', 'Count']]
    
    # KPIs
    total_pass = processed_lob[processed_lob['Status'] == 'Pass']['Count'].sum()
    total_fail = processed_lob[processed_lob['Status'] == 'Fail']['Count'].sum()
    total_vol = total_pass + total_fail
    
    # Chart
    fig = px.bar(processed_lob, x='Product', y='Count', color='Status', 
                 color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'},
                 facet_col='Region', title="Product Performance by Region")

# Common KPI Logic
pass_rate = (total_pass / total_vol) * 100 if total_vol > 0 else 0

# -----------------------------------------------------------------------------
# 5. DASHBOARD LAYOUT
# -----------------------------------------------------------------------------

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
