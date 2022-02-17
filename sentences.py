namePlayer = lambda x: f"Joueur {x}"
welcome = "Bienvenue dans le jeu MONOPOLY !"
askNumberOfPlayers = "Combien y a-t-il de joueurs ? (2, 3 ou 4) : "
confirm = lambda x: f"Confirmer {x} joueurs ? (y or n)"
tour = lambda x: f"Au tour du {x}"
diceSentence = 'Vous avez fait'
buySentence = 'Vous avez achetez'
locationSentence = 'Emplacement :'
mortgageSentence = 'Vous avez hypothequez'
unMortgageSentence = 'Vous avez dehypothequez'
buy = 'Acheter'
nobuy = 'Ne pas acheter'
lost = 'Vous avez perdu'
win = 'Vous avez gagne'
wait = 'Attendre'
getFree = 'Sortir de prison pour 50 €'
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
    'choice': 'Choississez une option',
    'player': 'Informations des joueurs',
    'text': 'Affichage du texte',
}
