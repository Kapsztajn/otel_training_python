import warnings
warnings.simplefilter("ignore", DeprecationWarning)

import json
import logging
import random
import uuid
from datetime import datetime

import psycopg2
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logger = logging.getLogger(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",  # Jaeger agent host
    agent_port=6831,  # Jaeger agent port for UDP
)

resource = Resource(attributes={"service.name": "db_facade"})  # Name of your service
provider = TracerProvider(resource=resource)
span_processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(span_processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

Psycopg2Instrumentor().instrument()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)


def get_all(table_name, transformer):
    connection = psycopg2.connect(database="otel_training", user="admin", password="pass", host="localhost", port=5432)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from {table_name};")

    result = []
    fetchall = cursor.fetchall()
    for item in fetchall:
        result.append(
            transformer(item)
        )
    if result:
        return json.dumps({'results': result})
    else:
        return json.dumps({'results': 'empty'})


def handle_null(value, default):
    return value if value else default


def insert_user(data):
    user_id = data.get('user_id', str(uuid.uuid4()))
    email = data.get('email', 'no email')
    split_name = data.get('name', "no_name no_surname").split(" ")
    first_name = split_name[0]
    last_name = split_name[1]

    insert = ("INSERT INTO users (user_id, email, first_name, last_name) "
              "VALUES (%s, %s, %s, %s)")
    connection = psycopg2.connect(database="otel_training", user="admin", password="pass", host="localhost", port=5432)

    try:
        cursor = connection.cursor()
        cursor.execute(insert, (user_id, email, first_name, last_name))
        connection.commit()
        connection.close()

        return json.dumps({'user_id': user_id})
    except Exception as e:
        logger.error(f"Error inserting data: {str(e)}")
        return json.dumps({'exception': {str(e)}})


def insert_room(data):
    room_no = data.get('no', random.randint(0, 10))
    room_id = data.get('id', str(uuid.uuid4()))
    floor = data.get('floor', random.randint(0, 10))
    price = data.get('price', random.randint(100, 1000))
    building = data.get('building', random.randint(0, 10))

    insert = ("INSERT INTO rooms (room_no, room_id, floor, price, building) "
              "VALUES (%s, %s, %s, %s, %s)")
    connection = psycopg2.connect(database="otel_training", user="admin", password="pass", host="localhost", port=5432)

    try:
        cursor = connection.cursor()
        cursor.execute(insert, (room_no, room_id, floor, price, building))
        connection.commit()
        connection.close()

        return json.dumps({'room_id': room_id})
    except Exception as e:
        logger.error(f"Error inserting data: {str(e)}")
        return json.dumps({'exception': {str(e)}})


def insert_reservation(data):
    reservation_id = data.get('reservation_id', str(uuid.uuid4()))
    user_id = data.get('user_id', str(uuid.uuid4()))
    room_id = data.get('room_id', str(uuid.uuid4()))

    insert = ("INSERT INTO reservations (reservation_id, user_id, room_id) "
              "VALUES (%s, %s, %s)")
    connection = psycopg2.connect(database="otel_training", user="admin", password="pass", host="localhost", port=5432)

    try:
        cursor = connection.cursor()
        cursor.execute(insert, (reservation_id, user_id, room_id))
        connection.commit()
        connection.close()

        return json.dumps({'reservation_id': reservation_id})
    except Exception as e:
        logger.error(f"Error inserting data: {str(e)}")
        return json.dumps({'exception': {str(e)}})


def get_item(table_name, identifier, item_id, transformer):
    connection = psycopg2.connect(database="otel_training", user="admin", password="pass", host="localhost", port=5432)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * from {table_name} where {identifier} = '{item_id}';")

    result = []
    fetchall = cursor.fetchall()
    for item in fetchall:
        result.append(
            transformer(item)
        )
    if result:
        return json.dumps({'results': result})
    else:
        return json.dumps({'results': 'empty'})
