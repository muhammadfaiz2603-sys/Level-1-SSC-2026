import streamlit as st
import pandas as pd
import plotly.express as px
import io

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="SSC 2026 Dashboard", layout="wide")

# Custom CSS for styling metrics
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
# 2. DATA EMBEDDING (Robust Version)
# -----------------------------------------------------------------------------

# We use .strip() to ensure no accidental whitespace causes errors

# --- REGIONAL SUMMARY ---
csv_regional = """Region,Pass,Fail,Total Headcount
Central,48,84,132
Northern,64,64,128
Southern,33,70,103
East Coast,25,20,45
Sabah,23,42,65
Sarawak,33,27,60
Total,226,307,533""".strip()

# --- LOB SUMMARY ---
csv_lob = """LOB,Central,Northern,Southern,East Coast,Sabah,Sarawak,Total
Apple Watch & iPhone (Pass),48,0,33,25,23,33,162
Apple Watch & iPhone (Fail),84,0,70,20,43,27,244
iPad (Pass),0,0,0,0,0,0,0
iPad (Fail),0,0,0,0,0,0,0
Mac (Pass),0,0,0,0,0,0,0
Mac (Fail),0,0,0,0,0,0,0""".strip()

# --- CENTRAL DATA ---
csv_central = """Outlet,Pass,Fail,Total Crew
AP,1,4,5
EV,2,3,5
MF,4,2,6
PR,3,2,5
PS,0,5,5
QS,1,4,5
SA,3,4,7
SL,5,0,5
SWSGKG,2,1,3
SWSGKW,3,2,5
SWSGSY,1,4,5
TG,2,5,7
UK,0,1,1
BG,2,2,4
BK,2,2,4
BV,3,2,5
EK,2,3,5
LY,2,3,5
MT,4,2,6
PU,0,5,5
PY,2,14,16
SWKLAA,1,2,3
SWKLGC,1,3,4
UP,0,5,5
WW,2,4,6
Total,48,84,132""".strip()

# --- NORTHERN DATA ---
csv_northern = """Outlet,Pass,Fail,Total Crew
AR,0,8,8
KI,2,3,5
TM,1,5,6
TS,0,7,7
LW,3,2,5
SWKDSW,4,0,4
VM,6,0,6
AC,2,5,7
AJ,5,3,8
AL,4,3,7
AS,0,5,5
BM,2,4,6
GT,7,7,14
PG,5,2,7
QB,6,9,15
SQ,4,1,5
SU,13,0,13
Total,64,64,128""".strip()

# --- SOUTHERN DATA ---
csv_southern = """Outlet,Pass,Fail,Total Crew
BP,2,5,7
JB,2,9,11
KJ,0,7,7
KP,2,2,4
PD,5,7,12
SC,1,5,6
SWJHBX,1,3,4
SWJHDS,0,5,5
SWJHEL,0,5,5
SWJHGP,2,3,5
WE,4,1,5
MP,4,0,4
NL,6,2,8
SG,3,3,6
SR,0,7,7
SWNSLJ,1,3,4
SWNSLT,0,3,3
Total,33,70,103""".strip()

# --- EAST COAST DATA ---
csv_east = """Outlet,Pass,Fail,Total Crew
EC,4,3,7
KT,3,1,4
MM,3,0,3
SWPHCH,0,4,4
SWPHLK,1,3,4
SWTRGD,0,5,5
SWTRMY,5,0,5
KA,7,0,7
KM,2,4,6
Total,25,20,45""".strip()

# --- SABAH DATA ---
csv_sabah = """Outlet,Pass,Fail,Total Crew
HS,6,0,6
IG,7,12,19
PQ,2,5,7
SS,0,10,10
SWSBCC,0,3,3
SWSBCM,3,2,5
SWSBKK,1,3,4
TW,4,3,7
SWLBFP,0,4,4
Total,23,42,65""".strip()

