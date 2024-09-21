# script_b.py
from flask import Flask, request
from opentelemetry import trace
from opentelemetry.propagate import extract
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Set up the OpenTelemetry Tracer Provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export traces to the console
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
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
