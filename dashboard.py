import streamlit as st
import pandas as pd
import plotly.express as px
import io

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="SSC 2026 Dashboard", layout="wide")

# CSS to style the metric cards
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
# 2. DATA EMBEDDING (separated for stability)
# -----------------------------------------------------------------------------

# --- REGIONAL SUMMARY ---
csv_regional = """Region,Pass,Fail,Total Headcount
Central,48,84,132
Northern,64,64,128
Southern,33,70,103
East Coast,25,20,45
Sabah,23,42,65
Sarawak,33,27,60
Total,226,307,533"""

# --- LOB SUMMARY ---
csv_lob = """LOB,Central,Northern,Southern,East Coast,Sabah,Sarawak,Total
Apple Watch & iPhone (Pass),48,0,33,25,23,33,162
Apple Watch & iPhone (Fail),84,0,70,20,43,27,244
iPad (Pass),0,0,0,0,0,0,0
iPad (Fail),0,0,0,0,0,0,0
Mac (Pass),0,0,0,0,0,0,0
Mac (Fail),0,0,0,0,0,0,0"""

# --- CENTRAL REGION DATA ---
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
Total,48,84,132"""

# --- NORTHERN REGION DATA ---
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
Total,64,64,128"""

# --- SOUTHERN REGION DATA ---
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
Total,33,70,103"""

# --- EAST COAST REGION DATA ---
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
Total,25,20,45"""

# --- SABAH REGION DATA ---
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
Total,23,42,65"""

# --- SARAWAK REGION DATA ---
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
Total,33,27,60"""

# -----------------------------------------------------------------------------
# 3. DATA PROCESSING FUNCTIONS
# -----------------------------------------------------------------------------

@st.cache_data
def load_and_clean_data():
    # 1. Regional Summary
    df_reg = pd.read_csv(io.StringIO(csv_regional))
    df_reg = df_reg[df_reg['Region'] != 'Total']
    df_reg['Region'] = df_reg['Region'].str.strip()
    
    # 2. LOB Summary
    df_lob = pd.read_csv(io.StringIO(csv_lob))
    df_lob = df_lob.rename(columns={'LOB': 'Result'})
    
    # 3. Outlet Data (Combine all regions)
    # Define a helper to read each block
    def read_block(csv_data, region_name):
        df = pd.read_csv(io.StringIO(csv_data))
        df = df[df['Outlet'] != 'Total'] # Remove Total row
        df['Region'] = region_name
        return df

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
    cols = ['Pass', 'Fail', 'Total Crew']
    for c in cols:
        if c in df_outlet.columns:
            df_outlet[c] = pd.to_numeric(df_outlet[c], errors='coerce').fillna(0)

    return df_reg, df_lob, df_outlet

def process_lob_data(df):
    # Remove Total column if present
    cols = [c for c in df.columns if c != 'Total']
    df = df[cols]
    
    # Melt to long format
    df_long = df.melt(id_vars=['Result'], var_name='Region', value_name='Count')
    
    # Extract Status and Product
    df_long['Status'] = df_long['Result'].apply(lambda x: 'Pass' if '(Pass)' in x else 'Fail')
    df_long['Product'] = df_long['Result'].apply(lambda x: x.split(' (')[0])
    
    return df_long

# Load data
try:
    df_regional, df_lob, df_outlet = load_and_clean_data()
