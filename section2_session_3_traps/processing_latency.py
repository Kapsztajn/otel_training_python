import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan
import time
import threading

# Define resources (optional: specify service details like name and version)
resource = Resource(attributes={
    "service.name": os.path.basename(__file__),
    "service.version": "1.0.0"
})

# Set the Tracer Provider with buffering and asynchronous processing
trace.set_tracer_provider(TracerProvider(resource=resource))

# Create a console exporter (in real use, this would be a telemetry backend exporter like Jaeger)
console_exporter = ConsoleSpanExporter()

# BatchSpanProcessor handles spans asynchronously, buffers them, and exports in batches
# max_queue_size: Maximum size of the span queue
# max_export_batch_size: Maximum number of spans to send in a batch
# schedule_delay_millis: Delay in milliseconds between export batches
batch_processor = BatchSpanProcessor(
    console_exporter,
    max_queue_size=2048,  # Maximum size of the internal span queue
    max_export_batch_size=512,  # Maximum number of spans sent in a single batch
    schedule_delay_millis=5000  # Send spans every 5 seconds if the batch isn't full
)

# Add the processor to the tracer provider
trace.get_tracer_provider().add_span_processor(batch_processor)

# Get a tracer instance
tracer = trace.get_tracer(__name__)


# Simulating telemetry data collection with asynchronous processing
def simulate_request(request_id, is_error=False):
    with tracer.start_as_current_span(f"request_{request_id}") as span:
        if is_error:
            span.set_status(trace.Status(trace.StatusCode.ERROR, "Error occurred"))
        else:
            span.set_status(trace.Status(trace.StatusCode.OK, "Request processed successfully"))

        # Simulating some processing time
        time.sleep(0.1)
        print(f"Span created for {'error' if is_error else 'success'} request: {request_id}")


# Simulate high volume requests in multiple threads
def simulate_traffic():
    for i in range(100):  # Simulate 100 requests
        # 20% chance to simulate an error request
        threading.Thread(target=simulate_request, args=(i, i % 5 == 0)).start()


# Start the traffic simulation
simulate_traffic()

# Allow enough time for spans to be processed and exported
time.sleep(10)
