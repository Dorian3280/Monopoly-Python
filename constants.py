ACTIONS = [
    "Jeter les des",
    "Hypothequer une propriete",
    "Deshypothequer une propriete",
    "Construire",
    "Vendre",
    "Fin de tour",
    "Essayer de faire un double",
    "Payer 50 € pour sortir de prison",
    "Utiliser la carte Liberer de Prison",
    "Quitter",
]

TITLES = {
    "action": "Effectuer une action",
    "history": "Historique",
    "player": "Informations des joueurs",
    "text": "Affichage du texte",
    "gameInfo": "Informations de la partie",
}

CARDS = {
    "communityChest": [
        {
            "text": "La vente de votre stock vous rapporte 50€.",
            "cast": lambda x: x.transaction(50),
        },
        {
            "text": "Recevez votre revenu annuel 100€.",
            "cast": lambda x: x.transaction(100),
        },
        {
            "text": "Payez la note du Medecin 50€.",
            "cast": lambda x: x.transaction(-50)},
        {
            "text": "Vous avez gagne le deuxieme Prix de Beaute. Recevez 100€.",
            "cast": lambda x: x.transaction(100),
        },
        {
            "text": "Retournez a Belleville.",
            "cast": lambda x: x.moveByCard(1, backward=True),
        },
        {
            "text": "Vous etes libere de prison. Cette carte peut être conservee jusqu'a ce qu'elle soit utilisee ou vendue.",
            "cast": lambda x: x.getFreeJailCard(),
        },
        {
            "text": "Placez vous sur le case Depart.",
            "cast": lambda x: x.moveByCard(0)},
        {
            "text": "Vous heritez 100€.",
            "cast": lambda x: x.transaction(100)},
        {
            "text": "Recevez votre interêt sur l'emprunt a 7%. 25€.",
            "cast": lambda x: x.transaction(25),
        },
        {
            "text": "Payer a l'Hôpital 100€.",
            "cast": lambda x: x.transaction(-100)},
        {
            "text": "Payer votre Police d'Assurance s'elevant a 50€.",
            "cast": lambda x: x.transaction(-50),
        },
        {
            "text": "Erreur de la Banque en votre faveur. Recevez 200€.",
            "cast": lambda x: x.transaction(200),
        },
        {
            "text": "Les Contributions vous remboursent la somme de 20€.",
            "cast": lambda x: x.transaction(20),
        },
        {
            "text": "Allez en prison. Rendez vous directement a la prison. Ne franchissez pas la case Depart. Ne touchez pas 200€.",
            "cast": lambda x: x.moveToJail(),
        },
        {
            "text": "Payer une amende de 10€ ou bien tirez une carte CHANCE",
            "cast": lambda x: x.transaction(-10),
        },
        {
            "text": "C'est votre anniversaire: chaque joueur doit vous donner 10€.",
            "cast": lambda x: x.transaction(40),
        },
    ],
    "chance": [
        {
            "text": "Allez en prison. Rendez vous directement a la prison. Ne franchissez pas la case Depart. Ne touchez pas 200€.",
            "cast": lambda x: x.moveToJail(),
        },
        {
            "text": "Reculez de 3 cases.",
            "cast": lambda x: x.moveByCard(-3, moveBackward=True),
        },
        {
            "text": "Rendez-vous a la Rue de la Paix.",
            "cast": lambda x: x.moveByCard(39),
        },
        {
            "text": "Payez pour frais de scolarite 150€.",
            "cast": lambda x: x.transaction(-150),
        },
        {
            "text": "Vous gagnez le prix des mots croises. Recevez 100€",
            "cast": lambda x: x.transaction(100),
        },
        {
            "text": "Vous êtes impose pour les reparations de voirie a raison de : 40€ par appartement et 115€ par hôtel.",
            "cast": lambda x: x.transaction(
                -x.getPriceOfAllBuildingsForTHEFUCKING_Card()
            ),
        },
        {
            "text": "Faites des reparations dans toutes vos maisons. Versez pour chaque maison 25€. Versez pour chaque hôtel 100€.",
            "cast": lambda x: x.transaction(
                -x.getPriceOfAllBuildingsForTHEWORSTFUCKING_Card()
            ),
        },
        {
            "text": "Amende pour exces de vitesse. 15€.",
            "cast": lambda x: x.transaction(-15),
        },
        {
            "text": "Avancez au Boulevard de la Villette. Si vous passez par la case Depart recevez 200€.",
            "cast": lambda x: x.moveByCard(11),
        },
        {
            "text": "Amende pour ivresse : 20€.",
            "cast": lambda x: x.transaction(-20)},
        {
            "text": "Vous êtes libere de prison. Cette carte peut être conservee jusqu'a ce qu'elle soit utilisee ou vendue.",
            "cast": lambda x: x.getFreeJailCard(),
        },
        {
            "text": "La Banque vous verse un dividende de 50€.",
            "cast": lambda x: x.transaction(50),
        },
        {
            "text": "Rendez vous a l'Avenue Henri-Martin. Si vous passez par la case Depart recevez 200€.",
            "cast": lambda x: x.moveByCard(24),
        },
        {
            "text": "Allez a la gare de Lyon. Si vous passez par la case Depart recevez 200€.",
            "cast": lambda x: x.moveByCard(15),
        },
        {
            "text": "Avancez jusqu'a la case Depart.",
            "cast": lambda x: x.moveByCard(0)},
        {
            "text": "Votre immeuble et votre prêt vous rapportent. Vous devez touchez 150€.",
            "cast": lambda x: x.transaction(150),
        },
    ],
}
