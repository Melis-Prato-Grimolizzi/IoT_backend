import os

import jwt
from sqlalchemy import text

from _utils import models, db, consts

"""
Cose di utilità per gestire gli slots
"""

class DuplicateSlotError(Exception):
    pass

class NotFoundError(Exception):
    pass

key_from_env = os.getenv("JWT_KEY")
jwt_key = consts.JWT_TEST_KEY if key_from_env is None else key_from_env

def add_slot(zone, parking_id, latitude, longitude):
    if models.Slot.query.filter(models.Slot.parking_id == parking_id).all():
        raise DuplicateSlotError
    slot = models.Slot(zone, parking_id, latitude, longitude)
    db.session.add(slot)
    db.session.commit()
    return slot

def start_parking_session(user_id, slot_id, start_time):
    session = models.ParkingSession(user_id, slot_id, start_time, 0)
    db.session.add(session)
    db.session.commit()

def end_parking_session(user_id, slot_id, end_time):
    session = models.ParkingSession.query.filter_by(user_id=user_id, slot_id=slot_id, end_time=0).first()
    if session is None:
        raise NotFoundError
    session.end_time = end_time
    db.session.commit()
    return session