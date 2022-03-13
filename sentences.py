congratulations = [
    lambda x: f"Congratulations {x} ! You won the game !!!",
    lambda x: f"Felicitations {x} ! Vous avez gagné la partie !!!",
]
currentTurn = [
    lambda x: f"{x}'s turn",
    lambda x: f"Au tour de {x}",
]
drawCards = [
    lambda x: f"Draw {x} card",
    lambda x: f"Vous tirez une carte {x}",
]
payToSentence = [
    lambda x: f"you pay a rent to {x}",
    lambda x: f"Vous payez a {x}",
]
nbrTurnSentence = ["Number of turn", "Nombre de tour"]
money = ["Money", "Argent"]
location = ["Location", "Position"]
owning = ["Owning", "Possession"]
diceSentence = ["You did", "Vous avez fait"]
buySentence = ["You get", "Vous achetez"]
buyBuildingSentence = ["Building on", "Construction sur"]
sellBuildingSentence = ["Sale on", "Vente sur"]
mortgageSentence = ["is mortgaged", "est hypotheque"]
unMortgageSentence = ["is no longer mortgaged", "n'est plus hypotheque"]
salary = ["You get your salary", "Vous recevez votre salaire"]
getFreeJailCard = [
    "You get the get out of jail free card",
    "Vous recevez la carte Libere de prison",
]
useFreeJailCard = [
    "You use the get out of jail free card",
    "Vous utilisez la carte Libere de prison",
]
mortgage = ["Mortgaged", "Hypotheque"]
house = ["house", "maison"]
hotel = ["hotel", "hotel"]
buy = ["Buy", "Acheter"]
notBuy = ["Do not buy", "Ne pas acheter"]
lost = ["You lost", "Vous avez perdu"]
win = ["You earn", "Vous avez gagne"]
free = ["You get out of jail", "Vous sortez de prison"]
inJail = ["You go to jail", "Vous allez en prison"]
lost = ["Vous have lost the game :( ....", "Vous avez perdu la partie :( ...."]
bankruptcy = ["Bankrupt", "En faillite"]
moneySign = ["£", "€"]

ACTIONS = [
    ["Roll Dice", "Jeter les des"],
    ["Mortgage", "Hypothequer une propriete"],
    ["Unmortgage", "Deshypothequer une propriete"],
    ["Build", "Construire"],
    ["Sell", "Vendre"],
    ["End your turn", "Fin de tour"],
    ["Throwing doubles", "Essayer de faire un double"],
    ["Pay a fine of 50 €", "Payer 50 € pour sortir de prison"],
    ["Use the get out of jail card", "Utiliser la carte Liberer de Prison"],
    ["Retire from the game", "Sortir de la partie"],
]

TITLES = {
    "action": ["Press a key", "Appuyer sur une touche"],
    "history": ["History", "Historique"],
    "player": ["Players' informations", "Informations des joueurs"],
    "text": ["Text Displaying", "Affichage du texte"],
    "info": ["Game's information", "Informations de la partie"],
}
