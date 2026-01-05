class LoggerError(Exception):
    pass


class StorageThresholdError(LoggerError):
    pass


class LoggerInitializationError(LoggerError):
    pass


class HeaderInitializationError(LoggerError):
    pass
