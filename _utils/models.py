from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from _utils import db, consts
import jwt
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
    latitude = Column(String)
    longitude = Column(String)
    def __init__(self, zone, latitude, longitude):
        self.zone = zone
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self):
        return {
            'id': self.id,
            'zone': self.zone,
            'state': self.state,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
    
    def get_state(self):
        return self.state
    
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
    

class User(db.Model):
    """
    Modello di User della nostra app.
    """
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), unique=True)
    password = Column(String(60))
    
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

    
