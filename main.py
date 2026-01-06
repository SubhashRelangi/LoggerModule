import time
from datetime import datetime
from storage import SystemStorage
from logger import BasicLogger


def realtime_hms_ms():
    now = datetime.now()
    return now.strftime("%H:%M:%S") + f":{now.microsecond // 1000:03d}"


SystemStorage().check()

logger = BasicLogger()
logger.initialize_logger(file_type="csv", compress=True)

logger.headers("time", "sensor", "value", "status")

logger.start()

i = 0
while logger.running:
    logger.logs([realtime_hms_ms(), "CAM01", i, "OK"])
    i += 1
    time.sleep(0.5)
