import logging
import os

import psycopg2
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)

# Initialize the OpenTelemetry Tracer
trace.set_tracer_provider(TracerProvider(resource=Resource(attributes={"service.name": os.path.basename(__file__)})))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

# Configure exporter to display spans on console

# Automatically instrument Psycopg2 (PostgreSQL)
Psycopg2Instrumentor().instrument()

# Database connection parameters
db_config = {
    'dbname': 'otel_training',
    'user': 'admin',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# Create a connection to the PostgreSQL database
connection = None

try:
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # Example SQL query (Psycopg2Instrumentor will automatically instrument this)
    query = "SELECT * FROM users;"
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        logger.info(f"Record: {record}")

    query = "SELECT * FROM rooms;"
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        logger.info(f"Record: {record}")

    query = "SELECT * FROM reservations;"
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        logger.info(f"Record: {record}")

except Exception as e:
    logger.error(f"Error occurred: {e}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()

    # Uninstrument psycopg2 after usage
    Psycopg2Instrumentor().uninstrument()
