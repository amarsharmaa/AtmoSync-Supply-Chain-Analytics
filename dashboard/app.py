
import streamlit as st

if "show_sensor" not in st.session_state:
    st.session_state.show_sensor = False

if "show_risk" not in st.session_state:
    st.session_state.show_risk = False

if "show_routes" not in st.session_state:
    st.session_state.show_routes = False

if "show_arbitrage" not in st.session_state:
    st.session_state.show_arbitrage = False



from snowflake_connection import get_snowflake_connection


st.set_page_config(
    page_title="AtmoSync Dashboard",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ AtmoSync")
st.subheader("Micro-Climate Arbitrage Analytics")

st.write("Real-Time Supply Chain Monitoring & Route Optimization")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Containers", 3)

with col2:
    st.metric("Available Routes", 6)

with col3:
    st.metric("Recommended Routes", 3)

st.success("AtmoSync Dashboard is Running Successfully!")

@st.cache_data(ttl=60)
def load_sensor_data():
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    CONTAINER_ID,
                    SENSOR_TIMESTAMP,
                    TEMPERATURE_C,
                    HUMIDITY_PERCENT,
                    VIBRATION_G
                FROM ATMOSYNC_DB.RAW.SENSOR_READINGS
                ORDER BY SENSOR_TIMESTAMP DESC
                LIMIT 100
            """)
            return cursor.fetch_pandas_all()
        finally:
            cursor.close()
    finally:
        conn.close()

st.subheader("📊 Live Sensor Readings")


if st.button("Load Sensor Data"):
    st.session_state.show_sensor = True

if st.session_state.show_sensor:

    try:
        with st.spinner("Fetching data from Snowflake..."):
            sensor_df = load_sensor_data()

        st.dataframe(sensor_df, use_container_width=True)

        st.subheader("🌡️ Container Temperature Trends")

        if not sensor_df.empty:
            chart_data = sensor_df.sort_values(
                "SENSOR_TIMESTAMP"
            )

            st.line_chart(
                chart_data,
                x="SENSOR_TIMESTAMP",
                y="TEMPERATURE_C",
                color="CONTAINER_ID"
            )

        st.subheader("💧 Container Humidity Trends")

        if not sensor_df.empty:
            st.line_chart(
                chart_data,
                x="SENSOR_TIMESTAMP",
                y="HUMIDITY_PERCENT",
                color="CONTAINER_ID"
            )



    except Exception as e:
        st.error(f"Snowflake connection error: {e}")

import os

os.environ["SNOWFLAKE_KEY_PASSWORD"] = st.text_input(
    "Enter Snowflake Private Key Password",
    type="password"
)

@st.cache_data(ttl=60)
def load_spoilage_risk():
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    CONTAINER_ID,
                    TOTAL_READINGS,
                    AVG_TEMPERATURE,
                    AVG_HUMIDITY,
                    HIGH_RISK_READINGS,
                    OVERALL_RISK
                FROM ATMOSYNC_DB.ANALYTICS.CONTAINER_RISK_SUMMARY
                ORDER BY CONTAINER_ID
            """)
            return cursor.fetch_pandas_all()
        finally:
            cursor.close()
    finally:
        conn.close()

st.divider()
st.subheader("⚠️ Container Spoilage Risk Analysis")


if st.button("Load Spoilage Risk"):
    st.session_state.show_risk = True

if st.session_state.show_risk:

    try:
        with st.spinner("Loading risk analysis..."):
            risk_df = load_spoilage_risk()

        if risk_df.empty:
            st.info("No risk data available.")
        else:
            st.dataframe(
                risk_df,
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Error loading risk data: {e}")

@st.cache_data(ttl=60)
def load_route_recommendations():
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    CONTAINER_ID,
                    ROUTE_ID,
                    EXPECTED_TEMPERATURE_C,
                    TRAVEL_TIME_HOURS,
                    TRANSPORT_COST_INR,
                    ROUTE_TEMPERATURE_RISK,
                    RECOMMENDATION_STATUS
                FROM ATMOSYNC_DB.ANALYTICS.BEST_ROUTE_RECOMMENDATION
                ORDER BY CONTAINER_ID, ROUTE_RANK
            """)
            return cursor.fetch_pandas_all()
        finally:
            cursor.close()
    finally:
        conn.close()

st.divider()
st.subheader("🚚 Best Route Recommendations")


if st.button("Load Route Recommendations"):
    st.session_state.show_routes = True

if st.session_state.show_routes:

    try:
        with st.spinner("Loading route recommendations..."):
            route_df = load_route_recommendations()

        if route_df.empty:
            st.info("No route data available.")
        else:
            st.dataframe(
                route_df,
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Error loading routes: {e}")

@st.cache_data(ttl=60)
def load_arbitrage_analysis():
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    CONTAINER_ID,
                    ROUTE_ID,
                    RECOMMENDATION_STATUS,
                    TRANSPORT_COST_INR,
                    EXTRA_COST_INR,
                    TEMPERATURE_REDUCTION_C,
                    EXTRA_TRAVEL_HOURS
                FROM ATMOSYNC_DB.ANALYTICS.ROUTE_ARBITRAGE_ANALYSIS
                ORDER BY CONTAINER_ID, ROUTE_ID
            """)
            return cursor.fetch_pandas_all()
        finally:
            cursor.close()
    finally:
        conn.close()

st.divider()
st.subheader("💰 Micro-Climate Arbitrage Analysis")


if st.button("Load Arbitrage Analysis"):
    st.session_state.show_arbitrage = True

if st.session_state.show_arbitrage:

    try:
        with st.spinner("Loading arbitrage analysis..."):
            arbitrage_df = load_arbitrage_analysis()

        if arbitrage_df.empty:
            st.info("No arbitrage data available.")
        else:
            st.dataframe(
                arbitrage_df,
                use_container_width=True
            )

            st.subheader("📊 Extra Cost vs Temperature Reduction")

            chart_df = arbitrage_df[
                arbitrage_df["ROUTE_ID"] != "ROUTE-A"
            ].copy()

            st.scatter_chart(
                chart_df,
                x="EXTRA_COST_INR",
                y="TEMPERATURE_REDUCTION_C",
                color="CONTAINER_ID"
            )


    except Exception as e:
        st.error(f"Error loading arbitrage data: {e}")