import logging
import sys
from motron.domain.entity.log_level import LogLevel
from motron.core.config_loader import get_config

class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        LogLevel.TRACE: "\033[90m",   # Gray
        LogLevel.DEBUG: "\033[94m",   # Blue
        LogLevel.INFO:  "\033[92m",   # Green
        LogLevel.WARN:  "\033[93m",   # Yellow
        LogLevel.ERROR: "\033[91m",   # Red
    }
    RESET = "\033[0m"

    def format(self, record):
        try:
            level = LogLevel(record.levelname) if record.levelname in LogLevel.__members__ else LogLevel.INFO
        except ValueError:
            level = LogLevel.INFO
        color = self.COLOR_CODES.get(level, "")
        formatted = super().format(record)
        return f"{color}{formatted}{self.RESET}"

class MotronLogger:
    LEVEL_PRIORITY = {
        LogLevel.TRACE: 0,
        LogLevel.DEBUG: 1,
        LogLevel.INFO:  2,
        LogLevel.WARN:  3,
        LogLevel.ERROR: 4,
    }

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Capture everything internally

        # Determine allowed level from config
        self.allowed_level = self._resolve_level_from_config()

        if not self.logger.hasHandlers():  # ✅ FIXED: prevents double logging
            ch = logging.StreamHandler(sys.stdout)
            formatter = ColoredFormatter(
                '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        self.logger.propagate = False  # ✅ FIXED: disables propagation to parent loggers

    def _resolve_level_from_config(self):
        config = get_config().get("motron", {}).get("logging", {}).get("level", {})
        for prefix, level_str in config.items():
            if self.name.startswith(prefix):
                try:
                    return LogLevel[level_str.upper()]
                except KeyError:
                    return LogLevel.INFO
        return LogLevel.INFO

    def _should_log(self, level: LogLevel):
        return self.LEVEL_PRIORITY[level] >= self.LEVEL_PRIORITY[self.allowed_level]

    def trace(self, msg):
        if self._should_log(LogLevel.TRACE):
            self.logger.debug(f"[TRACE] {msg}")

    def debug(self, msg):
        if self._should_log(LogLevel.DEBUG):
            self.logger.debug(msg)

    def info(self, msg):
        if self._should_log(LogLevel.INFO):
            self.logger.info(msg)

    def warn(self, msg):
        if self._should_log(LogLevel.WARN):
            self.logger.warning(msg)

    def error(self, msg):
        if self._should_log(LogLevel.ERROR):
            self.logger.error(msg)

    def log(self, msg, level: LogLevel = LogLevel.INFO):
        if self._should_log(level):
            {
                LogLevel.TRACE: self.trace,
                LogLevel.DEBUG: self.debug,
                LogLevel.INFO:  self.info,
                LogLevel.WARN:  self.warn,
                LogLevel.ERROR: self.error,
            }[level](msg)
