# script_a.py
import requests
from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Set up the OpenTelemetry Tracer Provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export traces to the console
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument the requests library to automatically inject trace context
RequestsInstrumentor().instrument()

# Start a new span
with tracer.start_as_current_span("span-script-A") as span:
    headers = {}
    inject(headers)  # Inject current span context into headers

    # Send HTTP request to Script B with the propagated context
    response = requests.get("http://localhost:5000/receive", headers=headers)
    print(f"Response from Script B: {response.text}")
