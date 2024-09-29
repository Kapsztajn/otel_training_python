from flask import Flask, request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.propagators import extract
from opentelemetry.trace.propagation import get_current_span

# Set up tracing for Service B
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Add a console exporter to see the trace output
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Flask app to simulate Service B
app = Flask(__name__)


@app.route("/process")
def process_request():
    # Extract trace context from incoming HTTP headers (propagated from Service A)
    context = extract(request.headers)

    # Start a new span in the context of the incoming trace
    with tracer.start_as_current_span("Service B - Processing", context=context) as span:
        # Simulate processing time
        time.sleep(0.1)
        span.add_event("Service B processed the request")
        return "Service B Response", 200


# Run the Flask app (Service B)
if __name__ == "__main__":
    app.run(port=5001)
