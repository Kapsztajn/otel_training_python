# structured_logging.py
import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.logs import LogEmitterProvider, LogEmitter, ConsoleLogExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up the OpenTelemetry Tracer Provider
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({"service.name": "my-service"}))
)
tracer = trace.get_tracer(__name__)

# Export spans to the console
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
span_processor = SimpleSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Integrate OpenTelemetry with the logging module
LoggingInstrumentor().instrument()

# Set up Python's built-in logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to simulate work and generate a log with trace/span info
def do_work():
    # Start a span
    with tracer.start_as_current_span("work-span") as span:
        trace_id = span.get_span_context().trace_id
        span_id = span.get_span_context().span_id

        # Log with structured information
        logger.info(f"Doing some work! Trace ID: {trace_id}, Span ID: {span_id}")


if __name__ == "__main__":
    do_work()
