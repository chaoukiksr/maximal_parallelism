import threading
import networkx as nx
import matplotlib.pyplot as plt

class Task:
    def __init__(self):
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None

def validate(tasks, precedence):
    # Vérification 1 — noms uniques
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            if tasks[i].name == tasks[j].name:
                print(f"Erreur : nom dupliqué '{tasks[i].name}'")
                return

    # Vérification 2 - noms des précédences valides
    noms_valides = [task.name for task in tasks]
    for key, values in precedence.items():
        if key not in noms_valides:
            print(f"Erreur : tâche '{key}' inconnue dans le dictionnaire")
            return
        for value in values:
            if value not in noms_valides:
                print(f"Erreur : tâche '{value}' inconnue dans les dépendances de '{key}'")
                return

    # Vérification 3 - détection de cycle
    pCount = {}
    for task in tasks:
        pCount[task.name] = len(precedence[task.name])

    working = [name for name, count in pCount.items() if count == 0]
    waiting = [name for name, count in pCount.items() if count != 0]

    while working:
        task = working.pop(0)
        for tache in list(waiting):
            if task in precedence[tache]:
                pCount[tache] -= 1
                if pCount[tache] == 0:
                    waiting.remove(tache)
                    working.append(tache)

    if waiting:
        print(f"Erreur : cycle détecté entre les tâches {waiting}")
        return


class TaskSystem:
    def __init__(self, tasks, precedence):
        validate(tasks, precedence)
        self.tasks = tasks
        self.precedence = precedence

    def bernstein(self, Ti, Tj):
        RAW = set(Ti.reads) & set(Tj.writes)
        WAR = set(Ti.writes) & set(Tj.reads)
        WAW = set(Ti.writes) & set(Tj.writes)
        return not (RAW or WAR or WAW)

    def maxParallel(self):
        for p in self.precedence:
            Tj = self.getTask(p)
            for j in list(self.precedence[p]):
                Ti = self.getTask(j)
                if self.bernstein(Ti, Tj):
                    self.precedence[p].remove(j)
        return self.precedence

    def getTask(self, name):
        for task in self.tasks:
            if task.name == name:
                return task

    def getDependencies(self, nomTache):
        return self.precedence[nomTache]

    def runSeq(self):
        pCount = {}
        for task in self.tasks:
            pCount[task.name] = len(self.precedence[task.name])

        ready = [name for name, count in pCount.items() if count == 0]
        ordre = []

        while ready:
            name = ready.pop(0)
            ordre.append(name)
            for tache in self.tasks:
                if name in self.precedence[tache.name]:
                    pCount[tache.name] -= 1
                    if pCount[tache.name] == 0:
                        ready.append(tache.name)

        for name in ordre:
            task = self.getTask(name)
            task.run()

    def run(self):
        pCount = {}
        for task in self.tasks:
            pCount[task.name] = len(self.precedence[task.name])

        waiting = [name for name, count in pCount.items() if count != 0]
        ready = [name for name, count in pCount.items() if count == 0]

        while ready:
            threads = []
            for t in ready:
                task = self.getTask(t)
                thread = threading.Thread(target=task.run)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            next_ready = []
            for Tx in ready:
                for Ty in list(waiting):
                    if Tx in self.getDependencies(Ty):
                        pCount[Ty] -= 1
                        if pCount[Ty] == 0:
                            next_ready.append(Ty)
                            waiting.remove(Ty)
            ready = next_ready

    def draw(self):
        G = nx.DiGraph()
        for task in self.tasks:
            G.add_node(task.name)
        for a in self.precedence:
            for b in self.precedence[a]:
                G.add_edge(b, a)        # ← b précède a
        nx.draw(G, with_labels=True, node_color="lightblue",
                node_size=2000, arrows=True, arrowsize=20,font_size="small")
        plt.title("Graphe de précédence")
        plt.show()