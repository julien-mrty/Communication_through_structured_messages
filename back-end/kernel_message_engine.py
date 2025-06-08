"""
Structured Messaging – Core Kernel
===================================
Implementation for the kernel part of the "messagerie structurée" project.
Author: David Kalala Kabambi
Date: 2025‑03‑28


1. The common/core JSON Schema all structured messages must respect.
2. A light‑weight message/thread data‑model in Python.
3. A pluggable registry so that business‑specific extensions can hook into the engine at runtime.
4. Two storage back‑ends – JSON files & SQLite – to keep everything local‑only (no network layer).

"""
from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

# ────────────────────────────────────────────────────────────────────────────
# 1. JSON‑SCHEMA – CORE MESSAGE GRAMMAR
# ────────────────────────────────────────────────────────────────────────────
# The idea: every structured message exchanged by any client must validate
# against this schema. Extensions can enrich components or extensions but
# the metadata stay unchanged to guarantee baseline interoperability.
CORE_SCHEMA: Dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "urn:polytech:msg:core:1.0",
    "title": "Structured Message – Core 1.0",
    "description": "Common grammar for minimal interoperable messaging between two accounts.",
    "type": "object",
    "properties": {
        "id": {"type": "string", "format": "uuid"},
        "thread_id": {"type": "string", "format": "uuid"},
        "timestamp": {"type": "string", "format": "date-time"},
        "sender": {"type": "string"},
        "receiver": {"type": "string"},
        "text": {"type": "string"},
        "components": {
            "type": "array",
            "items": {"$ref": "#/$defs/component"},
            "default": [],
        },
        "extensions": {
            "type": "object",
            "description": "Heterogeneous payloads validated by extra schemas (plugins).",
            "default": {},
        },
    },
    "required": ["id", "thread_id", "timestamp", "sender", "receiver"],
    "$defs": {
        "component": {
            "oneOf": [
                {"$ref": "#/$defs/checkbox"},
                {"$ref": "#/$defs/binaryQuestion"},
                {"$ref": "#/$defs/multiChoice"},
                {"$ref": "#/$defs/timeSlot"},
                {"$ref": "#/$defs/color"},
            ]
        },
        "checkbox": {
            "type": "object",
            "properties": {
                "type": {"const": "checkbox"},
                "label": {"type": "string"},
                "checked": {"type": "boolean"},
            },
            "required": ["type", "label", "checked"],
        },
        "binaryQuestion": {
            "type": "object",
            "properties": {
                "type": {"const": "binaryQuestion"},
                "question": {"type": "string"},
                "answer": {"type": "boolean", "nullable": True},
            },
            "required": ["type", "question"],
        },
        "multiChoice": {
            "type": "object",
            "properties": {
                "type": {"const": "multiChoice"},
                "question": {"type": "string"},
                "choices": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "selected": {
                    "type": "string",
                    "nullable": True,
                },
            },
            "required": ["type", "question", "choices"],
        },
        "timeSlot": {
            "type": "object",
            "properties": {
                "type": {"const": "timeSlot"},
                "start": {"type": "string", "format": "date-time"},
                "end": {"type": "string", "format": "date-time"},
            },
            "required": ["type", "start", "end"],
        },
        "color": {
            "type": "object",
            "properties": {
                "type": {"const": "color"},
                "hex": {"type": "string", "pattern": "^#?[0-9a-fA-F]{6}$"},
            },
            "required": ["type", "hex"],
        },
    },
}

# Optional: dump a pretty JSON file of the core schema so that the rest of the
# team (Maëva, Matthieu…) can validate / generate UI components.
SCHEMA_FILE = Path(__file__).with_name("core_schema.json")
if not SCHEMA_FILE.exists():
    SCHEMA_FILE.write_text(json.dumps(CORE_SCHEMA, indent=2))

# ────────────────────────────────────────────────────────────────────────────
# 2. DATA‑MODEL – PYTHONIC VIEW OF A MESSAGE THREAD
# ────────────────────────────────────────────────────────────────────────────


