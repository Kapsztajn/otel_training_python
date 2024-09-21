import json
import web
import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)

trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "db-facade-prot2o"})))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

logger = logging.getLogger(__name__)

import db_facade
import transformers

urls = (
    # get all
    '/all_rooms', 'all_rooms',
    '/all_reservations', 'all_reservations',
    '/all_users', 'all_users',

    # get particular
    '/rooms/(.*)', 'get_room',
    '/reservations/(.*)', 'get_reservation',
    '/users/(.*)', 'get_user',

    # post/add particular
    '/add_room', 'add_room',
    '/add_reservation', 'add_reservation',
    '/add_user', 'add_user'
)

app = web.application(urls, globals())


class all_rooms:
    def GET(self):
        with tracer.start_as_current_span("test"):
            return db_facade.get_all('rooms', transformers.roomer)


class all_reservations:
    def GET(self):
        return db_facade.get_all('reservations', transformers.reservator)


class all_users:
    def GET(self):
        return db_facade.get_all('users', transformers.useror)


class get_room:
    def GET(self, item_id):
        return db_facade.get_item('rooms', 'room_id', item_id, transformers.roomer)


class get_reservation:
    def GET(self, item_id):
        return db_facade.get_item('reservations', 'reservation_id', item_id, transformers.reservator)


class get_user:
    def GET(self, item_id):
        return db_facade.get_item('users', 'user_id', item_id, transformers.useror)


class add_room:
    def POST(self):
        data = json.loads(web.data().decode('utf-8'))
        return db_facade.insert_room(data)


class add_reservation:
    def POST(self):
        data = json.loads(web.data().decode('utf-8'))
        return db_facade.insert_reservation(data)


class add_user:
    def POST(self):
        data = json.loads(web.data().decode('utf-8'))
        return db_facade.insert_user(data)


if __name__ == "__main__":
    app.run()
