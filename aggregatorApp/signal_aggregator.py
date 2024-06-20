import paho.mqtt.client as mqtt
import logging
import sys
import psycopg2
import json
import statistics
import time
from copy import deepcopy

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.warning('This event was logged.')

# Parameters for MQTT Broker
mqtt_broker = "mqtt"
mqtt_port = 1883

# Parameters required to start a program T is how long should be the period between each measurement,
# N is how many measurements are required to aggregate
T = int(sys.argv[1])
N = int(sys.argv[2])

logging.info(("T is: "+str(T), "N is: "+str(N)))

is_aggregating = False
measurements = []

def save_to_db(period_start:str,period_end:str,n:int,min_value:float,max_value:float,median_value:float,average_value:float) -> None:
    conn = psycopg2.connect(host='db', user='user', password='password', dbname='aggregated_data', port=5432)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO measurements (period_start, period_end, n, min, max, median, average)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (period_start, period_end, n, min_value, max_value, median_value, average_value))
    conn.commit()
    cursor.close()
    conn.close()

def aggregate_and_save() -> None:
    global measurements,is_aggregating
    arr = deepcopy(measurements)
    if len(arr) < N:
        return
    elif len(arr) >= N:
        is_aggregating = True
        periods = [m['time']for m in arr]
        period_start = min(periods)
        period_end = max(periods)
        n = len(arr)
        values = [m['value'] for m in arr]
        min_value = min(values)
        max_value = max(values)
        median_value = statistics.median(values)
        average_value = sum(values) / len(values)
        save_to_db(period_start,period_end,n,min_value,max_value,median_value,average_value)
        measurements.clear()

def init_mqqt() -> None:
    client = mqtt.Client("Receiver", clean_session=True)
    client.connect(mqtt_broker, mqtt_port, 60)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.subscribe("measurements")
    client.message_callback_add("measurements",receive_message)
    client.loop_start()

def receive_message(client, userdata, message):
    global measurements
    data = json.loads(message.payload.decode("utf-8"))
    if not is_aggregating:
        measurements.append(data)
    else:
        client.publish("ignored",message.payload.decode("utf-8"))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected successfully!")
    else:
        logging.info(f"Connection error code [{rc}]")

def on_disconnect(client, userdata, rc):
    logging.info(f"Disconnected, code [{rc}]")

def run() -> None:
    global is_aggregating
    while True:
        aggregate_and_save()
        time.sleep(T)
        is_aggregating = False



if __name__ == '__main__':
    init_mqqt()
    run()
