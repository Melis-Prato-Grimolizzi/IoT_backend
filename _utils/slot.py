import os

import jwt
from sqlalchemy import text

from _utils import models, db, consts

"""
Cose di utilità per gestire gli slots
"""

class DuplicateSlotError(Exception):
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