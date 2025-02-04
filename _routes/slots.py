from datetime import datetime
from flask import Blueprint, jsonify, request, Response
from _utils import models, decorators, slot


slots = Blueprint('slots', __name__, url_prefix="/slots")


"""
Route usate per gestire gli slots e le sessioni di parcheggio.
"""

@slots.route("/", methods=["GET"])
def get_slots():
    """
    Route per ottenere tutti gli slots.
    """
    Slot = slot.get_slots()
    return jsonify([s.serialize() for s in Slot])



@slots.route("/slot/<parking_id>", methods=["GET"])
def get_slot(parking_id):
    """
    Route per ottenere un singolo slot.
    """
    Slot = slot.get_slot(parking_id)
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



@slots.route("/delete_slot/<parking_id>", methods=["DELETE"])
@decorators.admin_decorator
def delete_slot(parking_id):
    """
    Route per eliminare uno slot.
    """
    try:
        slot.delete_slot(parking_id)
        return Response("OK", status=200)
    except slot.NotFoundError:
        return Response("not found", 404)



@slots.route("/get_slots_by_zone/<zone>", methods=["GET"])
def get_slots_by_zone(zone):
    """
    Route per ottenere tutti gli slots di una determinata zona.
    """
    try:
        Slots = slot.get_slots_by_zone(zone)
        return jsonify([s.serialize() for s in Slots])
    except slot.NotFoundError:
        return Response("not found", 404)



@slots.route("/start_parking_session/<parking_id>", methods=["POST"])
@decorators.auth_decorator
def start_parking_session(user_id, parking_id):
    """
    Route per iniziare una sessione di parcheggio.
    """
    Slot = slot.get_slot(parking_id)
    if Slot is None:
        return Response("not found", 404)
    if Slot.state is False:
        return Response("Non puoi iniziare una sessione di parcheggio prima di esserti parcheggiato", 401)
    start_time = int(datetime.now().timestamp())
    slot.start_parking_session(user_id, parking_id, start_time)
    models.db.session.commit()
    return "OK, Sessione di parcheggio iniziata per l'utente con id {} nello slot {}".format(user_id, parking_id)



@slots.route("/update_slot_state/<parking_id>", methods=["POST"])
@decorators.admin_decorator
def update_slot(parking_id):
    """
    Route per aggiornare lo stato dello slot.
    """
    #print("L'utente {} ha cambiato lo stato dello slot {}".format(user_id, parking_id))
    Slot = slot.get_slot(parking_id)
    if Slot is None:
        return Response("not found", 404)
    if Slot.state is False: #significa che l'utente si è parcheggiato quindi bisogna anche far partire il timer per il pagamento
        #print("L'utente {} si è parcheggiato nello slot {}".format(user_id, parking_id))
        Slot.state = not Slot.state
        models.db.session.commit()
        return "OK, Nello slot {} qualcuno si è parcheggiato".format(parking_id)
    elif Slot.state is True: #significa che l'utente sta lasciando lo slot quindi bisogna fermare il timer
        #print("L'utente {} sta lasciando lo slot {}".format(user_id, parking_id))
        ParkingSession = slot.get_last_parking_session_not_finished(parking_id)
        if ParkingSession is None:
            Slot.state = not Slot.state
            models.db.session.commit()
            return "OK, Nello slot {} qualcuno sta lasciando lo slot ma non c'è nessuna sessione di parcheggio".format(parking_id)
        else:
            Slot.state = not Slot.state
            end_time = int(datetime.now().timestamp())
            ParkingSession.end_time = end_time
            ParkingSession.finished = True
            if end_time - ParkingSession.start_time < 60:      #lasciamo 60 per ora ma quando deployeremo sarà 900 (15 minuti)
                #Il tempo trascorso è minore di 60 secondi, non verrà effettuato alcun pagamento
                ParkingSession.amount = 0
            else:
                ParkingSession.amount = (end_time - ParkingSession.start_time) // 60 * 0.5
            models.db.session.commit()
            return "OK, Nello slot {} l'utente con id {} ha lasciato il parcheggio ed ha finito la sessione di parcheggio con {} secondi".format(parking_id, ParkingSession.user_id, end_time - ParkingSession.start_time)



