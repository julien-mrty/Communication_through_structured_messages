# Assistant de Réservation de Salle – Chatbot FastAPI & React

Ce projet est une application web qui simule un **assistant conversationnel** capable de prendre des réservations de salle pour des événements comme des concerts, des matchs, etc.

💬 L’utilisateur interagit via une interface React.
🤖 Le backend FastAPI traite les messages, guide l’utilisateur étape par étape et valide les données grâce à un schéma JSON Schema.

---

## ⚙️ Installation

### 1. 📦 Backend (FastAPI)

#### ⬇️ Prérequis

* Python 3.9+
* `pip` installé

#### ▶️ Installation

```bash
# Clone du projet
git clone https://github.com/ton-compte/assistant-reservation.git
cd assistant-reservation/backend

# Installation des dépendances
pip install -r requirements.txt
```

#### ▶️ Lancer le serveur

```bash
uvicorn main:app --reload
```

L’API sera disponible sur `http://localhost:8000`.

---

### 2. 💻 Frontend (React)

#### ⬇️ Prérequis

* Node.js (18+ recommandé)
* `npm` ou `yarn`

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

## 🧠 Fonctionnalités du chatbot

Voici les étapes de la conversation typique :

1. L’utilisateur commence en répondant **"oui"** à la demande de réservation.
2. Le bot demande le **type d’événement** : `concert` ou `match`.
3. Selon le type :

   * 🎤 **Concert** : on demande le **nom du groupe ou de l'artiste**
   * ⚽ **Match** : on demande **deux équipes** (ex: `Lakers, Celtics`)
4. Le bot demande une **date** au format `AAAA-MM-JJ`
5. Il confirme les infos et propose un **bouton de confirmation**
6. Une fois validé, un objet `reservation` est généré et **validé avec un JSON Schema**

---

## 📦 Exemple de corps de réservation généré

```json
{
  "reservationID": "a3f89d63-...-d19945",
  "event_type": {
    "artists": [
      { "band_name": "Imagine Dragons" }
    ]
  },
  "starting_date": "2025-10-15",
  "ending_date": "2025-10-15",
  "duration": "02:00:00",
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
```

> Pour un **match**, `event_type` ressemblera à :

```json
"event_type": {
  "teams": [
    { "name": "Lakers", "sport": "basket" },
    { "name": "Warriors", "sport": "basket" }
  ]
}
```