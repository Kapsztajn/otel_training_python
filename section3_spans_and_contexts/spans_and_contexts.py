# trace_context_example.py
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import SpanContext, Link

# Konfiguracja OpenTelemetry i eksportera konsolowego
resource = Resource.create({"service.name": os.path.basename(__file__)})
trace.set_tracer_provider(TracerProvider(resource=resource))

# Dodajemy prosty eksporter spanów do konsoli
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
span_processor = SimpleSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Tworzymy tracer
tracer = trace.get_tracer(__name__)


def process_within_span():
    # Tworzymy Minor span w ramach śladu (trace)
    with tracer.start_as_current_span("Minor Span") as span:
        span.set_attribute("operation.type", "Minor")
        print("Executing minor operation")


def main_operation():
    # Tworzymy Major span (rodzic dla podrzędnego)
    with tracer.start_as_current_span("Major Span") as parent_span:
        parent_span.set_attribute("operation.type", "Major")
        print("Executing major operation")

        # Wewnątrz nadrzędnego spana uruchamiamy Minor span
        process_within_span()


if __name__ == "__main__":
    print("Executing tracing with Major and Minor span")
    main_operation()
