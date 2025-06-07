# 📦 Extension de Schéma JSON : Réservation de Salle pour Événements

Ce répertoire contient un schéma JSON décrivant un système de **réservation de salle pour des événements**, tels que des concerts ou des matchs sportifs. Il inclut :

- le schéma `reservation.schema.json` en version 1.0.0
- un jeu de tests unitaires en Python (`tests_extended_schemes.py`)
- un exemple de données conforme au schéma (`data_valid.json`)

---

## 📁 Contenu du dossier

| Fichier                     | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `reservation.schema.json`  | Schéma JSON principal pour décrire une réservation d'événement.             |
| `tests_extended_schemes.py`| Tests Python utilisant `jsonschema` pour valider des exemples de données.   |
| `data_valid.json`          | Exemple de données **valide** selon le schéma, utile pour tests ou démo.    |

---

## ✅ Prérequis

Assurez-vous d'avoir Python 3 installé avec la bibliothèque `jsonschema` :

```bash
pip install jsonschema
```

## 🚀 Exécution des tests

Lancez les tests avec la commande suivante :

```bash
python tests_extended_schemes.py
```

Tous les tests doivent passer si le schéma est correct et les exemples bien formés.

## 📄 Exemple de données

Le fichier data_valid.json contient un exemple complet de réservation (type concert ou match) conforme au schéma défini.