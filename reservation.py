import json


def getReservation(reservation):
    return Reservation(
        reservation_id=reservation[0],
        user_id=reservation[1],
        room_id=reservation[2]
    ).to_dict()


class Reservation:
    def __init__(self, reservation_id, user_id, room_id):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.room_id = room_id

    # Convert the class instance to a dictionary
    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "user_id": self.user_id,
            "room_id": self.room_id
        }

    # Convert the class instance to a JSON string
    def to_json(self):
        return json.dumps(self.to_dict())
