from flask import Flask, request, jsonify
from _utils.db import init_db, session
from _utils import db, models
from _utils.models import Slot
from flask_sqlalchemy import SQLAlchemy
import _routes

app = Flask(__name__)
app.register_blueprint(_routes.users)

init_db()

#session.begin()

@app.route("/")
def root():
  #mettiamo nella tabella Slot un elemento
  slot = Slot(1)
  session.add(slot)
  session.commit()
  result = Slot.query.all()
  return jsonify([u.serialize() for u in result])

if __name__ == "__main__":
    app.run(port=5001, debug=True)
