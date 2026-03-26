from maxpar import Task, TaskSystem

# Variables globales
stock = None
paiement = None
adresse = None
reservation = None
paiement_valide = None
livraison = None
commande = None
facture = None
colis = None
confirmation = None
expedition = None
tracking = None

# Fonctions
def runT1():
    global stock
    stock = "stock_ok"

def runT2():
    global paiement
    paiement = "paiement_ok"

def runT3():
    global adresse
    adresse = "adresse_ok"

def runT4():
    global reservation
    reservation = "stock_reserve"

def runT5():
    global paiement_valide
    paiement_valide = "paiement_valide"

def runT6():
    global livraison
    livraison = "livraison_calculee"

def runT7():
    global commande
    commande = "commande_confirmee"

def runT8():
    global facture
    facture = "facture_generee"

def runT9():
    global colis
    colis = "colis_prepare"

def runT10():
    global confirmation
    confirmation = "confirmation_envoyee"

def runT11():
    global expedition
    expedition = "colis_expedie"

def runT12():
    global tracking
    tracking = "tracking_envoye"

# Création des tâches
t1 = Task(); t1.name = "VerifStock";    t1.reads = [];                          t1.writes = ["stock"];           t1.run = runT1
t2 = Task(); t2.name = "VerifPaie";     t2.reads = [];                          t2.writes = ["paiement"];        t2.run = runT2
t3 = Task(); t3.name = "VerifAddr";     t3.reads = [];                          t3.writes = ["adresse"];         t3.run = runT3
t4 = Task(); t4.name = "ReservStock";   t4.reads = ["stock"];                   t4.writes = ["reservation"];     t4.run = runT4
t5 = Task(); t5.name = "ValidPaie";     t5.reads = ["paiement"];                t5.writes = ["paiement_valide"]; t5.run = runT5
t6 = Task(); t6.name = "CalcLivr";      t6.reads = ["adresse"];                 t6.writes = ["livraison"];       t6.run = runT6
t7 = Task(); t7.name = "ConfCommande";  t7.reads = ["reservation","paiement_valide"]; t7.writes = ["commande"]; t7.run = runT7
t8 = Task(); t8.name = "GenFacture";    t8.reads = ["paiement_valide"];         t8.writes = ["facture"];         t8.run = runT8
t9 = Task(); t9.name = "PrepColis";     t9.reads = ["reservation","commande"];  t9.writes = ["colis"];           t9.run = runT9
t10 = Task(); t10.name = "EnvConfirm";  t10.reads = ["commande","facture"];     t10.writes = ["confirmation"];   t10.run = runT10
t11 = Task(); t11.name = "Expedition";  t11.reads = ["colis","livraison"];      t11.writes = ["expedition"];     t11.run = runT11
t12 = Task(); t12.name = "Tracking";    t12.reads = ["expedition","confirmation"]; t12.writes = ["tracking"];   t12.run = runT12

# Système de tâches
tasks = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12]

precedence = {
    "VerifStock":   [],
    "VerifPaie":    [],
    "VerifAddr":    [],
    "ReservStock":  ["VerifStock"],
    "ValidPaie":    ["VerifPaie"],
    "CalcLivr":     ["VerifAddr"],
    "ConfCommande": ["ReservStock", "ValidPaie"],
    "GenFacture":   ["ValidPaie"],
    "PrepColis":    ["ReservStock", "ConfCommande"],
    "EnvConfirm":   ["ConfCommande", "GenFacture"],
    "Expedition":   ["PrepColis", "CalcLivr"],
    "Tracking":     ["Expedition", "EnvConfirm"]
}

s1 = TaskSystem(tasks, precedence)
s1.maxParallel()

print("=== getDependencies ConfCommande ===")
print(s1.getDependencies("ConfCommande"))

print("=== runSeq ===")
s1.runSeq()
print(f"stock={stock}, commande={commande}, tracking={tracking}")

print("=== draw ===")
s1.draw()
