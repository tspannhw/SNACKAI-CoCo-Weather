# Raspberry Pi Weather Data Dashboard

A Streamlit dashboard for visualizing IoT weather sensor data collected from Raspberry Pi devices and stored in Snowflake.

## Overview

This dashboard provides real-time visualization and analysis of weather and device metrics including:
- Environmental readings (temperature, humidity, pressure, dew point, light/lux)
- Device health metrics (CPU usage, memory, CPU temperature)
- Host information and network details

## Features

### Filtering
- **Host Selection**: Multi-select filter to view data from specific Raspberry Pi devices
- **Temperature Range**: Slider to filter by temperature range (°F)
- **IP Search**: Text search to filter by IP address

### Key Metrics
- Average Temperature (°F)
- Average Humidity (%)
- Average Pressure
- Total Record Count

### Visualizations
| Tab | Charts |
|-----|--------|
| Temperature & Humidity | Temperature distribution histogram, Humidity distribution histogram |
| Device Metrics | CPU Usage vs CPU Temp scatter plot, Memory vs Device Temp scatter plot |
| Pressure & Lux | Pressure distribution histogram, Light (Lux) distribution histogram |

### Data Export
- Download filtered data as CSV
- View filtered record count

## Data Schema

The dashboard reads from `DEMO.DEMO.WEATHER_DATA` with the following key columns:

| Column | Type | Description |
|--------|------|-------------|
| UUID | VARCHAR | Unique record identifier |
| HOSTNAME | VARCHAR | Raspberry Pi hostname |
| IPADDRESS | VARCHAR | Device IP address |
| SYSTEMTIME | VARCHAR | Timestamp of reading |
| TEMPERATURE | FLOAT | Ambient temperature (°F) |
| HUMIDITY | FLOAT | Relative humidity (%) |
| PRESSURE | FLOAT | Barometric pressure |
| DEWPOINT | FLOAT | Dew point temperature |
| LUX | FLOAT | Light level (lux) |
| CPU | FLOAT | CPU usage (%) |
| MEMORY | FLOAT | Memory usage (%) |
| CPUTEMPF | NUMBER | CPU temperature (°F) |
| DEVICETEMPERATURE | FLOAT | Device temperature (°F) |

## Deployment

### Option 1: Snowflake Streamlit (Recommended)

1. Navigate to Snowsight → **Streamlit** → **+ Streamlit App**
2. Select your database and schema (e.g., `DEMO.DEMO`)
3. Upload the following files:
   - `streamlit_app.py`
   - `environment.yml`
4. Click **Run**

The app uses `get_active_session()` to connect to Snowflake automatically.

### Option 2: Local Development

```bash
cd streamlit_dashboard

pip install -r requirements.txt

streamlit run streamlit_app.py
```

> **Note**: Local development requires modifying `streamlit_app.py` to use `snowflake.connector` instead of `get_active_session()`.

## File Structure

```
streamlit_dashboard/
├── streamlit_app.py     # Main Streamlit application
├── environment.yml      # Snowflake Streamlit dependencies
├── requirements.txt     # Local development dependencies
└── README.md            # This file
```

## Configuration

### Cache Settings
- Data is cached for 10 minutes (`ttl=600`) using `@st.cache_data`
- Refresh the page to reload data after cache expiration

### Customization
- Modify `display_cols` in `streamlit_app.py` to change visible table columns
- Adjust `nbins` parameter in histograms to change bin count
- Update the table reference in `load_data()` to use a different data source

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Failed to load data" error | Verify table exists and you have SELECT privileges |
| Empty charts | Check if filters are too restrictive |
| Slow performance | Reduce data volume or increase cache TTL |

## Resources

- https://github.com/tspannhw/RPIWeatherStreaming

