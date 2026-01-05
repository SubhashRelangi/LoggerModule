import signal
from file_manager import FileManager
from exceptions import LoggerInitializationError, HeaderInitializationError


class BasicLogger:
    def __init__(self):
        self.file_manager = None
        self.headers_list = None
        self.running = False

    def initialize_logger(self, file_type: str, compress: bool = False) -> bool:
        if not file_type:
            raise LoggerInitializationError("file_type must be initialized")

        self.file_manager = FileManager(
            file_type=file_type,
            compress=compress
        )
        return True

    def headers(self, *headers) -> bool:
        if not self.file_manager:
            raise HeaderInitializationError("logger not initialized")

        if not headers:
            raise HeaderInitializationError("headers cannot be empty")

        self.headers_list = headers

        with open(self.file_manager.current_file, "a") as f:
            f.write(",".join(headers) + "\n")

        return True

    def start(self):
        """Start logger loop control (CTRL+C safe)."""
        self.running = True
        signal.signal(signal.SIGINT, self._stop)

    def _stop(self, sig, frame):
        print("\n[LOGGER] Stopping safely...")
        self.running = False

    def logs(self, payload):
        if not self.headers_list:
            raise HeaderInitializationError("headers not initialized")

        self.file_manager.rotate_if_needed()

        with open(self.file_manager.current_file, "a") as f:
            f.write(",".join(map(str, payload)) + "\n")

        self.file_manager.compress_directory_if_needed()
