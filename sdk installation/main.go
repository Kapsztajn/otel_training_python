package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/jaeger"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	"go.opentelemetry.io/otel/trace"
	"go.opentelemetry.io/otel/sdk/resource"
	semconv "go.opentelemetry.io/otel/semconv/v1.4.0"
)

// InitTracer initializes an OpenTelemetry tracer provider and sets up Jaeger exporter
func InitTracer() func(context.Context) error {
	// Configure the Jaeger exporter
	exporter, err := jaeger.New(jaeger.WithCollectorEndpoint(jaeger.WithEndpoint("http://localhost:14268/api/traces")))
	if err != nil {
		log.Fatalf("Failed to create the Jaeger exporter: %v", err)
	}

	// Create a resource (attributes that apply to all spans)
	res, err := resource.New(context.Background(),
		resource.WithAttributes(
			semconv.ServiceNameKey.String("go-opentelemetry-example"),
		),
	)
	if err != nil {
		log.Fatalf("Could not set resources: %v", err)
	}

	// Create the tracer provider
	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exporter),
		sdktrace.WithResource(res),
	)

	// Set the global tracer provider
	otel.SetTracerProvider(tp)

	return tp.Shutdown
}

func main() {
	// Initialize the tracer
	shutdown := InitTracer()
	defer func() {
		if err := shutdown(context.Background()); err != nil {
			log.Fatalf("Error shutting down tracer: %v", err)
		}
	}()

	// Instrument the HTTP handler
	handler := http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) {
		ctx := req.Context()
		span := trace.SpanFromContext(ctx)
		span.AddEvent("Handling request")
		fmt.Fprintf(w, "Hello, OpenTelemetry!")
	})

	// Use the otelhttp middleware to instrument the handler
	wrappedHandler := otelhttp.NewHandler(handler, "HelloHandler")

	// Start the HTTP server
	http.Handle("/", wrappedHandler)
	log.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Failed to start the server: %v", err)
	}
}
