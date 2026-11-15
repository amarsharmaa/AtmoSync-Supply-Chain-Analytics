import json
import snowflake.connector
import os
from getpass import getpass
from cryptography.hazmat.primitives import serialization
key_path = "consumer/snowflake_rsa_key.pem"
with open(key_path, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=getpass("Enter RSA key password: ").encode()
    )
snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
snowflake_user = os.getenv("SNOWFLAKE_USER")
snowflake_authenticator = "SNOWFLAKE_JWT"
conn = snowflake.connector.connect(
    account=snowflake_account,
    user=snowflake_user,
    authenticator=snowflake_authenticator,
    warehouse="SNOWFLAKE_LEARNING_WH",
    database="ATMOSYNC_DB",
    schema="RAW",
    private_key=private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
),
)
print("Snowflake Connected Successfully!")
cursor = conn.cursor()
from kafka import KafkaConsumer
consumer = KafkaConsumer(
    "container-sensors",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    group_id="atmosync-snowflake-consumer",
    value_deserializer=lambda data: json.loads(data.decode("utf-8"))
)
print("AtmoSync Kafka Consumer Started!")

for message in consumer:
    sensor_data = message.value
    print("Received:", sensor_data)
    cursor.execute(
    """
    INSERT INTO ATMOSYNC_DB.RAW.SENSOR_READINGS
    (CONTAINER_ID, SENSOR_TIMESTAMP, TEMPERATURE_C,
     HUMIDITY_PERCENT, VIBRATION_G)
    VALUES (%s, %s, %s, %s, %s)
    """,
    (
        sensor_data["container_id"],
        sensor_data["timestamp"],
        sensor_data["temperature_c"],
        sensor_data["humidity_percent"],
        sensor_data["vibration_g"]
    )
)
    #RIJILNL-DA81513