# --- SARAWAK DATA ---
csv_sarawak = """Outlet,Pass,Fail,Total Crew
CK,4,3,7
MB,5,0,5
MR,1,4,5
SB,5,0,5
SP,8,4,12
SWSWDM,2,3,5
SWSWER,1,4,5
SY,1,5,6
VC,6,4,10
Total,33,27,60""".strip()

# -----------------------------------------------------------------------------
# 3. DATA PROCESSING
# -----------------------------------------------------------------------------

@st.cache_data
def load_and_clean_data():
    # 1. Regional Summary
    # skipinitialspace=True helps if copy-pasting introduced spaces
    df_reg = pd.read_csv(io.StringIO(csv_regional), skipinitialspace=True)
    df_reg = df_reg[df_reg['Region'] != 'Total']
    df_reg['Region'] = df_reg['Region'].str.strip()
    
    # 2. LOB Summary
    df_lob = pd.read_csv(io.StringIO(csv_lob), skipinitialspace=True)
    # Rename 'LOB' to 'Result' to ensure consistency
    if 'LOB' in df_lob.columns:
        df_lob = df_lob.rename(columns={'LOB': 'Result'})
    
    # 3. Outlet Data (Combine all regions)
    def read_block(csv_data, region_name):
        try:
            df = pd.read_csv(io.StringIO(csv_data), skipinitialspace=True)
            # Standardize column names
            df.columns = df.columns.str.strip()
            # Remove Total row
            df = df[df['Outlet'] != 'Total']
            df['Region'] = region_name
            return df
        except Exception as e:
            st.error(f"Error reading {region_name} data: {e}")
            return pd.DataFrame()

    # Create the combined dataframe
    df_outlet = pd.concat([
        read_block(csv_central, 'Central'),
        read_block(csv_northern, 'Northern'),
        read_block(csv_southern, 'Southern'),
        read_block(csv_east, 'East Coast'),
        read_block(csv_sabah, 'Sabah'),
        read_block(csv_sarawak, 'Sarawak')
    ], ignore_index=True)
    
    # Ensure numeric columns are actually numeric
    cols_to_numeric = ['Pass', 'Fail', 'Total Crew']
    for c in cols_to_numeric:
        if c in df_outlet.columns:
            df_outlet[c] = pd.to_numeric(df_outlet[c], errors='coerce').fillna(0)

    return df_reg, df_lob, df_outlet

def process_lob_data(df):
    # Remove Total column if present
    cols = [c for c in df.columns if c != 'Total']
    df = df[cols]
    
    # Melt to long format
    # Check if 'Result' column exists, if not, try to find the first column
    id_col = 'Result' if 'Result' in df.columns else df.columns[0]
    
    df_long = df.melt(id_vars=[id_col], var_name='Region', value_name='Count')
    
    # Rename id_col to Result for consistency if it wasn't already
    if id_col != 'Result':
        df_long = df_long.rename(columns={id_col: 'Result'})
    
    # Extract Status and Product
    df_long['Status'] = df_long['Result'].apply(lambda x: 'Pass' if '(Pass)' in str(x) else 'Fail')
    df_long['Product'] = df_long['Result'].apply(lambda x: str(x).split(' (')[0])
    
    return df_long

# Load data safely
try:
    df_regional, df_lob, df_outlet = load_and_clean_data()
