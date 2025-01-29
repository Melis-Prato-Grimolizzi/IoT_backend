from _utils import models, db

"""
Cose di utilità per gestire gli slots e le sessioni di parcheggio
"""

class DuplicateSlotError(Exception):
    pass

class NotFoundError(Exception):
    pass


def get_slots():
    return models.Slot.query.all()

def get_slot(slot_id):
    return models.Slot.query.get(slot_id)

def get_slots_by_zone(zone):
    Slots = models.Slot.query.filter_by(zone=zone).all()
    if not Slots:
        raise NotFoundError
    return Slots

def add_slot(zone, parking_id, latitude, longitude):
    if models.Slot.query.filter(models.Slot.parking_id == parking_id).all():
        raise DuplicateSlotError
    slot = models.Slot(zone, parking_id, latitude, longitude)
    db.session.add(slot)
    db.session.commit()
    return slot

def delete_slot(slot_id):
    slot = models.Slot.query.get(slot_id)
    if slot is None:
        raise NotFoundError
    db.session.delete(slot)
    db.session.commit()
    return slot

def start_parking_session(user_id, slot_id, start_time):
    session = models.ParkingSession(user_id, slot_id, start_time, 0)
    db.session.add(session)
    db.session.commit()

#def end_parking_session(slot_id, end_time):
#    session = models.ParkingSession.query.filter_by(slot_id=slot_id, end_time=0).first()
#    if session is None:
#        raise NotFoundError
#    session.end_time = end_time
#    db.session.commit()
#    return session

def get_last_parking_session_not_finished(slot_id):
    return models.ParkingSession.query.filter_by(slot_id=slot_id, finished=False).order_by(models.ParkingSession.start_time.desc()).first()

def get_parking_sessions():
    return models.ParkingSession.query.all()

def get_user_parking_sessions(user_id):
    return models.ParkingSession.query.filter_by(user_id=user_id).all()

def get_last_parking_session(user_id):
    return models.ParkingSession.query.filter_by(user_id=user_id).order_by(models.ParkingSession.start_time.desc()).first()
