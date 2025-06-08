# kernel_message_engine.py

import uuid
from datetime import datetime

# Mémoire temporaire : stockage par utilisateur ou thread_id
conversation_state = {}

def process_message(message: str) -> dict:
    sender = "bot@localhost"
    receiver = "frontend@localhost"
    thread_id = "demo-thread"
    now = datetime.utcnow().isoformat()

    # Récupérer l'état de la conversation
    state = conversation_state.get(thread_id, {})

    # Étape 1 : début de la réservation
    if "réserver" in message.lower():
        conversation_state[thread_id] = {"step": "ask_date"}
        return {
            "id": str(uuid.uuid4()),
            "thread_id": thread_id,
            "timestamp": now,
            "sender": sender,
            "receiver": receiver,
            "text": "Pour quand souhaitez-vous réserver ?",
            "components": [{"type": "binaryQuestion", "question": "Voulez-vous continuer ?"}],
            "extensions": {}
        }

    # Étape 2 : récupération de la date
    elif state.get("step") == "ask_date":
        state["date"] = message
        state["step"] = "ask_event"
        conversation_state[thread_id] = state
        return {
            "id": str(uuid.uuid4()),
            "thread_id": thread_id,
            "timestamp": now,
            "sender": sender,
            "receiver": receiver,
            "text": "Pour quel type d'événement souhaitez-vous réserver ?",
            "components": [],
            "extensions": {}
        }

    # Étape 3 : récupération de l’événement
    elif state.get("step") == "ask_event":
        state["event_name"] = message
        state["step"] = "complete"
        conversation_state[thread_id] = state
        return {
            "id": str(uuid.uuid4()),
            "thread_id": thread_id,
            "timestamp": now,
            "sender": sender,
            "receiver": receiver,
            "text": "Réservation enregistrée ✅",
            "components": [{
                "type": "reservation",
                "location": "Salle des fêtes",
                "date": state["date"],
                "event_name": state["event_name"],
                "nb_of_people": 1
            }],
            "extensions": {
                "reservation": {
                    "location": "Salle des fêtes",
                    "date": state["date"],
                    "event_name": state["event_name"],
                    "nb_of_people": 1
                }
            }
        }

    # Cas par défaut
    else:
        return {
            "id": str(uuid.uuid4()),
            "thread_id": thread_id,
            "timestamp": now,
            "sender": sender,
            "receiver": receiver,
            "text": "Je n’ai pas compris votre demande 😅",
            "components": [],
            "extensions": {}
        }
