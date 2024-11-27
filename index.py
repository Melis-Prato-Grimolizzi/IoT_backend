from os import getenv
from dotenv import load_dotenv

from flask import Flask
from _routes import users, slots
from _utils import db
from _routes import *

load_dotenv()

REQUIRED_ENV_VARS = [
  "POSTGRES_PASSWORD",
  "POSTGRES_USER",
  "POSTGRES_DB"
]

missing_vars = False

for var in REQUIRED_ENV_VARS:
  if getenv(var) is None:
    print(f"Missing environment variable {var}")
    missing_vars = True

if missing_vars:
  exit(1)


app = Flask(__name__)


"""Inizializzazione del database"""

db_database = getenv("POSTGRES_DB")
db_user = getenv("POSTGRES_USER")
db_password = getenv("POSTGRES_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_password}@postgres:5432/{db_database}'

db.init_app(app)
with app.app_context():
  db.create_all()



app.register_blueprint(users.users)
app.register_blueprint(slots.slots)


if getenv("JWT_KEY") is None:
    print("Non è stata impostata una chiave per firmare i JWT, quindi verrà usata quella di test")


@app.route("/")
def root():
  return "Non c'è niente qui da vedere"

print("Avvio server")

if __name__ == "__main__":
    app.run(port=3000, debug=True, host="0.0.0.0")
