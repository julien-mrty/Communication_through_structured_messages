# Structured Messaging – **Core Kernel**

> **Author :** David Kalala Kabambi  ·  2024‑25 project
> **File :** `kernel_message_engine.py`

---

## 1. What *is* this module?

A self‑contained **message engine** designed for a *local‐only* structured‑messaging client.

* Validates every message against a **common JSON Schema** (`core_schema.json`).
* Stores complete threads in **JSON files *or* SQLite** – no network layer.
* Supports **plug‑in extensions** so domain‑specific payloads (e.g. hall reservation) can ride along in the `extensions` field.

The engine is meant to be integrated with :

| Layer            | Owner    | Module             | Interaction                                   |
| ---------------- | -------- | ------------------ | --------------------------------------------- |
| **UI**           | Maëva    | `ui.py` or web app | calls `Thread.append()`, renders `components` |
| **Exchange Sim** | Matthieu | `exchange.py`      | uses registry to load extension schemas       |
| **Integration**  | Julien   | `main.py` / tests  | picks storage backend, wires everything       |

---

## 2. File & Folder layout

```
project/
├─ kernel_message_engine.py      # <– YOU ARE HERE
├─ core_schema.json              # auto‑dumped at first run
├─ storage/                      # *.json threads (when using JSONFileStorage)
├─ storage.sqlite3               # SQLite backend (if chosen)
└─ tests/                        # pytest specs (optional)
```

---

## 3. Key concepts

### 3.1 Core JSON Schema

* **Draft 2020‑12** document embedded in the Python file.
* Guarantees : `id`, `thread_id`, `timestamp`, `sender`, `receiver`, plus free‑text `text`.
* `components[]` – universal UI widgets (checkbox, binary question, multichoice, timeslot, color).
* `extensions{}` – arbitrary JSON blocks validated by **extra schemas** (loaded at runtime).

### 3.2 Data model classes

| Class                                                                            | Role                                                                                          |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `StructuredComponent`                                                            | Base class for every UI component. Serialises to dict.                                        |
| *Sub‑classes* : `Checkbox`, `BinaryQuestion`, `MultiChoice`, `TimeSlot`, `Color` | Concrete widgets – automatically **registered** through `ComponentRegistry.register`.         |
| `Message`                                                                        | One item in the conversation. Holds metadata, list of components and extensions.              |
| `Thread`                                                                         | Ordered list of `Message` objects between exactly 2 participants. Assigns common `thread_id`. |
| `ComponentRegistry`                                                              | Runtime map `type → Python class` (lets plugins inject new component types).                  |

### 3.3 Storage back‑ends

* **`JSONFileStorage(root_dir="storage")`** – one human‑readable file per thread.
* **`SQLiteStorage(db_file="storage.sqlite3")`** – relational alternative; good for search.

Both implement the simple interface :

```python
save_thread(thread)   # → None
load_thread(thread_id)  # → Thread | None
```

---

## 4. Quick start

### 4.1 Prerequisites

* Python ≥ 3.10
* `pip install jsonschema`  *(only if you plan to activate strict validation)*

### 4.2 Run the built‑in self‑test

```bash
python kernel_message_engine.py
# ✅  Basic round‑trip succeeded for JSON & SQLite back‑ends.
```

This script creates a mini conversation (`alice ↔ bob`) with a binary question, then saves/loads it through **both** storage systems.

### 4.3 Creating your own thread in 5 lines

```python
from kernel_message_engine import Thread, Message, BinaryQuestion, JSONFileStorage

a = "david@localhost"; b = "maeva@localhost"
t = Thread(participants=[a, b])
msg = Message(sender=a, receiver=b, text="Game tonight?", components=[BinaryQuestion(question="Have tickets?")])
t.append(msg)
JSONFileStorage().save_thread(t)
```

### 4.4 Loading it back

```python
store = JSONFileStorage()
thread = store.load_thread(t.id)
for m in thread.messages:
    print(m.timestamp, m.sender, "→", m.text)
```

---

## 5. Using extensions (plugins)

1. **Load the extra schema** :

   ```python
   import json, jsonschema, kernel_message_engine as kme
   hall_schema = json.load(open("reservation.schema.json"))
   kme.register_extension_schema("reservation", hall_schema)
   ```
2. **Attach payload** in the message :

   ```python
   msg.extensions["reservation"] = {...}
   ```
3. Engine validates automatically when you call `Message.to_dict()` if `strict=True`.

*(See `docs/reservation_example.py` for a full snippet.)*

---

## 6. Switching storage back‑ends

Choose once, inject everywhere :

```python
from kernel_message_engine import SQLiteStorage  # or JSONFileStorage
store = SQLiteStorage()
store.save_thread(thread)
```

> Both back‑ends can coexist; the integration script can decide per env var (`SM_STORAGE=sqlite`).

---

## 7. Running tests

```bash
pip install pytest
pytest tests/
```

A sample pytest file is provided; add more to cover your extensions.

---

## 8. Future work / TODO

* [ ] Encryption at rest (optional AES layer).
* [ ] Pagination helpers for large threads.
* [ ] Support for **multiple** participants per thread (stretch goal).

---

## 9. License

MIT (see `LICENSE`).

---

Happy hacking ! 🎉