except Exception as e:
    st.error(f"Critical Error Loading Data: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 4. SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("SSC 2026 Dashboard")
    st.write("Explorer Quest - Jan 2026")
    
    view_selection = st.selectbox(
        "Select Dataset:",
        ["Regional Performance", "Outlet Performance", "LOB Comparison"]
    )
    
    st.markdown("---")
    st.caption("© 2026 Insight Team")

# -----------------------------------------------------------------------------
# 5. MAIN LOGIC
# -----------------------------------------------------------------------------

st.title(f"📊 {view_selection}")

active_df = pd.DataFrame()
chart_fig = None
total_pass = 0
total_fail = 0
total_vol = 0

if view_selection == "Regional Performance":
    active_df = df_regional
    
    if not active_df.empty:
        total_pass = active_df['Pass'].sum()
        total_fail = active_df['Fail'].sum()
        total_vol = active_df['Total Headcount'].sum()
        
        # Chart
        chart_df = active_df.melt(id_vars=['Region'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
        chart_fig = px.bar(chart_df, x='Region', y='Count', color='Status', barmode='group',
                           color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'}, 
                           title="Pass vs Fail by Region")

elif view_selection == "Outlet Performance":
    active_df = df_outlet
    
    if not active_df.empty:
        # Filter
        regions_list = sorted(active_df['Region'].unique().tolist())
        # Default to first region if available
        default_opt = regions_list[0] if regions_list else None
        selected_region = st.sidebar.multiselect("Filter by Region:", regions_list, default=default_opt)
        
        if selected_region:
            filtered_df = active_df[active_df['Region'].isin(selected_region)]
            title_text = f"Outlet Performance ({', '.join(selected_region)})"
        else:
            filtered_df = active_df
            title_text = "Outlet Performance (All)"
        
        # Metrics
        total_pass = filtered_df['Pass'].sum()
        total_fail = filtered_df['Fail'].sum()
        total_vol = total_pass + total_fail
        
        # Chart
        chart_df = filtered_df.melt(id_vars=['Outlet'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
        chart_df = chart_df.sort_values(by='Count', ascending=False)
        
        chart_fig = px.bar(chart_df, x='Outlet', y='Count', color='Status', barmode='group',
                           color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'}, 
                           title=title_text)

elif view_selection == "LOB Comparison":
    active_df = df_lob
    if not active_df.empty:
        processed_lob = process_lob_data(df_lob)
        
        total_pass = processed_lob[processed_lob['Status'] == 'Pass']['Count'].sum()
        total_fail = processed_lob[processed_lob['Status'] == 'Fail']['Count'].sum()
        total_vol = total_pass + total_fail
        
        # Chart
        chart_fig = px.bar(processed_lob, x='Product', y='Count', color='Region',
                           facet_row='Status',
                           title="Product Performance: Regional Breakdown")
        chart_fig.update_layout(height=600)

pass_rate = (total_pass / total_vol) * 100 if total_vol > 0 else 0

# -----------------------------------------------------------------------------
# 6. LAYOUT
# -----------------------------------------------------------------------------

# ROW 1: KPIs
st.subheader("1. Key Performance Indicators")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Volume", f"{int(total_vol)}")
c2.metric("Total Pass", f"{int(total_pass)}")
c3.metric("Total Fail", f"{int(total_fail)}")
c4.metric("Pass Rate", f"{pass_rate:.1f}%")

st.markdown("---")

# ROW 2: CHART
st.subheader("2. Graphical Analysis")
if chart_fig:
    st.plotly_chart(chart_fig, use_container_width=True)
else:
    st.info("No data available for chart.")

st.markdown("---")

# ROW 3: TABLE
st.subheader("3. Data Table")

display_df = active_df.copy()

# For outlet view, show the filtered data in the table
if view_selection == "Outlet Performance" and 'filtered_df' in locals():
    display_df = filtered_df.copy()

if not display_df.empty and 'Pass' in display_df.columns and 'Fail' in display_df.columns:
    display_df['Calculated Total'] = display_df['Pass'] + display_df['Fail']
    # Avoid division by zero
    display_df['Pass Rate (%)'] = display_df.apply(
        lambda row: (row['Pass'] / row['Calculated Total'] * 100) if row['Calculated Total'] > 0 else 0, 
        axis=1
    ).round(1)
    
    st.dataframe(
        display_df.style.background_gradient(cmap='RdYlGn', subset=['Pass Rate (%)'], vmin=0, vmax=100),
        use_container_width=True
    )
else:
    st.dataframe(display_df, use_container_width=True)
