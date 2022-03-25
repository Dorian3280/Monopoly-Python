import random


CARDS = {
    "chest": [
        {
            "text": ["Advance to Go (Collect £200)", "Placez vous sur le case Depart"],
            "cast": lambda x: x.moveByCard(0),
        },
        {
            "text": [
                "Bank error in your favor. Collect £200",
                "Erreur de la Banque en votre faveur. Recevez 200€",
            ],
            "cast": lambda x: x.transaction(200),
        },
        {
            "text": ["Doctor's fee. Pay £50", "Payez la note du Medecin €50"],
            "cast": lambda x: x.transaction(-50),
        },
        {
            "text": [
                "From sale of stock you get £50",
                "La vente de stock vous rapporte €50",
            ],
            "cast": lambda x: x.transaction(-50),
        },
        {
            "text": [
                "Get Out of Jail Free. This card may be kept until needed or sold/traded",
                "Vous etes libere de prison. Cette carte peut être conservee jusqu'a ce qu'elle soit utilisee ou vendue",
            ],
            "cast": lambda x: x.getFreeJailCard(),
        },
        {
            "text": [
                "Go to Jail. Go directly to jail. Do not pass Go, Do not collect £200",
                "Allez en prison. Rendez vous directement a la prison. Ne franchissez pas la case Depart. Ne touchez pas 200€",
            ],
            "cast": lambda x: x.moveToJail(),
        },
        {
            "text": [
                "Holiday fund matures. Receive £100",
                "Le fond de vacances arrive a echeance. Recevez 100€",
            ],
            "cast": lambda x: x.transaction(100),
        },
        {
            "text": [
                "Income tax refund. Collect £20",
                "Les Contributions vous remboursent la somme de 20€",
            ],
            "cast": lambda x: x.transaction(20),
        },
        {
            "text": [
                "It is your birthday. Collect £10 from every player",
                "C'est votre anniversaire: chaque joueur vous doit 10€",
            ],
            "cast": lambda x: x.birthday(),
        },
        {
            "text": [
                "Life insurance matures. Collect £100",
                "Recevez votre revenu annuel 100€",
            ],
            "cast": lambda x: x.transaction(100),
        },
        {
            "text": ["Pay hospital fees of £100", "Payer a l'Hôpital 100€"],
            "cast": lambda x: x.transaction(-100),
        },
        {
            "text": [
                "Pay school fees of £50",
                "Payez les frais de scolarite s'elevant a 50€",
            ],
            "cast": lambda x: x.transaction(-50),
        },
        {
            "text": [
                "Receive £25 consultancy fee",
                "Recevez votre interêt sur l'emprunt a 7%. 25€",
            ],
            "cast": lambda x: x.transaction(25),
        },
        {
            "text": [
                "You are assessed for street repairs. £40 per house. £115 per hotel",
                "Faites des reparations dans toutes vos maisons. Versez pour chaque maison 25€. Versez pour chaque hôtel 100€",
            ],
            "cast": lambda x: x.transaction(-x.costFromRepairsPlus()),
        },
        {
            "text": [
                "You have won second prize in a beauty contest. Collect £10",
                "Vous avez gagne le deuxieme Prix de Beaute. Recevez 10€",
            ],
            "cast": lambda x: x.transaction(10),
        },
        {
            "text": ["You inherit £100", "Vous heritez 100€"],
            "cast": lambda x: x.transaction(100),
        },
    ],
    "chance": [
        {
            "text": ["Advance to Go (Collect £200)", "Placez vous sur le case Depart"],
            "cast": lambda x: x.moveByCard(0),
        },
        {
            "text": [
                "Advance to Trafalgar Square. If you pass Go, collect £200",
                "Rendez vous a l'Avenue Henri Martin. Si vous passez par la case Depart recevez 200€",
            ],
            "cast": lambda x: x.moveByCard(24),
        },
        {
            "text": ["Advance to Mayfair", "Rendez-vous a la Rue de la Paix"],
            "cast": lambda x: x.moveByCard(39),
        },
        {
            "text": [
                "Advance to Pall Mall. If you pass Go, collect £200",
                "Avancez au Boulevard de la Villette. Si vous passez par la case Depart recevez 200€",
            ],
            "cast": lambda x: x.moveByCard(11),
        },
        {
            "text": [
                "Advance to the nearest Station. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled",
                "Avancez jusqu'a la station la plus proche. Si elle n'appartient a personne, vous devez l'acheter, sinon vous payez 2 fois le montant du loyer au proprietaire",
            ],
            "cast": lambda x: x.moveToNearest("railroad"),
        },
        {
            "text": [
                "Advance to the nearest Station. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled",
                "Avancez jusqu'a la station la plus proche. Si elle n'appartient a personne, vous devez l'acheter, sinon vous payez 2 fois le montant du loyer au proprietaire",
            ],
            "cast": lambda x: x.moveToNearest("railroad"),
        },
        {
            "text": [
                "Advance to the nearest Utility. If unowned, you may buy it from the Bank. If owned, pay wonder twice the rental to which they are otherwise entitled",
                "Avancez jusqu'a la compagnie la plus proche. Si elle n'appartient a personne, vous devez l'acheter, sinon vous payez 2 fois le montant du loyer au proprietaire",
            ],
            "cast": lambda x: x.moveToNearest("utility"),
        },
        {
            "text": [
                "Bank pays you dividend of £50",
                "La Banque vous verse un dividende de 50€",
            ],
            "cast": lambda x: x.transaction(50),
        },
        {
            "text": [
                "Get Out of Jail Free. This card may be kept until needed or sold/traded",
                "Vous etes libere de prison. Cette carte peut être conservee jusqu'a ce qu'elle soit utilisee ou vendue",
            ],
            "cast": lambda x: x.getFreeJailCard(),
        },
        {
            "text": ["Go Back 3 Spaces", "Reculez de 3 cases"],
            "cast": lambda x: x.moveByCard(-3, moveBackward=True),
        },
        {
            "text": [
                "Go to Jail. Go directly to jail. Do not pass Go, Do not collect £200",
                "Allez en prison. Rendez vous directement a la prison. Ne franchissez pas la case Depart. Ne touchez pas 200€",
            ],
            "cast": lambda x: x.moveToJail(),
        },
        {
            "text": [
                "Make general repairs on all your property. For each house pay £25. For each hotel pay £100",
                "Faites des reparations dans toutes vos maisons. Versez pour chaque maison 25€. Versez pour chaque hôtel 100€",
            ],
            "cast": lambda x: x.transaction(-x.costFromRepairs()),
        },
        {
            "text": ["Speeding fine £15", "Amende pour exces de vitesse. 15€"],
            "cast": lambda x: x.transaction(-15),
        },
        {
            "text": [
                "Take a trip to Reading Railroad. If you pass Go, collect £200",
                "Allez a la gare Montparnasse. Si vous passez par la case Depart recevez 200€",
            ],
            "cast": lambda x: x.moveByCard(5),
        },
        {
            "text": [
                "You have been elected Chairman of the Board. Pay each player £50",
                "Vous avez ete elu président du conseil d'administration. Payez 50€ à chaque joueur",
            ],
            "cast": lambda x: x.elected(),
        },
        {
            "text": [
                "Your building loan matures. Collect £150",
                "Votre immeuble et votre pret vous rapportent. Vous devez touchez 150€",
            ],
            "cast": lambda x: x.transaction(150),
        },
    ],
}

random.shuffle(CARDS["chance"])
random.shuffle(CARDS["chest"])