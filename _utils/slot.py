import os

import jwt
from sqlalchemy import text

from _utils import models, db, consts

"""
Cose di utilità per gestire gli slots
"""

key_from_env = os.getenv("JWT_KEY")
jwt_key = consts.JWT_TEST_KEY if key_from_env is None else key_from_env