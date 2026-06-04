# Parallélisme Maximal — Bibliothèque d'ordonnancement automatique de tâches

Une bibliothèque Python qui calcule automatiquement le **parallélisme maximal** d'un système de tâches avec contraintes de précédence, en utilisant les **conditions de Bernstein** pour détecter et supprimer les dépendances inutiles.

Réalisé dans le cadre d'un projet de cours Systèmes d'exploitation & Concurrence.

---

## Présentation

À partir d'un ensemble de tâches avec accès mémoire en lecture/écriture et un ensemble de contraintes de précédence, cette bibliothèque :

1. **Valide** le système de tâches (noms uniques, dépendances valides, détection de cycle)
2. **Calcule le parallélisme maximal** en supprimant les précédences redondantes via les conditions de Bernstein
3. **Exécute les tâches** de façon séquentielle ou parallèle avec des threads Python
4. **Visualise** le graphe de précédence avec NetworkX et Matplotlib

---

## Conditions de Bernstein

Deux tâches `Ti` et `Tj` peuvent s'exécuter en parallèle si et seulement si elles n'ont **aucun conflit mémoire** :

- **RAW** (Read After Write) : `Ti.reads ∩ Tj.writes = ∅`
- **WAR** (Write After Read) : `Ti.writes ∩ Tj.reads = ∅`
- **WAW** (Write After Write) : `Ti.writes ∩ Tj.writes = ∅`

Si les trois conditions sont satisfaites, la contrainte de précédence entre `Ti` et `Tj` est inutile et peut être supprimée — augmentant ainsi le parallélisme.

---

## Structure du projet

```
maximal_parallelism/
├── maxpar.py      # Bibliothèque principale (Task, TaskSystem, validate, Bernstein)
└── test.py        # Exemples d'utilisation et cas de test
```

---

## Utilisation

```python
from maxpar import Task, TaskSystem

# Définition des tâches
T1 = Task()
T1.name = "T1"
T1.reads = ["x"]
T1.writes = ["y"]
T1.run = lambda: print("Exécution de T1")

T2 = Task()
T2.name = "T2"
T2.reads = ["y"]
T2.writes = ["z"]
T2.run = lambda: print("Exécution de T2")

# Définition des contraintes de précédence
precedence = {
    "T1": [],
    "T2": ["T1"]
}

# Création du système de tâches
systeme = TaskSystem([T1, T2], precedence)

# Calcul du parallélisme maximal
systeme.maxParallel()

# Exécution en parallèle
systeme.run()

# Visualisation du graphe de précédence
systeme.draw()
```

---

## Référence de l'API

### `Task`
| Attribut | Type | Description |
|----------|------|-------------|
| `name` | `str` | Identifiant unique de la tâche |
| `reads` | `list` | Variables mémoire lues par la tâche |
| `writes` | `list` | Variables mémoire écrites par la tâche |
| `run` | `callable` | Fonction à exécuter |

### `TaskSystem(tasks, precedence)`
| Méthode | Description |
|---------|-------------|
| `bernstein(Ti, Tj)` | Retourne `True` si Ti et Tj peuvent s'exécuter en parallèle |
| `maxParallel()` | Supprime les précédences redondantes, retourne le graphe optimisé |
| `runSeq()` | Exécute toutes les tâches séquentiellement en respectant la précédence |
| `run()` | Exécute les tâches en parallèle via des threads |
| `getDependencies(name)` | Retourne la liste des dépendances d'une tâche |
| `draw()` | Affiche le graphe de précédence |

### `validate(tasks, precedence)`
Vérifie :
- Les noms de tâches dupliqués
- Les références inconnues dans la précédence
- La détection de cycle par parcours topologique

---

## Technologies

- **Python 3** — Langage principal
- **threading** — Exécution parallèle
- **networkx** — Structure et analyse de graphes
- **matplotlib** — Visualisation du graphe de précédence

---

## Auteurs

- Hamou Djellab
- Chaouki Kassouri
- Anis Nait Kaci
