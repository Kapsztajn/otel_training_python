from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased, ALWAYS_ON
from opentelemetry.trace import Status, StatusCode
from random import randint


class AdaptiveSampler:
    def __init__(self, error_sampler, success_sampler):
        self.error_sampler = error_sampler
        self.success_sampler = success_sampler

    def should_sample(self, span_context, trace_id, name, kind, attributes, links):
        # Check if the request is an error or a success
        if attributes.get("is_error", False):
            return self.error_sampler.should_sample(span_context, trace_id, name, kind, attributes, links)
        else:
            return self.success_sampler.should_sample(span_context, trace_id, name, kind, attributes, links)

    def get_description(self):
        return f"AdaptiveSampler(success={self.success_sampler.get_description()}, error={self.error_sampler.get_description()})"


# Define the custom sampler
adaptive_sampler = AdaptiveSampler(
    error_sampler=ALWAYS_ON,  # 100% sampling for error requests
    success_sampler=TraceIdRatioBased(1 / 1000)  # Sample 1 in 1000 for successful requests
)

# Set up the tracer provider with the custom sampler
trace.set_tracer_provider(TracerProvider(sampler=adaptive_sampler))

# Set up an exporter to visualize spans (console in this case)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Get the tracer
tracer = trace.get_tracer(__name__)

# Simulate different requests with success or error
def simulate_request(is_error=False):
    with tracer.start_as_current_span("http_request", attributes={"is_error": is_error}) as span:
        if is_error:
            span.set_status(Status(StatusCode.ERROR, "Error processing request"))
        else:
            span.set_status(Status(StatusCode.OK, "Request successful"))
        print(f"Span created for {'error' if is_error else 'success'} request")


# Simulate 10 requests (randomly some with errors)
for _ in range(10):
    simulate_request(is_error=randint(0, 10) > 8)  # 20% chance of error
