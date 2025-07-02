#imports
import paho.mqtt.client as mqtt
import json
import random
import time
import sqlite3

#define broker details and specific topics
broker = "broker.hivemq.com"
port = 1883
airforceTopic = "shoes/stock/airforces"
airmaxTopic = "shoes/stock/airmax"
jordansTopic = "shoes/stock/jordans"
daybreakTopic = "shoes/stock/daybreak"

airforcesStock = random.randint(5, 10)
airmaxStock = random.randint(5, 10)
jordansStock = random.randint(5, 10)
daybreakStock = random.randint(5, 10)
code = "0"

client = mqtt.Client()
client.connect(broker, port, 60)

time.sleep(3)
# Generate a random stock level between 5 and 10
# Create a JSON message with the stock level reading
airFmessage = json.dumps({"airforces": airforcesStock})
# Publish the message to the defined topic
client.publish(airforceTopic, airFmessage)
print(f"Airforces: Published stock level {airforcesStock}")
time.sleep(3)

# Generate a random stock level between 5 and 10
# Create a JSON message with the stock level reading
airMmessage = json.dumps({"airmax": airmaxStock})
# Publish the message to the defined topic
client.publish(airmaxTopic, airMmessage)
print(f"Airmax: Published stock level {airmaxStock}")
time.sleep(3)

# Generate a random stock level between 5 and 10
# Create a JSON message with the stock level reading
Jmessage = json.dumps({"jordans": jordansStock})
# Publish the message to the defined topic
client.publish(jordansTopic, Jmessage)
print(f"Jordans: Published stock level {jordansStock}")
time.sleep(3)

# Generate a random stock level between 5 and 10
# Create a JSON message with the stock level reading
Dmessage = json.dumps({"daybreak": daybreakStock})
# Publish the message to the defined topic
client.publish(daybreakTopic, Dmessage)
print(f"Daybreak: Published stock level {daybreakStock}")
time.sleep(3)

conn = sqlite3.connect('shoestock.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shoe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        stock INTEGER
    )
''')
print("Database Created")
time.sleep(2)

cursor.execute("INSERT INTO shoe (name, stock) VALUES (?, ?)", ("Air Force", airforcesStock))
cursor.execute("INSERT INTO shoe (name, stock) VALUES (?, ?)", ("Air Max", airmaxStock))
cursor.execute("INSERT INTO shoe (name, stock) VALUES (?, ?)", ("Jordans", jordansStock))
cursor.execute("INSERT INTO shoe (name, stock) VALUES (?, ?)", ("Daybreak", daybreakStock))
print("Stock Inserted")
time.sleep(2)

conn.commit()
conn.close()

def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")
    code = msg.payload.decode()
    print(code)
    if code == "AF-":
        conn = sqlite3.connect('shoestock.db')
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM shoe WHERE id = 1")
        newAirFStock = (int(cursor.fetchone()[0]) -1)
        airFmessage = json.dumps({"airforces": newAirFStock})
        # Publish the message to the defined topic
        client.publish(airforceTopic, airFmessage)
        print(f"Airforces: Published stock level {newAirFStock}")
        cursor.execute("UPDATE shoe SET stock = ? WHERE id = ?",(newAirFStock,1))
        conn.commit()
        conn.close()
    elif code == "AM-":
        conn = sqlite3.connect('shoestock.db')
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM shoe WHERE id = 2")
        newAirMStock = (int(cursor.fetchone()[0]) -1)
        airMmessage = json.dumps({"airmax": newAirMStock})
        # Publish the message to the defined topic
        client.publish(airmaxTopic, airMmessage)
        print(f"Air Max: Published stock level {newAirMStock}")
        cursor.execute("UPDATE shoe SET stock = ? WHERE id = ?",(newAirMStock,2))
        conn.commit()
        conn.close()
    elif code == "J-":
        conn = sqlite3.connect('shoestock.db')
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM shoe WHERE id = 3")
        newJordanStock = (int(cursor.fetchone()[0]) -1)
        Jmessage = json.dumps({"jordans": newJordanStock})
        # Publish the message to the defined topic
        client.publish(jordansTopic, Jmessage)
        print(f"Jordans: Published stock level {newJordanStock}")
        cursor.execute("UPDATE shoe SET stock = ? WHERE id = ?",(newJordanStock,3))
        conn.commit()
        conn.close()
    elif code == "D-":
        conn = sqlite3.connect('shoestock.db')
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM shoe WHERE id = 4")
        newDaybreakStock = (int(cursor.fetchone()[0]) -1)
        Dmessage = json.dumps({"daybreak": newDaybreakStock})
        # Publish the message to the defined topic
        client.publish(daybreakTopic, Dmessage)
        print(f"Daybreak: Published stock level {newDaybreakStock}")
        cursor.execute("UPDATE shoe SET stock = ? WHERE id = ?",(newDaybreakStock,4))
        conn.commit()
        conn.close()




client.subscribe([("shoes/stockdec/airforces", 2), ("shoes/stockdec/airmax", 2), ("shoes/stockdec/jordans", 2), ("shoes/stockdec/daybreak", 2)])
client.on_message = on_message

client.loop_forever()
