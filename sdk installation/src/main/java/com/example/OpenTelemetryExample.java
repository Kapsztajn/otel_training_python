package com.example;

import io.opentelemetry.api.GlobalOpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;

public class OpenTelemetryExample {

    public static void main(String[] args) {
        // Configure the OTLP exporter
        OtlpGrpcSpanExporter spanExporter = OtlpGrpcSpanExporter.builder()
            .setEndpoint("http://localhost:4317")
            .build();

        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
            .addSpanProcessor(BatchSpanProcessor.builder(spanExporter).build())
            .build();

        OpenTelemetrySdk.builder().setTracerProvider(tracerProvider).buildAndRegisterGlobal();

        // Get a tracer instance
        Tracer tracer = GlobalOpenTelemetry.getTracer("exampleTracer");

        // Create and end a span
        Span span = tracer.spanBuilder("example-span").startSpan();
        span.setAttribute("key", "value");
        span.end();

        // Shutdown the SDK
        tracerProvider.shutdown();
    }
}
