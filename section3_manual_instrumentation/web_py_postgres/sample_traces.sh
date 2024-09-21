#!/usr/bin/env bash

set -x

curl -X POST http://localhost:8080/add_user -H "Content-Type: application/json" -d '{"user_id": "training_attendee", "email": "attendee@training.com", "name": "John Kowalski"}'




# this fails:
curl -X POST http://localhost:8080/add_rdd_reservation -H "Content-Type: application/json" -d '{}'

# DETAIL:  Key (room_id)=(someuuid) already exists.
curl -X POST http://localhost:8080/add_room -H "Content-Type: application/json" -d '{"no": "132", "id": "someuuid", "floor": 1, "price": "500", "area": "123"}'

#psycopg2.errors.ForeignKeyViolation: insert or update on table "reservations" violates foreign key constraint "reservations_user_id_fkey"
#DETAIL:  Key (user_id)=(f6a694e6-9711-40e8-83ab-dfba524bdb81) is not present in table "users".
 curl -X POST http://localhost:8080/add_reservation -H "Content-Type: application/json" -d '{}'

google-chrome-stable http://localhost:16686/