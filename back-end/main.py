from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from jsonschema import Draft202012Validator, ValidationError
import json
import uuid
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    id: str
    thread_id: str
    timestamp: str
    sender: str
    receiver: str
    text: str
    components: Optional[List[Dict[str, Any]]] = []
    extensions: Optional[Dict[str, Any]] = {}

with open("core_schema.json") as f:
    core_schema = json.load(f)

with open("reservation_schema.json") as f:
    reservation_schema = json.load(f)

reservation_validator = Draft202012Validator(reservation_schema["$def"]["reservation"])

session_states: Dict[str, Dict[str, Any]] = {}

def create_message(sender, receiver, text, thread_id, components=None, extensions=None):
    return Message(
        id=str(uuid.uuid4()),
        thread_id=thread_id,
        timestamp=datetime.utcnow().isoformat(),
        sender=sender,
        receiver=receiver,
        text=text,
        components=components or [],
        extensions=extensions or {}
    )

@app.get("/api/start")
def start_conversation():
    thread_id = str(uuid.uuid4())
    session_states[thread_id] = {"step": "ask_event_type", "reservation": {}}

    return create_message(
        sender="bot@localhost",
        receiver="frontend@localhost",
        text="Bonjour ! Souhaitez-vous réserver une salle pour un évènement ? 😊",
        thread_id=thread_id,
        components=[
            {
                "type": "binaryQuestion",
                "question": "Souhaitez-vous faire une réservation ?"
            }
        ]
    )

@app.post("/api/message")
def receive_message(message: Message) -> Message:
    thread_id = message.thread_id
    user_input = message.text.lower()

    if thread_id not in session_states:
        session_states[thread_id] = {"step": "ask_event_type", "reservation": {}}

    state = session_states[thread_id]

    if state["step"] == "ask_event_type" and user_input in ["oui", "yes"]:
        state["step"] = "waiting_for_event_type"
        return create_message(
            sender="bot@localhost",
            receiver=message.sender,
            text="Quel type d'événement voulez-vous réserver ?",
            thread_id=thread_id,
            components=[
                {
                    "type": "multiChoice",
                    "question": "Choisissez un type d'événement",
                    "choices": ["concert", "basket", "handball", "théâtre", "conférence"]
                }
            ]
        )

    elif state["step"] == "waiting_for_event_type" and user_input in ["concert", "basket", "handball", "théâtre", "conférence"]:
        state["reservation"]["event_type"] = user_input
        state["step"] = "waiting_for_date"
        return create_message(
            sender="bot@localhost",
            receiver=message.sender,
            text="Pour quelle date souhaitez-vous réserver la salle ? (format : AAAA-MM-JJ)",
            thread_id=thread_id
        )

    elif state["step"] == "waiting_for_date":
        try:
            datetime.strptime(user_input, "%Y-%m-%d")
            state["reservation"]["starting_date"] = user_input
            state["reservation"]["ending_date"] = user_input
            state["reservation"]["duration"] = "02:00:00"
            state["step"] = "confirm"

            return create_message(
                sender="bot@localhost",
                receiver=message.sender,
                text=f"Souhaitez-vous réserver pour le {user_input} pour un {state['reservation']['event_type']} ?",
                thread_id=thread_id,
                components=[
                    {
                        "type": "binaryQuestion",
                        "question": "Confirmez-vous cette réservation ?"
                    }
                ]
            )
        except ValueError:
            return create_message(
                sender="bot@localhost",
                receiver=message.sender,
                text="Le format de date n'est pas valide. Merci d'utiliser AAAA-MM-JJ",
                thread_id=thread_id
            )

    elif state["step"] == "confirm" and user_input in ["oui", "yes"]:
        reservation = {
            "reservationID": str(uuid.uuid4()),
            **state["reservation"],
            "hall": {
                "name": "Salle Polytech",
                "address": {
                    "street_address": "123 rue des Sciences",
                    "city": "Paris",
                    "state": "IDF",
                    "country": "France"
                }
            },
            "status": "pending"
        }

        try:
            reservation_validator.validate(reservation)
        except ValidationError as e:
            return create_message(
                sender="bot@localhost",
                receiver=message.sender,
                text=f"Erreur de validation : {e.message}",
                thread_id=thread_id
            )

        return create_message(
            sender="bot@localhost",
            receiver=message.sender,
            text="Merci, votre réservation a bien été enregistrée ✅",
            thread_id=thread_id,
            extensions={"reservation": reservation}
        )

    return create_message(
        sender="bot@localhost",
        receiver=message.sender,
        text="Je n'ai pas compris votre réponse. Pour recommencer, tapez 'réserver'.",
        thread_id=thread_id
    )
