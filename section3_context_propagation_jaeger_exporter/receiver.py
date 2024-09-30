# script_b.py
import os

from flask import Flask, request
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import extract
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up the OpenTelemetry Tracer Provider
trace.set_tracer_provider(TracerProvider(resource=Resource(attributes={"service.name": os.path.basename(__file__)})))
tracer = trace.get_tracer(__name__)

# Export traces to the jaeger
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
span_processor = SimpleSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)


@app.route("/receive", methods=["GET"])
def receive():
    # Extract the context from the incoming request headers
    context = extract(request.headers)

    # Start a new span with the extracted context, continuing the trace
    with tracer.start_as_current_span("span-script-B", context=context) as span:
        # Simulate some work in Script B
        return "Processed in Script B!"


if __name__ == "__main__":
    app.run(port=5000)