@dataclass
class StructuredComponent:
    """Base class – each concrete component registers itself via ComponentRegistry."""

    TYPE: str = "component"  # overridden by subclasses

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["type"] = self.TYPE
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StructuredComponent":
        comp_type = data.get("type")
        component_cls = ComponentRegistry.get(comp_type)
        if component_cls is None:
            raise ValueError(f"Unsupported component type: {comp_type}")
        # Remove the discriminator before unpacking
        data = {k: v for k, v in data.items() if k != "type"}
        return component_cls(**data)  # type: ignore[arg-type]


class ComponentRegistry:
    """Runtime registry so that plugins can inject new component types."""

    _REGISTRY: Dict[str, Type[StructuredComponent]] = {}

    @classmethod
    def register(cls, component_cls: Type[StructuredComponent]) -> Type[StructuredComponent]:
        cls._REGISTRY[component_cls.TYPE] = component_cls
        return component_cls

    @classmethod
    def get(cls, comp_type: str) -> Optional[Type[StructuredComponent]]:
        return cls._REGISTRY.get(comp_type)


# ── Concrete built‑in components ──────────────────────────────────────────


@ComponentRegistry.register
@dataclass
class Checkbox(StructuredComponent):
    TYPE: str = "checkbox"
    label: str = ""
    checked: bool = False


@ComponentRegistry.register
@dataclass
class BinaryQuestion(StructuredComponent):
    TYPE: str = "binaryQuestion"
    question: str = ""
    answer: Optional[bool] = None


@ComponentRegistry.register
@dataclass
class MultiChoice(StructuredComponent):
    TYPE: str = "multiChoice"
    question: str = ""
    choices: List[str] = field(default_factory=list)
    selected: Optional[str] = None


@ComponentRegistry.register
@dataclass
class TimeSlot(StructuredComponent):
    TYPE: str = "timeSlot"
    start: datetime = datetime.utcnow()
    end: datetime = datetime.utcnow()


@ComponentRegistry.register
@dataclass
class Color(StructuredComponent):
    TYPE: str = "color"
    hex: str = "#ffffff"


# ────────────────────────────────────────────────────────────────────────────
# 3. MESSAGE + THREAD – DOMAIN ENTITIES
# ────────────────────────────────────────────────────────────────────────────


@dataclass
class Message:
    sender: str
    receiver: str
    text: str = ""
    components: List[StructuredComponent] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    thread_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # Serialization helpers ------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "receiver": self.receiver,
            "text": self.text,
            "components": [c.to_dict() for c in self.components],
            "extensions": self.extensions,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        comps = [StructuredComponent.from_dict(d) for d in data.get("components", [])]
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            text=data.get("text", ""),
            components=comps,
            extensions=data.get("extensions", {}),
            id=data["id"],
            thread_id=data.get("thread_id", ""),
            timestamp=data.get("timestamp", datetime.utcnow().isoformat()),
        )


@dataclass
class Thread:
    """Represents an ordered list of messages between two participants."""

    participants: List[str]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[Message] = field(default_factory=list)

    def append(self, message: Message) -> None:
        if set([message.sender, message.receiver]) != set(self.participants):
            raise ValueError("Message participants do not match thread participants")
        message.thread_id = self.id  # keep things in sync
        self.messages.append(message)

    # Quick dump helpers ---------------------------------------------------
    def to_json(self) -> str:
        return json.dumps([m.to_dict() for m in self.messages], indent=2)

    @classmethod
    def from_json(cls, json_str: str, participants: List[str]) -> "Thread":
        data = json.loads(json_str)
        thread = cls(participants=participants)
        for m in data:
            thread.append(Message.from_dict(m))
        return thread


# ────────────────────────────────────────────────────────────────────────────
# 4. STORAGE LAYERS – KEEPING EVERYTHING LOCAL
# ────────────────────────────────────────────────────────────────────────────


class StorageBackend:
    def save_thread(self, thread: Thread) -> None:  # pragma: no cover
        raise NotImplementedError

    def load_thread(self, thread_id: str) -> Optional[Thread]:  # pragma: no cover
        raise NotImplementedError


