from room import getRoom
from reservation import getReservation

from user import getUser


def roomer(room):
    return getRoom(room)


def reservator(reservation):
    return getReservation(reservation)


def useror(user):
    return getUser(user)
