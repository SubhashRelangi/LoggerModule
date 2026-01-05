import time
import gzip
import shutil
from pathlib import Path
from config import (
    MAX_FILE_SIZE_MB,
    LOG_DIRECTORY,
    LOG_DIRECTORY_MAX_SIZE_MB,
    MAX_COMPRESSION_PERCENT,
    LOG_TIMESTAMP_FORMAT,
)
from exceptions import LoggerInitializationError


class FileManager:
    def __init__(
        self,
        file_type: str,
        log_directory: Path = LOG_DIRECTORY,
        max_file_size_mb: int = MAX_FILE_SIZE_MB,
        dir_max_size_mb: int = LOG_DIRECTORY_MAX_SIZE_MB,
        max_compress_percent: int = MAX_COMPRESSION_PERCENT,
        compress: bool = False,
    ):
        if not file_type:
            raise LoggerInitializationError("file_type must be initialized")

        self.file_type = file_type.lstrip(".")
        self.log_dir = log_directory
        self.max_file_size = max_file_size_mb * 1024 * 1024
        self.dir_max_size = dir_max_size_mb * 1024 * 1024
        self.max_compress_percent = max_compress_percent
        self.compress = compress

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_file = self._new_log_file()

    def _new_log_file(self) -> Path:
        ts = time.strftime(LOG_TIMESTAMP_FORMAT)
        return self.log_dir / f"log_{ts}.{self.file_type}"

    def rotate_if_needed(self):
        if self.current_file.exists() and self.current_file.stat().st_size >= self.max_file_size:
            self.current_file = self._new_log_file()

    def directory_size(self) -> int:
        return sum(f.stat().st_size for f in self.log_dir.iterdir() if f.is_file())

    def compress_directory_if_needed(self):
        if not self.compress:
            return

        if self.directory_size() < self.dir_max_size:
            return

        target_size = self.dir_max_size * (self.max_compress_percent / 100)

        files = sorted(
            (f for f in self.log_dir.iterdir() if f.is_file() and not f.name.endswith(".gz")),
            key=lambda f: f.stat().st_mtime,
        )

        for file in files:
            if self.directory_size() <= target_size:
                break

            gz_path = file.with_name(file.name + ".gz")

            with open(file, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

            file.unlink()
