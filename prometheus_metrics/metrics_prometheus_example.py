from prometheus_client import start_http_server, Counter
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
import time

# Set up OpenTelemetry MeterProvider
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)

# Create a custom Prometheus metric
request_counter = Counter('request_counter', 'Counts the number of requests')

# Start the Prometheus HTTP server on port 8000
start_http_server(8000)

# Function to simulate requests and increment counter
def simulate_request():
    request_counter.inc()  # Increment the Prometheus counter
    print("Request simulated, counter incremented.")

if __name__ == "__main__":
    while True:
        simulate_request()
        time.sleep(5)
