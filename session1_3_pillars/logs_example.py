import logging
from opentelemetry import logs
from opentelemetry.sdk.logs import LoggerProvider, ConsoleLogExporter, SimpleLogRecordProcessor

# Set up the logging provider
logs.set_logger_provider(LoggerProvider())
logger = logs.get_logger(__name__)

# Export logs to the console
log_exporter = ConsoleLogExporter()
log_processor = SimpleLogRecordProcessor(log_exporter)
logs.get_logger_provider().add_log_record_processor(log_processor)

# Set up the Python standard logging integration
logging.basicConfig(level=logging.INFO)
py_logger = logging.getLogger(__name__)

# Create log entries
py_logger.info("This is an info log message.")
py_logger.error("This is an error log message.")

logger.info("Custom OpenTelemetry log message.")
logger.error("Custom OpenTelemetry error log.")
