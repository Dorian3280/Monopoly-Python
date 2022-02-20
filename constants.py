import curses


std = curses.initscr()


def color_initialize():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, 88, 234)
    curses.init_pair(2, 51, 234)
    curses.init_pair(3, 5, 234)
    curses.init_pair(4, 208, 234)
    curses.init_pair(5, 4, 234)
    curses.init_pair(6, 14, 234)
    curses.init_pair(7, 2, 234)
    curses.init_pair(8, 27, 234)
    curses.init_pair(9, 244, 234)
    curses.init_pair(9, 0, 234)
    return (
        curses.color_pair(1),
        curses.color_pair(2),
        curses.color_pair(3),
        curses.color_pair(4),
        curses.color_pair(5),
        curses.color_pair(6),
        curses.color_pair(7),
        curses.color_pair(8),
        curses.color_pair(9),
        curses.color_pair(10),
    )


COLORS = color_initialize()

ACTIONS = [
    "Jeter les des",
    "Hypothequer une propriete",
    "Deshypothequer une propriete",
    "Construire",
    "Vendre",
    "Fin de tour",
    "Quitter",
    "Se libere de prison"
]

TITLES = {
    'action': 'Effectuer une action',
    'history': 'Historique',
    'player': 'Informations des joueurs',
    'text': 'Affichage du texte',
}

CARDS = {
    'communityChest': [
        { "text": "La vente de votre stock vous rapporte 50€.", 'cast': lambda x: x.transaction(50), 'historyText': "Vous gagnez 50 €" },
        { "text": "Recevez votre revenu annuel 100€.", 'cast': lambda x: x.transaction(100), 'historyText': "Vous gagnez 100 €" },
        { "text": "Payez la note du Medecin 50€.", 'cast': lambda x: x.transaction(-50), 'historyText': "Vous perdez 50 €" },
        { "text": "Vous avez gagne le deuxieme Prix de Beaute. Recevez 100€.", 'cast': lambda x: x.transaction(100), 'historyText': "Vous gagnez 100 €" },
        { "text": "Retournez a Belleville.", 'cast': lambda x: x.moveByCard(1, backward=True), 'historyText': "Vous reculez a Belleville" },
        { "text": "Vous etes libere de prison. Cette carte peut être conservee jusqu'a ce qu'elle soit utilisee ou vendue.", 'cast': lambda x: x.getFreeJailCard(), 'historyText': "Vous recevez la carte Libere de prison" },
        { "text": "Placez vous sur le case Depart.", 'cast': lambda x: x.moveByCard(0), 'historyText': "Vous avancez jusqu'a la case Depart" },
        { "text": "Vous heritez 100€.", 'cast': lambda x: x.transaction(100), 'historyText': "Vous gagnez 100 €" },
        { "text": "Recevez votre interêt sur l'emprunt a 7%. 25€.", 'cast': lambda x: x.transaction(25), 'historyText': "Vous gagnez 25 €" },
        { "text": "Payer a l'Hôpital 100€.", 'cast': lambda x: x.transaction(-100), 'historyText': "Vous perdez 100 €" },
        { "text": "Payer votre Police d'Assurance s'elevant a 50€.", 'cast': lambda x: x.transaction(-50), 'historyText': "Vous perdez 50 €" },
        { "text": "Erreur de la Banque en votre faveur. Recevez 200€.", 'cast': lambda x: x.transaction(200), 'historyText': "Vous gagnez 200 €" },
        { "text": "Les Contributions vous remboursent la somme de 20€.", 'cast': lambda x: x.transaction(20), 'historyText': "Vous gagnez 20 €" },
        { "text": "Allez en prison. Rendez vous directement a la prison. Ne franchissez pas la case Depart. Ne touchez pas 200€.", 'cast': lambda x: x.moveToJail(), 'historyText': "Vous allez en prison" },
        { "text": "Payer une amende de 10€ ou bien tirez une carte CHANCE", 'cast': lambda x: x.transaction(-10), 'historyText': "Vous perdez 10 €" },
        { "text": "C'est votre anniversaire: chaque joueur doit vous donner 10€.", 'cast': lambda x: x.transaction(40), 'historyText': "Vous gagnez 40 €"  },
    ],
    'chance': [
        { "text": "Reculez de 3 cases.", 'cast': lambda x: x.moveByCard(-3, moveBackward=True), 'historyText': "Vous reculez de 3 cases"},
        { "text": "Rendez-vous a la Rue de la Paix.", 'cast': lambda x: x.moveByCard(39), 'historyText': "Vous avancez jusqu'a la Rue de la Paix" },
        { "text": "Payez pour frais de scolarite 150€.", 'cast': lambda x: x.transaction(-150), 'historyText': "Vous perdez 150 €" },
        { "text": "Vous gagnez le prix des mots croises. Recevez 100€", 'cast': lambda x: x.transaction(100), 'historyText': "Vous gagnez 100 €" },
        { "text": "Vous êtes impose pour les reparations de voirie a raison de : 40€ par appartement et 115€ par hôtel.", 'cast': lambda x: x.transaction(-x.getPriceOfAllBuildingsForTHEFUCKING_Card()), 'historyText': "Vous perdez de l'argent €" },
        { "text": "Faites des reparations dans toutes vos maisons. Versez pour chaque maison 25€. Versez pour chaque hôtel 100€.", 'cast': lambda x: x.transaction(-x.getPriceOfAllBuildingsForTHEWORSTFUCKING_Card()), 'historyText': "Vous perdez de l'argent €" },
        { "text": "Amende pour exces de vitesse. 15€.", 'cast': lambda x: x.transaction(-15), 'historyText': "Vous perdez 15 €" },
        { "text": "Avancez au Boulevard de la Villette. Si vous passez par la case Depart recevez 200€.", 'cast': lambda x: x.moveByCard(11), 'historyText': "Vous avancez jusqu'au Boulevard de la Vilette" },
        { "text": "Allez en prison. Rendez vous directement a la prison. Ne franchissez pas la case Depart. Ne touchez pas 200€.", 'cast': lambda x: x.moveToJail(), 'historyText': "Vous allez en prison"  },
        { "text": "Amende pour ivresse : 20€.", 'cast': lambda x: x.transaction(-20), 'historyText': "Vous perdez 20 €" },
        { "text": "Vous êtes libere de prison. Cette carte peut être conservee jusqu'a ce qu'elle soit utilisee ou vendue.", 'cast': lambda x: x.getFreeJailCard(), 'historyText': "Vous recevez la carte Libere de prison" },
        { "text": "La Banque vous verse un dividende de 50€.", 'cast': lambda x: x.transaction(50), 'historyText': "Vous gagnez 50 €" },
        { "text": "Rendez vous a l'Avenue Henri-Martin. Si vous passez par la case Depart recevez 200€.", 'cast': lambda x: x.moveByCard(24), 'historyText': "Vous avancez jusqu'a l'Avenue Henri-Martin" },
        { "text": "Allez a la gare de Lyon. Si vous passez par la case Depart recevez 200€.", 'cast': lambda x: x.moveByCard(15), 'historyText': "Vous avancez jusqu'a la gare de Lyon" },
        { "text": "Avancez jusqu'a la case Depart.", 'cast': lambda x: x.moveByCard(0), 'historyText': "Vous avancez jusqu'a la case Depart" },
        { "text": "Votre immeuble et votre prêt vous rapportent. Vous devez touchez 150€.", 'cast': lambda x: x.transaction(150), 'historyText': "Vous gagnez 150 €" },
    ]
}
