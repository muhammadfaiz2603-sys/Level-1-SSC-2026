import streamlit as st
import pandas as pd
import plotly.express as px
import io

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="SSC 2026 Dashboard", layout="wide")

# Custom CSS to style the metric cards
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
# 2. DATA EMBEDDING (Raw Data from your Excel files)
# -----------------------------------------------------------------------------

# FILE 1: REGIONAL PERFORMANCE
csv_regional_raw = """Region,Pass,Fail,Total Headcount
Central,48,84,132
Northern,64,64,128
Southern,33,70,103
East Coast,25,20,45
Sabah,23,42,65
Sarawak ,33,27,60
Total,226,307,533"""

# FILE 2: LOB COMPARISON
csv_lob_raw = """LOB,Central,Northern,Southern,East Coast,Sabah,Sarawak,Total
Apple Watch & iPhone (Pass),48,0,33,25,23,33,162
Apple Watch & iPhone (Fail),84,0,70,20,43,27,244
iPad (Pass),0,0,0,0,0,0,0
iPad (Fail),0,0,0,0,0,0,0
Mac (Pass),0,0,0,0,0,0,0
Mac (Fail),0,0,0,0,0,0,0"""

# FILE 3: OUTLET PERFORMANCE (Staggered Data)
csv_outlet_raw = """Central Region,Pass,Fail,Total Crew
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
Total,48,84,132
Nothern Region,Pass,Fail,Total Crew
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
Total,64,64,128
Southern Region,Pass,Fail,Total Crew
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
Total,33,70,103
East Coast Region,Pass,Fail,Total Crew
EC,4,3,7
KT,3,1,4
MM,3,0,3
SWPHCH,0,4,4
SWPHLK,1,3,4
SWTRGD,0,5,5
SWTRMY,5,0,5
KA,7,0,7
KM,2,4,6
Total,25,20,45
Sabah Region,Pass,Fail,Total Crew
HS,6,0,6
IG,7,12,19
PQ,2,5,7
SS,0,10,10
SWSBCC,0,3,3
SWSBCM,3,2,5
SWSBKK,1,3,4
TW,4,3,7
SWLBFP,0,4,4
Total,23,42,65
Sarawak Region,Pass,Fail,Total Crew
CK,4,3,7
MB,5,0,5
MR,1,4,5
SB,5,0,5
SP,8,4,12
SWSWDM,2,3,5
SWSWER,1,4,5
SY,1,5,6
VC,6,4,10
Total,33,27,60"""

# -----------------------------------------------------------------------------
# 3. DATA PROCESSING FUNCTIONS
# -----------------------------------------------------------------------------

@st.cache_data
def load_and_clean_data():
    # --- 1. Regional Data ---
    df_reg = pd.read_csv(io.StringIO(csv_regional_raw))
    df_reg = df_reg[df_reg['Region'] != 'Total'] # Remove 'Total' row
    df_reg['Region'] = df_reg['Region'].str.strip() # Clean "Sarawak " space
    
    # --- 2. LOB Data ---
    df_lob = pd.read_csv(io.StringIO(csv_lob_raw))
    df_lob = df_lob.rename(columns={'LOB': 'Result'})
    
    # --- 3. Outlet Data (Complex Staggered Format) ---
    raw_outlet_df = pd.read_csv(io.StringIO(csv_outlet_raw), header=None)
    clean_outlets = []
    
    # Map of (Column Index, Region Name)
    region_map = [
        (0, 'Central'), (4, 'Northern'), (8, 'Southern'), 
        (12, 'East Coast'), (16, 'Sabah'), (20, 'Sarawak')
    ]
    
    for col_idx, region_name in region_map:
        # Slice the 3 relevant columns
        subset = raw_outlet_df.iloc[:, col_idx:col_idx+3].copy()
        subset.columns = ['Outlet', 'Pass', 'Fail']
        
        # Cleaning
        subset = subset.dropna(subset=['Outlet']) # Drop empty rows
        subset = subset[~subset['Outlet'].str.contains('Total', case=False, na=False)] # Drop Total rows
        subset = subset[~subset['Outlet'].str.contains('Region', case=False, na=False)] # Drop Header rows
        
        # Convert to numeric
        subset['Pass'] = pd.to_numeric(subset['Pass'], errors='coerce')
        subset['Fail'] = pd.to_numeric(subset['Fail'], errors='coerce')
        subset = subset.dropna(subset=['Pass', 'Fail'])
        
        subset['Region'] = region_name
        clean_outlets.append(subset)
        
    df_outlet_clean = pd.concat(clean_outlets, ignore_index=True)
    
    return df_reg, df_lob, df_outlet_clean

