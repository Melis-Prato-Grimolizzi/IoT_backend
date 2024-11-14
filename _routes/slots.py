from flask import Blueprint, jsonify, request, Response
from _utils import models, decorators, slot


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
    return jsonify(Slot.serialize()) if Slot is not None else Response("not found", 404)



@slots.route("/add_slot", methods=["POST"])
@decorators.FormValidatorDecorator(
    required_fields=["zone", "latitude", "longitude", "parking_id"],
    validators=[models.Slot.validate_zone, models.Slot.validate_latitude, models.Slot.validate_longitude, models.Slot.validate_parking_id]
)
@decorators.admin_decorator
def add_slot():
    """
    Route per aggiungere uno slot.
    """
    try:
        slot.add_slot(request.form['zone'], request.form['parking_id'], request.form['latitude'], request.form['longitude'])
        return Response("OK", status=201)
    except slot.DuplicateSlotError:
        return Response("slot conflict, the id is already in use", status=409)



@slots.route("/delete_slot/<slot_id>", methods=["DELETE"])
@decorators.admin_decorator
def delete_slot(slot_id):
    """
    Route per eliminare uno slot.
    """
    Slot = models.Slot.query.get(slot_id)
    if Slot is None:
        return Response("not found", 404)
    models.db.session.delete(Slot)
    models.db.session.commit()
    return "OK"



@slots.route("/update_slot_state/<slot_id>", methods=["POST"])
@decorators.auth_decorator
def update_slot(user_id, slot_id):
    """
    Route per aggiornare lo stato dello slot.
    """
    print("L'utente {} ha cambiato lo stato dello slot {}".format(user_id, slot_id))
    Slot = models.Slot.query.get(slot_id)
    if Slot is None:
        return Response("not found", 404)
    if Slot.state is False: #significa che l'utente si è parcheggiato quindi bisogna anche far partire il timer per il pagamento
        print("L'utente {} si è parcheggiato nello slot {}".format(user_id, slot_id))
        Slot.state = not Slot.state
    elif Slot.state is True: #significa che l'utente sta lasciando lo slot quindi bisogna fermare il timer
        print("L'utente {} sta lasciando lo slot {}".format(user_id, slot_id))
        Slot.state = not Slot.state
    models.db.session.commit()
    
    return "OK"



@slots.route("/get_slot_state/<slot_id>", methods=["GET"])
def get_slot_state(slot_id):
    """
    Route per ottenere lo stato di uno slot.
    """
    Slot = models.Slot.query.get(slot_id)
    return jsonify(Slot.get_state()) if Slot is not None else Response("not found", 404)