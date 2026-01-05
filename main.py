import time
from datetime import datetime
from storage import SystemStorage
from logger import BasicLogger


def realtime_hms_ms():
    now = datetime.now()
    return now.strftime("%H:%M:%S") + f":{now.microsecond // 1000:03d}"


# 1️⃣ Storage check
SystemStorage().check()

# 2️⃣ Initialize logger
logger = BasicLogger()
logger.initialize_logger(file_type="csv", compress=True)

# 3️⃣ Headers
logger.headers("time", "sensor", "value", "status")

# 4️⃣ Start logging
logger.start()

i = 0
while logger.running:
    logger.logs([realtime_hms_ms(), "CAM01", i, "OK"])
    i += 1
    time.sleep(0.5)
