from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from _utils import db, consts
from sqlalchemy import ForeignKey
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
    zone = Column(Integer, nullable=False)
    parking_id = Column(Integer, unique=True, nullable=False)
    state = Column(Boolean, default=False, nullable=False)
    latitude = Column(DECIMAL(10,8), nullable=False)
    longitude = Column(DECIMAL(11,8), nullable=False)
    def __init__(self, zone, parking_id, latitude, longitude):
        self.zone = zone
        self.parking_id = parking_id
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self):
        return {
            'id': self.id,
            'zone': self.zone,
            'parking_id': self.parking_id,
            'state': self.state,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    
    @staticmethod
    def validate_zone(zone: int):
        if zone is None:
            return False
        
        if not zone.isdigit():
            return False
        
        return True
    
    @staticmethod
    def validate_latitude(latitude: str):
        if latitude is None:
            return False
        
        if not latitude.replace('.', '', 1).isdigit():
            return False
        
        return True
    
    @staticmethod
    def validate_longitude(longitude: str):
        if longitude is None:
            return False
        
        if not longitude.replace('.', '', 1).isdigit():
            return False
        
        return True
    
    @staticmethod
    def validate_parking_id(parking_id: int):
        if parking_id is None:
            return False
        
        if not parking_id.isdigit():
            return False
        
        return True
    

class User(db.Model):
    """
    Modello di User della nostra app.
    """
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        pwhash = hashpw(password, gensalt(consts.BCRYPT_SALT_ROUNDS))
        self.password = pwhash.decode('utf-8')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    @staticmethod
    def validate_password(password: str):
        if password is None:
            return False
        
        if len(password) < consts.MIN_PASSWORD_LENGTH or len(password) > consts.MAX_PASSWORD_LENGTH:
            return False
        
        for char in password:
            if not char.isprintable():
                return False
        return True
    
    @staticmethod
    def validate_username(username: str):
        if username is None:
            return False
        
        if len(username) < consts.MIN_USERNAME_LENGTH or len(username) > consts.MAX_USERNAME_LENGTH:
            return False
        
        for char in username:
            if not char.isalnum():
                return False
        return True


class ParkingSession(db.Model):
    """
    Modello di ParkingSession della nostra app.
    """
    __tablename__ = 'ParkingSession'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    slot_id = Column(Integer, ForeignKey('Slot.id'), nullable=False)
    start_time = Column(Integer, nullable=True)
    end_time = Column(Integer, nullable=True)
    amount = Column(DECIMAL(10,2), nullable=True)
    #per completezza forse è meglio aggiungere anche un campo finished (booleano) per sapere se la sessione è finita
    #probabilmente bisognerà aggiungere un campo per la targa dell'auto
    
    def __init__(self, user_id, slot_id, start_time, end_time):
        self.user_id = user_id
        self.slot_id = slot_id
        self.start_time = start_time
        self.end_time = end_time

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'slot_id': self.slot_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'amount': self.amount
        }
    