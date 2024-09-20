import json


def getRoom(room):
    return Room(
        room_id=room[0],
        uuid=room[1],
        floor=room[2],
        price=str(room[3]),
        building=room[4]
    ).to_dict()

class Room:
    def __init__(self, room_id, uuid, floor, price, building):
        self.room_id = room_id
        self.uuid = uuid
        self.floor = floor
        self.price = price
        self.building = building

    # Convert the class instance to a dictionary
    def to_dict(self):
        return {
            "room_id": self.room_id,
            "uuid": self.uuid,
            "floor": self.floor,
            "price": self.price,
            "building": self.building
        }

    # Convert the class instance to a JSON string
    def to_json(self):
        return json.dumps(self.to_dict())

