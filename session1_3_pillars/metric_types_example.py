import time
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# 1. Set up resource that applies to both metrics and traces
resource = Resource.create(attributes={"service.name": "my-service"})

### TRACING SETUP ###

# 2. Set up Tracer Provider and Jaeger Exporter
trace.set_tracer_provider(TracerProvider(resource=resource))

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",  # Adjust this based on where Jaeger is running
    agent_port=6831,  # Default UDP port for Jaeger
)

# Add a BatchSpanProcessor to send spans to Jaeger
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer(__name__)

### METRICS SETUP ###

# 3. Set up Meter Provider and Prometheus Exporter
start_http_server(8000)  # Prometheus server to scrape metrics on port 8000

# Use PrometheusMetricReader to expose metrics to Prometheus
prometheus_reader = PrometheusMetricReader()

# Set up MeterProvider with the Prometheus reader
metrics.set_meter_provider(MeterProvider(metric_readers=[prometheus_reader]))

meter = metrics.get_meter(__name__)

# Create instruments for metrics
request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1",
)

request_latency_histogram = meter.create_histogram(
    name="http_request_duration_seconds",
    description="Histogram of request duration in seconds",
    unit="s",
)

### SIMULATE TRACING AND METRICS ###

def simulate_requests():
    for i in range(10):
        with tracer.start_as_current_span("http_request"):
            # Increment the request counter
            request_counter.add(1, attributes={"endpoint": "/api/v1/resource"})

            # Record a latency in the histogram
            latency = 0.1 + i * 0.05
            request_latency_histogram.record(latency, attributes={"endpoint": "/api/v1/resource"})

            time.sleep(1)  # Simulate some processing time

if __name__ == "__main__":
    simulate_requests()
