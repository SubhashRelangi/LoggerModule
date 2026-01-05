from pathlib import Path

# ================= STORAGE =================
STORAGE_THRESHOLD_PERCENT = 80

# ================= FILE MANAGEMENT =================
MAX_FILE_SIZE_MB = 10
LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY_MAX_SIZE_MB = 100
MAX_COMPRESSION_PERCENT = 70

# ================= LOGGER =================
DEFAULT_FILE_TYPE = "csv"
DEFAULT_COMPRESS = False

# ================= TIMESTAMP =================
LOG_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
