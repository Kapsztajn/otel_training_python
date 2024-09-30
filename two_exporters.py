import os

from flask import Flask, jsonify
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup OpenTelemetry Tracing with Jaeger and OTLP
resource = Resource(attributes={"service.name": os.path.basename(__file__)})
trace.set_tracer_provider(TracerProvider(resource=resource))

# Jaeger exporter configuration
jaeger_exporter = JaegerExporter(
    agent_host_name='localhost',  # Jaeger agent host
    agent_port=6831,              # Default Jaeger agent port
)

# OTLP exporter configuration
# Assumes you are sending traces to an OpenTelemetry Collector at localhost:4317
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)

# Add the Jaeger exporter to the trace processor
jaeger_span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(jaeger_span_processor)

# Add the OTLP exporter to the trace processor
otlp_span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(otlp_span_processor)

# Initialize Flask application
app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/items/<item_id>')
def get_item(item_id):
    return jsonify(item_id=item_id, name=f"Item {item_id}")

if __name__ == "__main__":
    app.run(debug=True)
