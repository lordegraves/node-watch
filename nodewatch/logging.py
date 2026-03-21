import json
import logging
import sys
from datetime import datetime, timezone
from nodewatch import config


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }

        extra_data = getattr(record, "extra", None)
        if isinstance(extra_data, dict):
            log_record.update(extra_data)

        return json.dumps(log_record)


def get_logger(name: str = "nodewatch") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)

    if config.LOG_JSON:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )

    logger.addHandler(handler)
    logger.setLevel(config.LOG_LEVEL)
    logger.propagate = False

    return logger