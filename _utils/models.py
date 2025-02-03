from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from _utils import db, consts
from sqlalchemy import ForeignKey
import re
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
    car_plate = Column(String(10), nullable=True, default=None, unique=True)
    admin = Column(Boolean, default=False, nullable=True)
    
    def __init__(self, username, password, car_plate):
        self.username = username
        pwhash = hashpw(password, gensalt(consts.BCRYPT_SALT_ROUNDS))
        self.password = pwhash.decode('utf-8')
        self.car_plate = car_plate

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'car_plate': self.car_plate,
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
    
    @staticmethod
    def validate_car_plate(car_plate: str):
        if car_plate is None:
            return False
        
        # Italian car plates have the format AA123AA
        pattern = r'^[A-Z]{2}\d{3}[A-Z]{2}$'
        if not re.match(pattern, car_plate):
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
    finished = Column(Boolean, default=False, nullable=True)
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
    

class ParkingStatusHistory(db.Model):
    """
    Modello di ParkingStatusHistory della nostra app.
    """
    __tablename__ = 'ParkingStatusHistory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    parking_id = Column(Integer, ForeignKey('Slot.parking_id'), nullable=False)
    state = Column(Boolean, default=False, nullable=False)
    timestamp = Column(Integer, nullable=False)
    
    def __init__(self, parking_id, state, timestamp):
        self.parking_id = parking_id
        self.state = state
        self.timestamp = timestamp

    def serialize(self):
        return {
            'id': self.id,
            'parking_id': self.parking_id,
            'state': self.state,
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def validate_state(state: bool):
        if state is None:
            return False
        
        if not isinstance(state, bool):
            return False
        
        return True
    
    @staticmethod
    def validate_timestamp(timestamp: int):
        if timestamp is None:
            return False
        
        if not timestamp.isdigit():
            return False
        
        return True