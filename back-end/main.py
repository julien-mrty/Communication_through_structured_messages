from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from jsonschema import Draft202012Validator, ValidationError
from datetime import datetime
import uuid, json

app = FastAPI()

# CORS
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

with open("reservation_schema.json", encoding="utf-8") as f:
    reservation_schema = json.load(f)

validator = Draft202012Validator(reservation_schema)

session_states: Dict[str, Dict[str, Any]] = {}

def create_message(sender: str, receiver: str, text: str, thread_id: str,
                   components: Optional[List[Dict[str, Any]]] = None,
                   extensions: Optional[Dict[str, Any]] = None) -> Message:
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

@app.get("/api/start", response_model=Message)
def start_conversation():
    thread_id = str(uuid.uuid4())
    session_states[thread_id] = {"step": "ask_start", "reservation": {}}
    return create_message(
        sender="bot@localhost",
        receiver="frontend@localhost",
        text="Bonjour ! Voulez-vous réserver une salle ?",
        thread_id=thread_id,
        components=[{"type": "binaryQuestion", "question": "On démarre ?"}]
    )

@app.post("/api/message", response_model=Message)
def receive_message(message: Message) -> Message:
    thread_id = message.thread_id
    state = session_states.setdefault(thread_id, {"step": "ask_start", "reservation": {}})
    answer = message.text.strip().lower()

    if state["step"] == "ask_start" and answer in ("oui", "yes"):
        state["step"] = "ask_type"
        return create_message(
            sender="bot@localhost",
            receiver=message.sender,
            text="Quel type d’événement voulez-vous ?",
            thread_id=thread_id,
            components=[{
                "type": "multiChoice",
                "question": "Type d’événement",
                "choices": ["concert", "match", "conférence"]
            }]
        )

    if state["step"] == "ask_type" and answer in ("concert", "match", "conférence"):
        state["reservation"]["type_choice"] = answer
        if answer == "concert":
            state["step"] = "ask_artist"
            return create_message(
                sender="bot@localhost",
                receiver=message.sender,
                text="Quel est le nom de l’artiste ou du groupe ?",
                thread_id=thread_id
            )
        elif answer == "match":
            state["step"] = "ask_teams"
            return create_message(
                sender="bot@localhost",
                receiver=message.sender,
                text="Donnez au moins deux noms d’équipes, séparés par une virgule.",
                thread_id=thread_id
            )
        else:
            state["step"] = "ask_topic"
            return create_message(
                sender="bot@localhost",
                receiver=message.sender,
                text="Quel est le sujet de la conférence ?",
                thread_id=thread_id
            )

    if state["step"] == "ask_artist":
        artist_name = message.text.strip()
        state["reservation"]["event_type"] = {
            "artists": [{"band_name": artist_name}]
        }
        state["step"] = "ask_date"
        return create_message("bot@localhost", message.sender, "Pour quelle date ? (AAAA-MM-JJ)", thread_id)

    if state["step"] == "ask_teams":
        teams = [t.strip() for t in message.text.split(",") if t.strip()]
        if len(teams) < 2:
            return create_message("bot@localhost", message.sender, "Veuillez indiquer au moins deux équipes.", thread_id)
        state["reservation"]["event_type"] = {
            "teams": [{"name": team, "sport": "football"} for team in teams[:2]]
        }
        state["step"] = "ask_date"
        return create_message("bot@localhost", message.sender, "Pour quelle date ? (AAAA-MM-JJ)", thread_id)

    if state["step"] == "ask_topic":
        state["reservation"]["conf_topic"] = message.text.strip()
        state["step"] = "ask_speaker"
        return create_message("bot@localhost", message.sender, "Quel est le nom de l'intervenant principal ?", thread_id)

    if state["step"] == "ask_speaker":
        state["reservation"]["event_type"] = {
            "topic": state["reservation"].pop("conf_topic"),
            "speaker": message.text.strip(),
            "is_online": False
        }
        state["step"] = "ask_date"
        return create_message("bot@localhost", message.sender, "Pour quelle date ? (AAAA-MM-JJ)", thread_id)

    if state["step"] == "ask_date":
        try:
            datetime.strptime(answer, "%Y-%m-%d")
            state["reservation"].update({
                "starting_date": answer,
                "ending_date": answer,
                "duration": "02:00:00"
            })
            state["step"] = "ask_confirm"
            return create_message(
                sender="bot@localhost",
                receiver=message.sender,
                text=f"Confirmez-vous la réservation du {answer} ?",
                thread_id=thread_id,
                components=[{"type": "binaryQuestion", "question": "Oui / Non"}]
            )
        except ValueError:
            return create_message("bot@localhost", message.sender, "Format invalide. Utilisez AAAA-MM-JJ.", thread_id)

    if state["step"] == "ask_confirm" and answer in ("oui", "yes"):
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
                },
                "accessibility": [],
                "parking": False
            },
            "status": "pending"
        }

        try:
            validator.validate(reservation)
        except ValidationError as e:
            return create_message("bot@localhost", message.sender, f"Validation failed: {e.message}", thread_id)

        return create_message(
            sender="bot@localhost",
            receiver=message.sender,
            text="✅ Réservation enregistrée avec succès !",
            thread_id=thread_id,
            extensions={"reservation": reservation}
        )

    return create_message("bot@localhost", message.sender, "Désolé, je n’ai pas compris. Tapez \"oui\" pour recommencer.", thread_id)
