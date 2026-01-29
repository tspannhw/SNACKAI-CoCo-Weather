import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

@st.cache_data(ttl=600)
def load_data():
    session = get_active_session()
    df = session.table("DEMO.DEMO.WEATHER_DATA").to_pandas()
    return df

st.title("🌤️ Weather Data Dashboard")

try:
    df = load_data()
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

st.sidebar.header("Filters")

if "HOSTNAME" in df.columns:
    hosts = df["HOSTNAME"].dropna().unique().tolist()
    selected_hosts = st.sidebar.multiselect("Host", hosts, default=hosts)
    df = df[df["HOSTNAME"].isin(selected_hosts)]

temp_range = st.sidebar.slider(
    "Temperature (°F)",
    float(df["TEMPERATURE"].min()) if not df.empty else 0.0,
    float(df["TEMPERATURE"].max()) if not df.empty else 100.0,
    (float(df["TEMPERATURE"].min()) if not df.empty else 0.0, float(df["TEMPERATURE"].max()) if not df.empty else 100.0)
)
df = df[(df["TEMPERATURE"] >= temp_range[0]) & (df["TEMPERATURE"] <= temp_range[1])]

search_term = st.sidebar.text_input("Search by IP Address")
if search_term:
    df = df[df["IPADDRESS"].str.contains(search_term, case=False, na=False)]

st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Avg Temperature", f"{df['TEMPERATURE'].mean():.1f}°F" if not df.empty else "N/A")
with col2:
    st.metric("Avg Humidity", f"{df['HUMIDITY'].mean():.1f}%" if not df.empty else "N/A")
with col3:
    st.metric("Avg Pressure", f"{df['PRESSURE'].mean():.1f}" if not df.empty else "N/A")
with col4:
    st.metric("Records", f"{len(df):,}")

st.subheader("Charts")
tab1, tab2, tab3 = st.tabs(["Temperature & Humidity", "Device Metrics", "Pressure & Lux"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x="TEMPERATURE", nbins=30, title="Temperature Distribution")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="HUMIDITY", nbins=30, title="Humidity Distribution")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(df, x="CPU", y="CPUTEMPF", color="HOSTNAME", title="CPU Usage vs CPU Temp", render_mode="svg")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(df, x="MEMORY", y="DEVICETEMPERATURE", color="HOSTNAME", title="Memory vs Device Temp", render_mode="svg")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x="PRESSURE", nbins=30, title="Pressure Distribution")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="LUX", nbins=30, title="Light (Lux) Distribution")
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Data Table")
display_cols = ["SYSTEMTIME", "HOSTNAME", "IPADDRESS", "TEMPERATURE", "HUMIDITY", "PRESSURE", "DEWPOINT", "LUX", "CPU", "MEMORY", "CPUTEMPF"]
display_cols = [c for c in display_cols if c in df.columns]
st.dataframe(df[display_cols], use_container_width=True, height=400)

st.subheader("Export")
col1, col2 = st.columns(2)
with col1:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "weather_data.csv", "text/csv")
with col2:
    st.write(f"Filtered records: {len(df):,}")
