from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.propagators import inject
import requests
import time

# Set up tracing for Service A
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Add a console exporter to see the trace output
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Service A - Simulates a client sending a request to Service B
def service_a_request_to_b():
    with tracer.start_as_current_span("Service A - Request to Service B") as span:
        # Create a dictionary to hold trace context headers
        headers = {}

        # Inject trace context into the headers (propagate traceparent and tracestate)
        inject(headers)

        # Simulate an HTTP request to Service B with trace headers
        response = requests.get("http://localhost:5001/process", headers=headers)
        print(f"Service A received response from Service B: {response.text}")

# Simulate the request from Service A
service_a_request_to_b()
