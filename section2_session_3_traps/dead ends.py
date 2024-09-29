import requests
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace.status import Status, StatusCode

# Set up tracing with OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Add a console exporter to visualize spans
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)


# Circuit Breaker state
class CircuitBreaker:
    def __init__(self, max_failures, reset_timeout):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()

    def is_open(self):
        if self.failures >= self.max_failures:
            if time.time() - self.last_failure_time < self.reset_timeout:
                return True
            else:
                self.reset()
        return False

    def reset(self):
        self.failures = 0
        self.last_failure_time = None


# Instantiate the circuit breaker (allow 3 failures, reset after 10 seconds)
circuit_breaker = CircuitBreaker(max_failures=3, reset_timeout=10)


# Function to simulate an external API call with timeout and circuit breaker
def call_external_api():
    url = "https://jsonplaceholder.typicode.com/posts/1"  # Simulate a third-party API

    # Check if the circuit breaker is open
    if circuit_breaker.is_open():
        print("Circuit breaker is open. Skipping external API call.")
        return

    with tracer.start_as_current_span("External API Call") as span:
        try:
            # Simulate a network timeout for the external call (e.g., 1 second)
            response = requests.get(url, timeout=1)
            response.raise_for_status()
            span.set_status(Status(StatusCode.OK))
            span.add_event(f"Received response: {response.status_code}")

        except requests.exceptions.Timeout:
            span.set_status(Status(StatusCode.ERROR, "Timeout occurred"))
            span.add_event("Timeout occurred while calling external API")
            circuit_breaker.record_failure()

        except requests.exceptions.RequestException as e:
            span.set_status(Status(StatusCode.ERROR, f"Error: {str(e)}"))
            span.add_event(f"Failed to reach external API: {str(e)}")
            circuit_breaker.record_failure()

        else:
            print("API call successful!")
            circuit_breaker.reset()


# Simulating multiple API calls
def simulate_multiple_requests():
    for i in range(10):
        print(f"Attempt {i + 1}: Calling external API")
        call_external_api()
        time.sleep(2)  # Wait for 2 seconds between requests


# Simulate multiple API calls
simulate_multiple_requests()