def process_lob_data(df):
    # Remove Total column if exists
    cols = [c for c in df.columns if c != 'Total']
    df = df[cols]
    
    # Melt to long format
    df_long = df.melt(id_vars=['Result'], var_name='Region', value_name='Count')
    
    # Parse Result string "Product (Status)"
    df_long['Status'] = df_long['Result'].apply(lambda x: 'Pass' if '(Pass)' in x else 'Fail')
    df_long['Product'] = df_long['Result'].apply(lambda x: x.split(' (')[0])
    
    return df_long

# Load datasets
df_regional, df_lob, df_outlet = load_and_clean_data()

# -----------------------------------------------------------------------------
# 4. SIDEBAR UI
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
# 5. MAIN PAGE LOGIC
# -----------------------------------------------------------------------------

st.title(f"📊 {view_selection}")

# Initialize variables
active_df = pd.DataFrame()
chart_fig = None
total_pass = 0
total_fail = 0
total_vol = 0

# --- DATA PREPARATION BASED ON SELECTION ---

if view_selection == "Regional Performance":
    active_df = df_regional
    
    # Metrics
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
    
    # Filter Widget (Essential for Outlet view)
    regions_list = sorted(active_df['Region'].unique().tolist())
    selected_region = st.sidebar.multiselect("Filter by Region:", regions_list, default=regions_list[0])
    
    # Apply Filter
    if selected_region:
        filtered_df = active_df[active_df['Region'].isin(selected_region)]
        title_text = f"Outlet Performance ({', '.join(selected_region)})"
    else:
        filtered_df = active_df
        title_text = "Outlet Performance (All)"
        
    # Metrics (Using ALL data, or filtered? Usually Dashboard metrics reflect the Filter)
    # Let's make metrics reflect the filter for better interactivity
    total_pass = filtered_df['Pass'].sum()
    total_fail = filtered_df['Fail'].sum()
    total_vol = total_pass + total_fail
    
    # Chart
    chart_df = filtered_df.melt(id_vars=['Outlet'], value_vars=['Pass', 'Fail'], var_name='Status', value_name='Count')
    # Sort by Count to make chart readable
    chart_df = chart_df.sort_values(by='Count', ascending=False)
    
    chart_fig = px.bar(chart_df, x='Outlet', y='Count', color='Status', barmode='group',
                       color_discrete_map={'Pass': '#00CC96', 'Fail': '#EF553B'}, 
                       title=title_text)

elif view_selection == "LOB Comparison":
    active_df = df_lob # For table display
    processed_lob = process_lob_data(df_lob)
    
    # Metrics
    total_pass = processed_lob[processed_lob['Status'] == 'Pass']['Count'].sum()
    total_fail = processed_lob[processed_lob['Status'] == 'Fail']['Count'].sum()
    total_vol = total_pass + total_fail
    
    # Chart
    chart_fig = px.bar(processed_lob, x='Product', y='Count', color='Region',
                       facet_row='Status', # Split charts by Pass/Fail
                       title="Product Performance: Regional Breakdown")
    chart_fig.update_layout(height=600)

# Global Metric Calculation
pass_rate = (total_pass / total_vol) * 100 if total_vol > 0 else 0


# -----------------------------------------------------------------------------
# 6. DASHBOARD DISPLAY LAYOUT
# -----------------------------------------------------------------------------

# --- ROW 1: KPIs ---
st.subheader("1. Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Volume", f"{int(total_vol)}")
col2.metric("Total Pass", f"{int(total_pass)}")
col3.metric("Total Fail", f"{int(total_fail)}")
col4.metric("Pass Rate", f"{pass_rate:.1f}%")

st.markdown("---")

# --- ROW 2: VISUALIZATION ---
st.subheader("2. Graphical Analysis")
if chart_fig:
    st.plotly_chart(chart_fig, use_container_width=True)

st.markdown("---")

# --- ROW 3: DATA TABLE ---
st.subheader("3. Data Table")

# Display logic: If Outlet or Region, calculate Pass Rate for the table
display_df = active_df.copy()

if view_selection == "Outlet Performance":
    # Use the filtered DF for the table too
    if selected_region:
        display_df = filtered_df.copy()

if 'Pass' in display_df.columns and 'Fail' in display_df.columns:
    display_df['Calculated Total'] = display_df['Pass'] + display_df['Fail']
    display_df['Pass Rate (%)'] = (display_df['Pass'] / display_df['Calculated Total'] * 100).round(1)
    
    # Move Pass Rate to front or significant position if desired, or just style it
    st.dataframe(
        display_df.style.background_gradient(cmap='RdYlGn', subset=['Pass Rate (%)'], vmin=0, vmax=100),
        use_container_width=True
    )
else:
    # For LOB or other formats
    st.dataframe(display_df, use_container_width=True)
