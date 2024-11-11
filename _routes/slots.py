from flask import Blueprint, jsonify
from _utils import models

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