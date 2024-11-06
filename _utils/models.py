from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import Column, Integer, String, Boolean
from _utils import db, consts
"""
Qua vanno tutti i modelli di dato
che useremo nell'app.
"""
class Slot(db.Model):
    """
    Modello di Slot della nostra app.
    """
    __tablename__ = 'Slot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    zone = Column(Integer)
    state = Column(Boolean, default=False)
    def __init__(self, zone):
        self.zone = zone

    def serialize(self):
        return {
            'id': self.id,
            'zone': self.zone,
            'state': self.state
        }