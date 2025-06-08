# Assistant de Réservation de Salle – Chatbot FastAPI & React

Ce projet est une application web qui simule un **assistant conversationnel** capable de prendre des réservations de salle pour des événements comme des concerts, des matchs, conférences. Il s'agit d'un moteur de messagerie fonctionnant uniquement en local.

💬 L’utilisateur interagit via une interface React.
🤖 Le backend FastAPI traite les messages, guide l’utilisateur étape par étape et valide les données grâce à un schéma JSON Schema noyau et d'extension.
🧩 Schéma d'extension pour gérer des cas métiers comme la réservation  

---

# 🗂️ Organisation du projet

```
project/
├─ backend/
│  ├─ main.py                    # API FastAPI & logique métier
│  ├─ kernel_message_engine.py   # Moteur de messages structuré
│  ├─ core_schema.json           # Schéma de base (auto-généré)
│  ├─ reservation_schema.json    # Schéma d'extension : réservation
│  ├─ test_valid_data.py         # Test sur fichier de données valides
│  ├─ tests_extended_schemes.py  # Test des extensions JSON Schema
│  └─ storage/                   # Fichiers de threads au format JSON
├─ frontend/
│  └─ src/                       # Composants React + hooks + types
├─ readme.md
└─ video_example.mov             # 🎥 Démo vidéo du chatbot
```

# Répartition des tâches

| Layer            | Owner    | Module             | Interaction                                   |
| ---------------- | -------- | ------------------ | --------------------------------------------- |
| **UI**           | Maëva    | front-end | Intégration d'une interface web |
| **Simulation d'échanges** | Matthieu | `exchange.py`      | charge le schéma d'extension       |
| **Integration**  | Julien   | `main.py` / tests  | Orchestre les modules et gère le stockage       |
| **Schéma noyau**  | David   | `core_schema.json` / tests  | conception du schéma noyau       |
| **Schéma d'extension**  | Julie   | `reservation_schema.json` / tests  | conception du schéma d'extension associé au sujet       |

## ⚙️ Installation

### 1. 🔧 Backend – FastAPI

#### ⬇️ Prérequis

* Python 3.9+
* `pip` installé
* `pip install jsonschema`  *(pour vérifier les schémas avec les tests fournis)*

#### ▶️ Installation

```bash
# Cloner le dépot du projet
git clone https://github.com/ton-compte/assistant-reservation.git
cd assistant-reservation/backend


#### ▶️ Lancer le serveur

```bash
uvicorn main:app --reload
```

L’API sera disponible sur `http://localhost:8000`.


#### 🧪 Lancer les tests

Test du schéma noyau :

```bash
python kernel_message_engine.py
```
Ce script crée une mini conversation (alice ↔ bob) avec une question binaire, puis la sauvegarde/charge via les deux systèmes de stockage.

Validation du schéma d'extension :

```bash
python tests_extended_schemes.py
python test_valid_data.py
```
Ces scripts testent le schéma d'extension en l'instanciant. Cela nous a permis de mettre en évidence des bugs notamment sur les champs requis. 
Tous les tests doivent passer si le schéma est correct et les exemples bien formés.

---

### 2. 💻 Frontend (React)

#### ⬇️ Prérequis

* Node.js (18+ recommandé)
* `npm`

#### ▶️ Installation

```bash
cd ../frontend
npm install
```

#### ▶️ Lancer le frontend

```bash
npm run dev
```

L’interface sera disponible sur `http://localhost:5173`.

---

# 🧠 Fonctionnement du chatbot

Voici les étapes de la conversation typique :

1. L’utilisateur commence en répondant **"oui"** à la demande de réservation.
2. Le bot demande le **type d’événement** : `concert`, `match` ou `conference`.
3. Selon le type :

   * 🎤 **Concert** : on demande le **nom du groupe ou de l'artiste**
   * ⚽ **Match** : on demande **deux équipes** (ex: `Lakers, Celtics`)
   * 🎙️ **Conférence** : on demande le **nom de l’intervenant ou du sujet**
