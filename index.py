from flask import Flask, request, jsonify
from _utils.db import init_db
from _utils import db, models
from flask_sqlalchemy import SQLAlchemy
import _routes

app = Flask(__name__)
app.register_blueprint(_routes.users)

init_db()

@app.route("/")
def root():
  prova_stampa_slot = models.Slot.query.all()
  return jsonify(prova_stampa_slot) 

if __name__ == "__main__":
    app.run(port=5001, debug=True)
