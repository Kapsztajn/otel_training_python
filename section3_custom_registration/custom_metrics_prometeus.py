# custom_metrics.py
import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

# Set up the Meter Provider (metric management)
metrics.set_meter_provider(MeterProvider())
meter = metrics.get_meter(__name__)

# Create a Counter metric (Custom Metric 1)
items_processed_counter = meter.create_counter(
    name="items_processed",
    description="Number of processed items",
    unit="items",
)

# Create a Histogram metric (Custom Metric 2)
processing_time_histogram = meter.create_histogram(
    name="processing_time",
    description="Time taken to process an item",
    unit="ms",
)

# Register Prometheus Exporter for metrics
prometheus_exporter = PrometheusMetricReader()
metrics.get_meter_provider().add_metric_reader(prometheus_exporter)

# Start Prometheus HTTP server to expose the metrics
start_http_server(8000)  # Prometheus will scrape metrics from http://localhost:8000

# Function to simulate item processing and record metrics
def process_items():
    for i in range(10):
        # Simulate processing time
        processing_time = i * 10 + 5  # Simulated processing time
        time.sleep(0.5)

        # Update the counter metric
        items_processed_counter.add(1)

        # Record the processing time in the histogram
        processing_time_histogram.record(processing_time)

        print(f"Processed item {i + 1}, Processing time: {processing_time}ms")

if __name__ == "__main__":
    print("Processing items and exposing metrics at http://localhost:8000/metrics")
    process_items()
