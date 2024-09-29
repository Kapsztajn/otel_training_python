from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._metrics import Counter, UpDownCounter, Histogram, ObservableGauge
import random
import time

# Setup Meter Provider and Exporter
resource = Resource.create(attributes={"service.name": "metrics-example"})
exporter = ConsoleMetricExporter()
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
meter_provider = MeterProvider(resource=resource, metric_readers=[reader])

metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Counter Example: Increment a value over time
requests_counter = meter.create_counter(
    name="requests_counter",
    description="Counts the number of requests served",
    unit="1"
)

# UpDownCounter Example: A counter that can go up and down
active_connections = meter.create_up_down_counter(
    name="active_connections",
    description="Tracks the number of active connections",
    unit="1"
)

# Histogram Example: Distribution of request durations
request_duration_histogram = meter.create_histogram(
    name="request_duration_histogram",
    description="Distribution of request durations",
    unit="ms"
)

# Gauge Example: Observes a fluctuating metric
def cpu_usage_observer(observer):
    cpu_usage = random.uniform(0, 100)  # Simulate CPU usage between 0-100%
    observer.observe(cpu_usage, {})

meter.create_observable_gauge(
    name="cpu_usage",
    callbacks=[cpu_usage_observer],
    description="Tracks the CPU usage",
    unit="percentage"
)

# Simulate Metrics Collection
def simulate_metrics():
    for _ in range(10):
        # Simulate request count
        requests_counter.add(1)

        # Simulate active connections fluctuating
        active_connections.add(random.randint(-1, 1))

        # Simulate request durations
        request_duration_histogram.record(random.uniform(10, 500))

        time.sleep(1)

if __name__ == "__main__":
    simulate_metrics()
