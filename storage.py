import shutil
from exceptions import StorageThresholdError
from config import STORAGE_THRESHOLD_PERCENT


class SystemStorage:
    def __init__(self, threshold_percent: int = STORAGE_THRESHOLD_PERCENT):
        self.threshold = threshold_percent

    def check(self) -> bool:
        usage = shutil.disk_usage("/")
        used_percent = (usage.used / usage.total) * 100

        if used_percent >= self.threshold:
            raise StorageThresholdError(
                f"can't initialize due to low memory (used={used_percent:.2f}%)"
            )

        return True
