import os
import time
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

# # Set up TracerProvider with a resource name
# trace.set_tracer_provider(
#     TracerProvider(
#         resource=Resource.create({"service.name": os.path.basename(__file__)})
#     )
# )

# Configure OTLP exporter to send data to the OpenTelemetry Collector
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4371", insecure=True)

# Add a BatchSpanProcessor for batching and sending spans
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Get a tracer to create spans
tracer = trace.get_tracer(__name__)


def process_items():
    for i in range(5):
        # Start a span
        with tracer.start_as_current_span("process_item") as span:
            span.set_attribute("item.number", i + 1)
            span.set_attribute("item.processing_time_ms", i * 100)

            # Simulate processing time
            time.sleep(0.5)
            print(f"Processed item {i + 1}")


if __name__ == "__main__":
    print("Processing items and sending traces to OpenTelemetry Collector...")
    process_items()
