
import json
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

# Shipping containers
CONTAINERS = ["CONT-001", "CONT-002", "CONT-003"]
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda data: json.dumps(data).encode("utf-8")
)

# Generate simulated IoT sensor readings
def generate_sensor_data(container_id):
    return {
        "container_id": container_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature_c": round(random.uniform(2, 12), 2),
        "humidity_percent": round(random.uniform(55, 95), 2),
        "vibration_g": round(random.uniform(0, 1.5), 3)
    }

def main():
    print("AtmoSync IoT Simulator Started!")

    try:
        while True:
            for container in CONTAINERS:
                sensor_data = generate_sensor_data(container)
                print(json.dumps(sensor_data))
                producer.send("container-sensors", value=sensor_data)

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nSimulator stopped.")

if __name__ == "__main__":
    main()
