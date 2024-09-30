import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from prometheus_client import start_http_server, Counter

# Set up the meter provider
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)

# Start the Prometheus HTTP server on port 8000
start_http_server(8000)

# Create a custom Prometheus metric
request_counter = Counter('request_counter', 'Counts the number of requests')

# Create a counter to track the number of requests
request_counter = meter.create_counter(
    name="request_counter",
    description="Counts the number of requests",
    unit="requests"
)

# Create a histogram to track response time
response_time_histogram = meter.create_histogram(
    name="response_time",
    description="Tracks the response time of requests",
    unit="ms"
)

# Simulate a request and record prometheus_metrics
for _ in range(50):
    request_counter.add(1)
    response_time = 100 + (time.time() % 1) * 100  # Simulate response time
    response_time_histogram.record(response_time)
    print(f"Request completed in {response_time:.2f}ms")
    time.sleep(1)
