from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import requests

# Set up tracing provider and exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export traces to the console
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument HTTP requests to automatically create spans
RequestsInstrumentor().instrument()

# Manually create a trace
with tracer.start_as_current_span("parent-span"):
    with tracer.start_as_current_span("child-span"):
        response = requests.get("https://httpbin.org/get")
        print(f"Response status code: {response.status_code}")