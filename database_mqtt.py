import paho
# Module Import
import paho.mqtt.client as paho
import mariadb
import sys


# Connecting the database from mariadb

try:
    conn = mariadb.connect(
        user="root",
        password="xju53rqh",
        host="localhost",
        port=3306,
        database="gps",
        autocommit=True)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()


# functions for the all the data getting send to the database

def add_latitude_gps(cur, lat):
    cur.execute("INSERT INTO gps.gpstrackerino(latitude) "
                "VALUES (?)", (lat,))

def add_longitude_gps(cur, long):
    cur.execute("INSERT INTO gps.gpstrackerino(longitude) "
                "VALUES (?)", (long,))

def add_temperature_gps(cur, t):
    cur.execute("INSERT INTO gps.gpstrackerino(temperature) "
                "VALUES (?)", (t,))


# functions, so the latitude, longitude and temperature gets transported
# to the database


def on_message(mosq, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def on_connect_latitude(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Gpstracker/latitude")                   # subscribed to the latitude wildcard

def on_message_latitude(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    add_latitude_gps(cur, float(msg.payload))                 # latitude will be printed in the database

def on_connect_longitude(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Gpstracker/longitude")                  # subscribed to the longitude wildcard

def on_message_longitude(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    add_longitude_gps(cur, float(msg.payload))                # longitude will be printed in the database

def on_connect_temperature(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Gpstracker/temperature")                # subscribed to the temperature wildcard

def on_message_temperature(client, obj, msg):
    print(msg.topic + " " + str(msg.payload))
    add_temperature_gps(cur, float(msg.payload))              # temperature will be printed in the database




mqttc = paho.Client()

mqttc.message_callback_add('Gpstracker/latitude', on_message_latitude)
mqttc.message_callback_add('Gpstracker/longitude', on_message_longitude)
mqttc.message_callback_add('Gpstracker/temperature', on_message_temperature)
mqttc.on_message = on_message
mqttc.connect("test.mosquitto.org", 1883, 30)           # we are using the test server for our mqtt server
mqttc.subscribe("Gpstracker/#")                         # subscribing to the mqtt topic

mqttc.loop_forever()









