
# AtmoSync — Micro-Climate Arbitrage Analytics

## Project Overview
AtmoSync is a supply chain analytics project that monitors simulated IoT sensor data and compares transportation routes based on temperature, travel time, and cost.

The project demonstrates how data engineering and analytics can support supply chain monitoring and route decision-making.

## Technologies Used
- Python — IoT simulation and data processing
- Apache Kafka — Sensor data streaming
- Snowflake — Cloud data warehouse
- dbt — SQL data transformation
- Streamlit — Interactive dashboard
- Git & GitHub — Version control

## Key Features
- Simulated IoT sensor data generation
- Kafka-based data streaming
- Snowflake data storage
- Temperature and humidity monitoring
- Rule-based spoilage risk analysis
- Simulated route recommendations
- Micro-climate arbitrage comparison
- Interactive Streamlit dashboard

## Data Pipeline
IoT Simulator → Apache Kafka → Python Consumer → Snowflake RAW → dbt Analytics → Streamlit Dashboard

## Dashboard
The dashboard displays:
- Container sensor readings
- Temperature and humidity trends
- Container spoilage risk summaries
- Route recommendations
- Transport cost and temperature trade-offs

## Project Limitations
- Sensor and route data are simulated.
- Spoilage risk thresholds are demonstration rules, not validated for specific cargo.
- Route recommendations do not currently use live weather, traffic, or GPS data.

## Project Status
Core analytics pipeline and dashboard implemented.

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/amarsharmaa/AtmoSync-Supply-Chain-Analytics.git
cd AtmoSync-Supply-Chain-Analytics
```

### 2. Create a Python Environment
```bash
python -m venv .venv
```

Activate the environment on Windows:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Configure Snowflake
Create a Snowflake database and configure key-pair authentication.

Keep RSA private keys, passwords, and other credentials outside Git.

### 5. Start Kafka
Start the Kafka service using Docker.

### 6. Run the IoT Simulator
```bash
python simulator/iot_simulator.py
```

### 7. Run the Kafka Consumer
In another terminal:
```bash
python consumer/kafka_to_snowflake.py
```

### 8. Run dbt Models
```bash
cd atmosync_dbt
dbt debug
dbt run
cd ..
```

### 9. Launch the Dashboard
```bash
python -m streamlit run dashboard/app.py
```

Open http://localhost:8501 in your browser.

## Security
Never commit RSA private keys, Snowflake passwords,
or local credential configuration files to GitHub.
