import os

from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup OpenTelemetry Tracing with Jaeger and OTLP
resource = Resource(attributes={"service.name": "flask-service"})
trace.set_tracer_provider(TracerProvider(resource=resource))

# OTLP exporter configuration
# Assumes you are sending traces to an OpenTelemetry Collector at localhost:4317
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)

# Add the OTLP exporter to the trace processor
otlp_span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(otlp_span_processor)

# Initialize Flask application
app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

tracer = trace.get_tracer(__name__)

@app.route('/')
def hello_world():      
    with tracer.start_as_current_span("mainEndpoint"):
        return jsonify(message="Hello, World!")

@app.route('/items/<item_id>')
def get_item(item_id):
    with tracer.start_as_current_span(f"itemsEndpoint {item_id}"):
        return jsonify(item_id=item_id, name=f"Item {item_id}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