4. Le bot demande une **date** au format `AAAA-MM-JJ`
5. Il confirme les infos et propose un **bouton de confirmation**
6. Une fois validé, un objet `reservation` est généré et **validé avec un JSON Schema**


# 🧩 Description du moteur de messages

* ✔️ Validation de chaque message via un **schéma JSON commun** (`core_schema.json`).
* 📁 Stockage local sous forme de **fichiers JSON** (par thread).
* 🔌 Prend en charge des **extensions plug‑in** dans le champ `extensions{}`.

# 📐 Les Schéma JSON
## 📦Schéma JSON central (noyau)

* Schéma conforme au standard **Draft 2020‑12**.
* Champs garantis : `id`, `thread_id`, `timestamp`, `sender`, `receiver`, et un champ texte libre `text`.
* `components[]` – composants UI universels (case à cocher, question binaire, choix multiple, créneau horaire, couleur).
* `extensions{}` – blocs JSON personnalisés, validés à l’exécution par des **schéma d'extensions**.

### 🧱 Modèles de données

| Classe                                                                            | Rôle                                                                                              |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `StructuredComponent`                                                             | Classe de base pour tous les composants UI. Se convertit en dictionnaire.                         |
| *Sous‑classes* : `Checkbox`, `BinaryQuestion`, `MultiChoice`, `TimeSlot`, `Color` | Widgets concrets, automatiquement **enregistrés** via `ComponentRegistry.register`.               |
| `Message`                                                                         | Un message structuré dans une conversation, avec métadonnées, composants et extensions.           |
| `Thread`                                                                          | Liste ordonnée de messages entre deux participants, partageant un `thread_id` commun.             |
| `ComponentRegistry`                                                               | Registre dynamique `type → classe Python` (permet d’ajouter des types de composants via plugins). |

## 📦 Module : Réservation de salle (schéma d’extension)

Ce répertoire contient un schéma JSON décrivant un système de **réservation de salle pour des événements**, tels que des concerts, des matchs sportifs ou des conférences. Il inclut :

- le schéma `reservation.schema.json` en version 1.0.0
- un jeu de tests unitaires en Python (`tests_extended_schemes.py`, `test_valid_data.py` )
- un exemple de données conforme au schéma (`data_valid.json`)

### 📄 Exemple de données

Le fichier data_valid.json contient un exemple complet de réservation (type concert, match ou conférence) conforme au schéma défini.


## 🧩 Utiliser une extension (plugin)

1. **Charger un schéma supplémentaire :**

   ```python
   import json, jsonschema, kernel_message_engine as kme
   hall_schema = json.load(open("reservation.schema.json"))
   kme.register_extension_schema("reservation", hall_schema)
   ```
2. **Ajouter une extension à un message :**

   ```python
   msg.extensions["reservation"] = {...}
   ```
3. Le moteur valide automatiquement l’extension lors de l’appel à `Message.to_dict()` si `strict=True`.


# 🔌Utilisation des threads

## ✍️ Exemple – Créer un thread en 5 lignes

```python
from kernel_message_engine import Thread, Message, BinaryQuestion, JSONFileStorage

a = "david@localhost"; b = "maeva@localhost"
t = Thread(participants=[a, b])
msg = Message(sender=a, receiver=b, text="Game tonight?", components=[BinaryQuestion(question="Have tickets?")])
t.append(msg)
JSONFileStorage().save_thread(t)
```

## 🔁 Exemple – Recharger un thread

```python
store = JSONFileStorage()
thread = store.load_thread(t.id)
for m in thread.messages:
    print(m.timestamp, m.sender, "→", m.text)
```

## 💾 Système de stockage – JSON uniquement

* **`JSONFileStorage(root_dir="storage")`** – Chaque conversation est enregistrée dans un fichier lisible et structuré.

API simple :

```python
save_thread(thread)   # → None
load_thread(thread_id)  # → Thread | None
```


