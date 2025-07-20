import csv
import json
import time
from datetime import datetime
import pywhatkit as kit

# -------- Load Config --------
with open("config.json") as f:
    config = json.load(f)

TEMPLATE = config["default_message_template"]
WAIT_TIME = config["wait_time_before_send"]
DELAY = config["message_delay_seconds"]

# -------- Load Students --------
students = []
with open("students.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        students.append({
            "name": row["name"],
            "phone": row["phone"]
        })

# -------- Send Messages --------
today = datetime.today().strftime('%d-%m-%Y')

for student in students:
    name = student["name"]
    phone = student["phone"]
    message = TEMPLATE.format(name=name, date=today)

    print(f"Sending to {name} ({phone})...")

    try:
        kit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=WAIT_TIME,
            tab_close=True
        )
        print("✅ Message sent.")
        time.sleep(DELAY)
    except Exception as e:
        print(f"❌ Failed to send to {name}: {e}")
