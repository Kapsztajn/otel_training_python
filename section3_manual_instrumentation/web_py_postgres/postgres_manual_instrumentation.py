import json
import logging
import os
import random
import uuid

import psycopg2

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)

trace.set_tracer_provider(TracerProvider(resource=Resource(attributes={"service.name": os.path.basename(__file__)})))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

logger = logging.getLogger(__name__)


def get_all(table_name, transformer):
    with tracer.start_as_current_span(f"get_all {table_name}"):
        conn = psycopg2.connect(database="otel_training", user="admin", password="root", host="localhost", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from {table_name};")
        result = []
        fetchall = cursor.fetchall()
        for item in fetchall:
            result.append(
                transformer(item)
            )
        if result:
            trace.get_current_span().add_event(name='rows fetch successful', attributes={'size': len(result)})
            return json.dumps({'results': result})
        else:
            trace.get_current_span().add_event(name='rows fetch failed')
            return json.dumps({'results': 'empty'})


def amazing_python(table_name, transformer):
    with tracer.start_as_current_span(f"amazing_python {table_name}"):
        invalid_password = "INVALID PASSWORD"
        conn = psycopg2.connect(database="otel_training", user="admin", password=invalid_password, host="localhost", port=5432)
        trace.get_current_span().add_event(f"connect with invalid password: {invalid_password} worked!! ")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from {table_name};")
        result = []
        fetchall = cursor.fetchall()
        for item in fetchall:
            result.append(
                transformer(item)
            )
        if result:
            trace.get_current_span().add_event(name='rows fetch successful', attributes={'size': len(result)})
            return json.dumps({'results': result})
        else:
            trace.get_current_span().add_event(name='rows fetch failed')
            return json.dumps({'results': 'empty'})


def fail(table_name, transformer):
    with tracer.start_as_current_span(f"fail {table_name}"):
        conn = psycopg2.connect(database="otel_training", user="!admin", password="INVALID PASSWORD", host="localhost", port=5432)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from {table_name};")
        result = []
        fetchall = cursor.fetchall()
        for item in fetchall:
            result.append(
                transformer(item)
            )
        if result:
            trace.get_current_span().add_event(name='rows fetch successful', attributes={'size': len(result)})
            return json.dumps({'results': result})
        else:
            trace.get_current_span().add_event(name='rows fetch failed')
            return json.dumps({'results': 'empty'})


def insert_user(data):
    with tracer.start_as_current_span(f"insert_user {data}"):
        user_id = data.get('user_id', str(uuid.uuid4()))
        email = data.get('email', 'no email')
        split_name = data.get('name', "no_name no_surname").split(" ")
        first_name = split_name[0]
        last_name = split_name[1]

        insert = ("INSERT INTO users (user_id, email, first_name, last_name) "
                  "VALUES (%s, %s, %s, %s)")
        trace.get_current_span().add_event(name='get connection')
        connection = psycopg2.connect(database="otel_training", user="admin", password="root", host="localhost", port=5432)
        trace.get_current_span().add_event(name='get cursor')

        try:
            cursor = connection.cursor()
            trace.get_current_span().add_event(name='execute sql')
            cursor.execute(insert, (user_id, email, first_name, last_name))
            trace.get_current_span().add_event(name='commit')
            connection.commit()
            trace.get_current_span().add_event(name='close connection')
            connection.close()

            trace.get_current_span().set_attribute('set attribute', 'example')
            trace.get_current_span().add_event(name='insert', attributes={'add insert event': user_id})
            trace.get_current_span().set_status(trace.Status(trace.StatusCode.OK), "hurra! ")
            return json.dumps({'user_id': user_id})
        except Exception as e:
            trace.get_current_span().record_exception(e)
            trace.get_current_span().set_status(trace.Status(trace.StatusCode.ERROR), "damn... ")
            logger.error(f"Error inserting data: {str(e)}")
            return json.dumps({'exception': {str(e)}})


def insert_room(data):
    with tracer.start_as_current_span(f"insert_room {data}"):
        room_no = data.get('no', random.randint(0, 10))
        room_id = data.get('id', str(uuid.uuid4()))
        floor = data.get('floor', random.randint(0, 10))
        price = data.get('price', random.randint(100, 1000))
        building = data.get('building', random.randint(0, 10))

        insert = ("INSERT INTO rooms (room_no, room_id, floor, price, building) "
                  "VALUES (%s, %s, %s, %s, %s)")
        connection = psycopg2.connect(database="otel_training", user="admin", password="root", host="localhost", port=5432)

        try:
            cursor = connection.cursor()
            cursor.execute(insert, (room_no, room_id, floor, price, building))
            connection.commit()
            connection.close()

            return json.dumps({'room_id': room_id})
        except Exception as e:
            trace.get_current_span().record_exception(e)
            logger.error(f"Error inserting data: {str(e)}")
            return json.dumps({'exception': {str(e)}})


def insert_reservation(data):
    with tracer.start_as_current_span(f"insert_reservation {str(data)}"):
        reservation_id = data.get('reservation_id', str(uuid.uuid4()))
        user_id = data.get('user_id', str(uuid.uuid4()))
        room_id = data.get('room_id', str(uuid.uuid4()))

        insert = ("INSERT INTO reservations (reservation_id, user_id, room_id) "
                  "VALUES (%s, %s, %s)")
        connection = psycopg2.connect(database="otel_training", user="admin", password="root", host="localhost", port=5432)

        try:
            cursor = connection.cursor()
            cursor.execute(insert, (reservation_id, user_id, room_id))
            connection.commit()
            connection.close()

            return json.dumps({'reservation_id': reservation_id})
        except Exception as e:
            trace.get_current_span().record_exception(e)
            logger.error(f"Error inserting data: {str(e)}")
            return json.dumps({'exception': {str(e)}})


def get_item(table_name, identifier, item_id, transformer):
    with tracer.start_as_current_span(f"get_item from: {table_name}, identifier: {identifier}, id: {item_id}"):
        conn = psycopg2.connect(database="otel_training", user="admin", password="root", host="localhost", port=5432)
        cursor = conn.cursor()
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
