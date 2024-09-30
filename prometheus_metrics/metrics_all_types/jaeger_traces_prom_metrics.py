import time
import random
from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server

# Start up the server to expose the metrics on port 8000
start_http_server(8000)

# Counter: Monotonically increasing counter
request_counter = Counter('http_requests_total', 'Total number of HTTP requests', ['endpoint'])

# Gauge: Represents a value that can go up and down
temperature_gauge = Gauge('temperature_celsius', 'Current temperature in Celsius')

# Histogram: Records observations and counts them in configurable buckets (e.g., request durations)
request_duration_histogram = Histogram(
    'http_request_duration_seconds', 'Histogram of request duration in seconds', ['endpoint'],
    buckets=[0.1, 0.5, 1, 2, 5, 10]
)

# Summary: Tracks the size and count of events, providing quantile-based summaries
request_size_summary = Summary('http_request_size_bytes', 'Summary of HTTP request sizes in bytes', ['endpoint'])


# Simulate different metric recordings
def process_request(endpoint):
    # Simulate a random request duration
    duration = random.uniform(0.1, 5.0)

    # Increment the request counter
    request_counter.labels(endpoint=endpoint).inc()

    # Set a random temperature for the gauge
    temperature_gauge.set(random.uniform(15.0, 35.0))

    # Observe the request duration in the histogram
    request_duration_histogram.labels(endpoint=endpoint).observe(duration)

    # Observe the request size in the summary
    request_size_summary.labels(endpoint=endpoint).observe(random.uniform(500, 2000))

    # Simulate some processing time (sleep)
    time.sleep(duration)


if __name__ == "__main__":
    print("Starting Prometheus metrics collection on port 8000...")

    # Simulate metrics for 10 different requests
    endpoints = ["/api/v1/resource", "/api/v2/item", "/api/v1/user"]
    while True:
        process_request(random.choice(endpoints))