@slots.route("/get_all_slot_states/", methods=["GET"])
@decorators.admin_decorator
def get_all_slot_states():
    """
    Author: Federico Melis
    Route per ottenere lo stato di tutti gli slot.
    """
    Slot = slot.get_slots()
    return jsonify({s.parking_id: s.state for s in Slot})



@slots.route("/get_slot_state/<parking_id>", methods=["GET"])
def get_slot_state(parking_id):
    """
    Route per ottenere lo stato di uno slot.
    """
    Slot = slot.get_slot(parking_id)
    return jsonify(Slot.state) if Slot is not None else Response("not found", 404)



#dobbiamo capire se serve avere il middleware per fare il controllo dell'admin per questa route
@slots.route("/get_parking_sessions/", methods=["GET"])
def get_parking_sessions():
    """
    Route per ottenere tutte le sessioni di parcheggio.
    """
    ParkingSession = slot.get_parking_sessions()
    return jsonify([p.serialize() for p in ParkingSession])



@slots.route("/get_last_parking_session/", methods=["GET"])
@decorators.auth_decorator
def get_last_parking_session(user_id):
    """
    Route per ottenere l'ultima sessione di parcheggio dell'utente.
    """
    ParkingSession = slot.get_last_parking_session(user_id)
    return jsonify(ParkingSession.serialize()) if ParkingSession is not None else Response("not found", 404)



@slots.route("/get_user_parking_sessions/", methods=["GET"])
@decorators.auth_decorator
def get_user_parking_sessions(user_id):
    """
    Route per ottenere tutte le sessioni di parcheggio dell'utente.
    """
    ParkingSession = slot.get_user_parking_sessions(user_id)
    return jsonify([p.serialize() for p in ParkingSession]) if ParkingSession is not None else Response("not found", 404)


@slots.route("/update_only_state/", methods=["POST"])
@decorators.admin_decorator
def update_only_state():
    """
    Route per aggiornare solo lo stato dello slot.
    """
    parking_id = request.form['parking_id']
    Slot = slot.get_slot(parking_id)
    if Slot is None:
        return Response("not found", 404)
    State = request.form['state']
    if State == "1":
        Slot.state = True
    elif State == "0":
        Slot.state = False
    models.db.session.commit()
    return "OK, Lo stato dello slot {} è stato aggiornato".format(parking_id)



@slots.route("/update_parking_history/", methods=["POST"])
@decorators.admin_decorator
def update_parking_history():
    """
    Route per aggiornare la cronologia del parcheggio.
    """
    SlotsState = slot.get_slots_state()
    print("DEBUG: lunghezza SlotsState")
    print(len(SlotsState))
    size = slot.get_history_size(1)
    if size < 3600:
        timestamp = int(datetime.now().timestamp())
        for parking_id, state in SlotsState.items():
            slot.update_parking_history(parking_id, state, timestamp)
        return "OK, Cronologia del parcheggio aggiornata"
    elif size >= 3600:
        slot.remove_oldest_parking_history()
        print("Rimossa la history più vecchia")
        timestamp = int(datetime.now().timestamp())
        for parking_id, state in SlotsState.items():
            slot.update_parking_history(parking_id, state, timestamp)
        return "OK, Cronologia del parcheggio aggiornata"


@slots.route("/update_parking_history/<parking_id>/", methods=["POST"])
@decorators.admin_decorator
def update_parking_history_slot(parking_id):
    """
    Route per aggiornare la cronologia del parcheggio di uno slot.
    Si prende lo stato e il ts dal body della richiesta ma in formato json.
    """
    data = request.get_json()
    if data is None:
        return Response("bad request", 400)
    
    for ts, state in data.items():
        slot.update_parking_history(parking_id, state, ts)

    return "OK, Cronologia del parcheggio aggiornata per lo slot {}".format(parking_id)
    
    