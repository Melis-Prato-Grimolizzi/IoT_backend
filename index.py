from os import getenv
from dotenv import load_dotenv

from flask import Flask, jsonify
from _utils import db
from _utils.models import Slot
import _routes

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


db_database = getenv("POSTGRES_DB")
db_user = getenv("POSTGRES_USER")
db_password = getenv("POSTGRES_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_password}@postgres:5432/{db_database}'

db.init_app(app)
with app.app_context():
  db.create_all()

app.register_blueprint(_routes.users)


@app.route("/")
def root():
  #mettiamo nella tabella Slot un elemento
  slot = Slot(1)
  db.session.add(slot)
  db.session.commit()
  result = Slot.query.all()
  return jsonify([s.serialize() for s in result])

print("Avvio server")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
