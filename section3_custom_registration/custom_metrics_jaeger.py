# custom_tracing_jaeger.py
import os
import time

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Set up Jaeger exporter
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)

# Set up trace provider and resource with service name
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": os.path.basename(__file__)})
    )
)

# Add a BatchSpanProcessor to export spans asynchronously to Jaeger
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Get the tracer to create spans
tracer = trace.get_tracer(__name__)


# Function to simulate item processing and record traces
def process_items():
    for i in range(10):
        # Start a new span for each item processed
        with tracer.start_as_current_span("process_item") as span:
            # Simulate processing time
            processing_time = i * 10 + 5  # Simulated processing time
            time.sleep(0.5)

            # Add custom attributes to the span
            span.set_attribute("item.number", i + 1)
            span.set_attribute("processing.time_ms", processing_time)

            # Simulate work within the span
            print(f"Processed item {i + 1}, Processing time: {processing_time}ms")


if __name__ == "__main__":
    print("Processing items and exporting traces to Jaeger...")
    process_items()
