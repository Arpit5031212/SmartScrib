from contextvars import ContextVar
import json
import logging
from datetime import datetime, timezone



request_id_var: ContextVar[str] = ContextVar("request_id", default="no-request-id")

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        super().format(record)  # Call the base class format to populate record attributes
        log_dict = {
            "request_id": request_id_var.get(),
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "module": record.module,
            "lineno": record.lineno,
        }
        if record.exc_text:
            log_dict["exception"] = record.exc_text
            
        return json.dumps(log_dict)
    

def setup_logging(environment: str, debug: bool) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    handler = logging.StreamHandler()
    
    formatter = JSONFormatter() if environment == "PROD" else logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.getLogger("httpx").setLevel(logging.WARNING)  # Suppress httpx debug logs in production
    logging.getLogger("chromadb").setLevel(logging.WARNING)  # Suppress chromadb debug logs in production
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)