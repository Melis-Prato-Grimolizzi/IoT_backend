from flask import Blueprint, jsonify, request
from _utils import models, decorators


slots = Blueprint('slots', __name__, url_prefix="/slots")


"""
Route usate per gestire gli slots.
"""

@slots.route("/", methods=["GET"])
def get_slots():
    """
    Route per ottenere tutti gli slots.
    """
    Slot = models.Slot.query.all()
    return jsonify([s.serialize() for s in Slot])


@slots.route("/slot/<slot_id>", methods=["GET"])
def get_slot(slot_id):
    """
    Route per ottenere un singolo slot.
    """
    Slot = models.Slot.query.get(slot_id)
    return jsonify(Slot.serialize())

@slots.route("/add_slot", methods=["POST"])
@decorators.admin_decorator
def add_slot(username):
    """
    Route per aggiungere uno slot.
    """
    if username != "bridge":
        return "not an admin"
    Slot = models.Slot(request.form['zone'], request.form['latitude'], request.form['longitude'])
    models.db.session.add(Slot)
    models.db.session.commit()
    return "OK"