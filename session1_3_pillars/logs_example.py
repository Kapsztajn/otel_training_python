import logging

from opentelemetry.sdk._logs import LoggingHandler, LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk.resources import Resource

# Define a resource (to identify your service in traces)
resource = Resource.create(attributes={"service.name": "my-python-service"})

# Create a LoggerProvider with the resource
logger_provider = LoggerProvider(resource=resource)

# Create an OTLP exporter (logs are sent to a collector running on localhost:4317 by default)
otlp_log_exporter = OTLPLogExporter()

# Add a BatchLogRecordProcessor to handle batch exporting of logs
logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))

# Integrate the Python logging module with OpenTelemetry
logging_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)

# Set up the Python logging module to use the OpenTelemetry handler
logging.basicConfig(level=logging.INFO)
logging.getLogger().addHandler(logging_handler)

# Example logger
logger = logging.getLogger(__name__)

# Log some test messages
logger.info("OpenTelemetry logging is working!")
logger.error("This is an error message")
logger.warning("This is a warning message")

# Ensure that logs are flushed before program exit
logger_provider.shutdown()
