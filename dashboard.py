import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration to wide mode to better utilize the 2-column layout
st.set_page_config(layout="wide", page_title="Performance Dashboard")

# --- 1. Load Data ---
@st.cache_data
def load_data():
    try:
        # Load the CSV files
        df_lob = pd.read_csv('Level 1.xlsx - LOB Comparison.csv')
        df_region = pd.read_csv('Level 1.xlsx - Regional Performance Comparison.csv')
        df_outlet = pd.read_csv('Level 1.xlsx - Outlet Performance Comparison.csv')
        return df_lob, df_region, df_outlet
    except FileNotFoundError as e:
        st.error(f"Error loading files: {e}. Please ensure the CSV files are in the same directory.")
        return None, None, None

df_lob, df_region, df_outlet = load_data()

if df_lob is not None:
    
    # --- Data Preprocessing ---
    # Process LOB data: Melt and split 'Result' into 'Product' and 'Status' for better plotting
    df_lob_melted = df_lob.melt(id_vars=['Result'], var_name='Region_Col', value_name='Count')
    # Regex to extract "iPhone" from "iPhone (Pass)"
    df_lob_melted[['Product', 'Status']] = df_lob_melted['Result'].str.extract(r'(.+) \((.+)\)')
    
    # --- COLUMN 1: SIDEBAR ---
    with st.sidebar:
        st.header("Settings")
        st.write("Filter the dashboard views.")
        
        # Filter: Select Regions (Applies to Regional and LOB charts)
        # normalize region names for consistency if needed
        available_regions = df_region['Region'].unique()
        selected_regions = st.multiselect(
            "Select Region(s)",
            options=available_regions,
            default=available_regions
        )
        
        st.markdown("---")
        st.caption("Dashboard v1.0")

    # Filter data based on selection
    if selected_regions:
        filtered_region_df = df_region[df_region['Region'].isin(selected_regions)]
        
        # For LOB, we map the column names. Note: 'sarawak' in LOB is lowercase vs 'Sarawak' in Region
        # We create a mapping or just filter strictly if names match. 
        # Let's handle case sensitivity for 'sarawak'.
        region_map = {r.lower(): r for r in available_regions} # map lower to display name
        
        # Filter LOB melted data
        # We lowercase the Region_Col to match against selected regions (lowercased)
        selected_regions_lower = [r.lower() for r in selected_regions]
        filtered_lob_df = df_lob_melted[df_lob_melted['Region_Col'].str.lower().isin(selected_regions_lower)]
    else:
        filtered_region_df = df_region
        filtered_lob_df = df_lob_melted

    # --- COLUMN 2: MAIN AREA ---
    # The main area is divided into 3 Rows as requested

    # --- ROW 1: DATA CARDS ---
    st.subheader("Overview")
    
    # Calculate metrics
    total_pass = filtered_region_df['Pass'].sum()
    total_fail = filtered_region_df['Fail'].sum()
    total_headcount = filtered_region_df['Total Headcount'].sum()
    pass_rate = (total_pass / total_headcount * 100) if total_headcount > 0 else 0

    # Create 3 columns for the cards
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric(label="Total Pass", value=f"{total_pass:,}")
    with c2:
        st.metric(label="Total Fail", value=f"{total_fail:,}")
    with c3:
        st.metric(label="Overall Pass Rate", value=f"{pass_rate:.1f}%")

    st.markdown("---")

    # --- ROW 2: GRAPHS ---
    st.subheader("Performance Visualizations")
    
    # Create two columns for graphs
    g1, g2 = st.columns(2)
    
    with g1:
        st.caption("Regional Pass vs Fail")
        # Melt regional data for stacked bar chart
        reg_melted = filtered_region_df.melt(id_vars=['Region'], value_vars=['Pass', 'Fail'], 
                                             var_name='Status', value_name='Count')
        fig_reg = px.bar(reg_melted, x='Region', y='Count', color='Status', 
                         title="Results by Region", barmode='group',
                         color_discrete_map={'Pass': '#4CAF50', 'Fail': '#EF5350'})
        st.plotly_chart(fig_reg, use_container_width=True)

    with g2:
        st.caption("LOB (Line of Business) Performance")
        # Aggregating the filtered LOB data by Product and Status
        lob_grouped = filtered_lob_df.groupby(['Product', 'Status'])['Count'].sum().reset_index()
        
        fig_lob = px.bar(lob_grouped, x='Product', y='Count', color='Status', 
                         title="Results by Product Line", barmode='group',
                         color_discrete_map={'Pass': '#4CAF50', 'Fail': '#EF5350'})
        st.plotly_chart(fig_lob, use_container_width=True)

    # Optional: Outlet chart in a full width below if needed, or just keep 2 cols.
    # Let's add the Outlet chart below these two to fill the "Graphs" row fully.
    
    st.caption("Outlet Performance Breakdown")
    fig_outlet = px.bar(df_outlet, x='Outlet', y=['Pass', 'Fail'], 
                        title="Results by Outlet", barmode='group',
                        color_discrete_map={'Pass': '#4CAF50', 'Fail': '#EF5350'})
    st.plotly_chart(fig_outlet, use_container_width=True)

    st.markdown("---")

    # --- ROW 3: DATA TABLE ---
    st.subheader("Detailed Data")
    
    # Use tabs to organize the different tables
    tab1, tab2, tab3 = st.tabs(["Regional Data", "LOB Data", "Outlet Data"])
    
    with tab1:
        st.dataframe(filtered_region_df, use_container_width=True)
        
    with tab2:
        # Pivot back for a cleaner table view if needed, or show raw
        st.dataframe(df_lob, use_container_width=True)
        
    with tab3:
        st.dataframe(df_outlet, use_container_width=True)

else:
    st.warning("Please upload the necessary CSV files to view the dashboard.")