class JSONFileStorage(StorageBackend):
    """Stores every thread in its own .json file under a given directory."""

    def __init__(self, root_dir: Path | str = "storage") -> None:
        self.root = Path(root_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def _file_for(self, thread_id: str) -> Path:
        return self.root / f"{thread_id}.json"

    def save_thread(self, thread: Thread) -> None:
        self._file_for(thread.id).write_text(thread.to_json())

    def load_thread(self, thread_id: str) -> Optional[Thread]:
        path = self._file_for(thread_id)
        if not path.exists():
            return None
        participants = json.loads(path.read_text())[0]["sender"], json.loads(path.read_text())[0]["receiver"]
        return Thread.from_json(path.read_text(), list(participants))


class SQLiteStorage(StorageBackend):
    """Relational alternative using the built‑in sqlite3 module – still 100% local."""

    def __init__(self, db_file: str = "storage.sqlite3") -> None:
        self.conn = sqlite3.connect(db_file)
        self._prepare()

    def _prepare(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS threads(
                id TEXT PRIMARY KEY,
                participants TEXT
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages(
                id TEXT PRIMARY KEY,
                thread_id TEXT,
                payload TEXT,
                FOREIGN KEY(thread_id) REFERENCES threads(id)
            );
            """
        )
        self.conn.commit()

    # ------------------------------
    def save_thread(self, thread: Thread) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO threads(id, participants) VALUES(?, ?)",
            (thread.id, json.dumps(thread.participants)),
        )
        for msg in thread.messages:
            cur.execute(
                "INSERT OR REPLACE INTO messages(id, thread_id, payload) VALUES(?, ?, ?)",
                (msg.id, thread.id, json.dumps(msg.to_dict())),
            )
        self.conn.commit()

    def load_thread(self, thread_id: str) -> Optional[Thread]:
        cur = self.conn.cursor()
        cur.execute("SELECT participants FROM threads WHERE id=?", (thread_id,))
        row = cur.fetchone()
        if not row:
            return None
        participants = json.loads(row[0])
        cur.execute("SELECT payload FROM messages WHERE thread_id=? ORDER BY ROWID", (thread_id,))
        msgs = [Message.from_dict(json.loads(r[0])) for r in cur.fetchall()]
        return Thread(id=thread_id, participants=participants, messages=msgs)


# ────────────────────────────────────────────────────────────────────────────
# 5. QUICK SELF‑TEST – run `python kernel_message_engine.py` directly
# (makes debugging easier before the integration phase led by Julien).
# ────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    alice, bob = "alice@localhost", "bob@localhost"
    thread = Thread(participants=[alice, bob])

    # message 1 – simple binary question
    msg1 = Message(sender=alice, receiver=bob, text="Hey, game tonight?")
    msg1.components.append(BinaryQuestion(question="Do you have tickets?"))
    thread.append(msg1)

    # message 2 – Bob answers
    msg2 = Message(sender=bob, receiver=alice, text="Nope, still looking.")
    thread.append(msg2)

    # Store to JSON & SQLite just to prove both work
    json_store = JSONFileStorage()
    json_store.save_thread(thread)
    restored = json_store.load_thread(thread.id)
    assert restored and len(restored.messages) == 2

    sql_store = SQLiteStorage()
    sql_store.save_thread(thread)

    print("✅  Basic round‑trip succeeded for JSON & SQLite back‑ends.")


def process_message(user_message: str) -> dict:
    """Traitement d’un message utilisateur simple pour l’API FastAPI"""

    sender = "frontend@localhost"
    receiver = "bot@localhost"

    # Charger ou créer une nouvelle conversation
    store = JSONFileStorage()
    threads = list(store.root.glob("*.json"))

    if threads:
        thread = store.load_thread(threads[0].stem)
    else:
        thread = Thread(participants=[sender, receiver])

    # Ajouter le message utilisateur
    msg_in = Message(sender=sender, receiver=receiver, text=user_message)
    thread.append(msg_in)

    # Générer une réponse automatique
    msg_out = Message(sender=receiver, receiver=sender, text="Message reçu 👌")
    msg_out.components.append(BinaryQuestion(question="Voulez-vous continuer ?", answer=None))
    thread.append(msg_out)

    # Sauvegarder
    store.save_thread(thread)

    return msg_out.to_dict()
