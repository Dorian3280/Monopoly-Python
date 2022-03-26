congratulations = lambda x: [
    f"Congratulations {x} ! You won the game !!!",
    f"Felicitations {x} ! Vous avez gagne la partie !!!",
]
currentTurn = lambda x: [f"{x}'s turn", f"Au tour de {x}"]
drawCards = lambda x: [f"Draw {x}", f"Vous tirez une carte {x}"]
payToSentence = lambda x: [f"you pay a rent to {x}", f"Vous payez a {x}"]
playerBuySentence = lambda x: [f"{x} bought", f"{x} a achete"]

genName = ["Player", "Joueur"]
nbrTurnSentence = ["Number of turn", "Nombre de tour"]
money = ["Money", "Argent"]
location = ["Location", "Position"]
owning = ["Owning", "Possession"]
diceSentence = ["You did", "Vous avez fait"]
buySentence = ["You get", "Vous achetez"]
buyBuildingSentence = ["Building on", "Construction sur"]
sellBuildingSentence = ["Sale on", "Vente sur"]
mortgageSentence = ["is mortgaged", "est hypotheque"]
unmortgageSentence = ["is no longer mortgaged", "n'est plus hypotheque"]
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
remainingHouses = ["Remaining Houses", "Maisons restantes"]
remainingHotels = ["Remaining Hotels", "Hotels restants"]
buy = ["Buy", "Acheter"]
auction = ["Auction", "Mettre aux encheres"]
lost = ["You lost", "Vous avez perdu"]
win = ["You earn", "Vous avez gagne"]
outOfFailSentence = ["You get out of jail", "Vous sortez de prison"]
moveToJailSentence = ["You go to jail", "Vous allez en prison"]
lostGame = ["Vous have lost the game :( ....", "Vous avez perdu la partie :( ...."]
bankruptcy = ["Bankrupt", "En faillite"]
moneySign = ["£", "€"]
accept = ["Accept", "Accepter"]
decline = ["Decline", "Decliner"]
acceptTrade = ["accept the deal", "a accepte l'echange"]
declineTrade = ["decline the deal", "a refuse l'echange"]
bid = ["Bid", "Offre"]
out = ["Get out", "Sortir"]
isOut = ["is out", "est sorti"]
winAuction = ["won the auction", "a gagne la vente aux encheres"]
offers = ["offers", "propose"]
bidAmountSentence = ["Bis's amount", "Montant de l'encheres"]
remains = ["Remaining bidders", "Offreurs restants"]
objectOfAuction = ["Object of the auction", "Objet de l'encheres"]
chooseTileSentence = [
    "Choose any property you own by entering his id",
    "Choississez la propriete en rentrant son id",
]
choosePlayerSentence = [
    "Choose any player you want to trade with",
    "Choississez le joueur avec qui vous voulez echanger",
]
chooseNumberSentence = ["Choose an amount", "Choississez un montant"]

ACTIONS = [
    ["Roll Dice", "Jeter les des"],
    ["Mortgage", "Hypothequer une propriete"],
    ["Unmortgage", "Deshypothequer une propriete"],
    ["Build", "Construire"],
    ["Sell", "Vendre"],
    ["End your turn", "Fin de tour"],
    ["Throwing doubles", "Essayer de faire un double"],
    ["Pay a fine of 50€", "Payer 50€ pour sortir de prison"],
    ["Use the get out of jail card", "Utiliser la carte Liberer de Prison"],
    ["Retire from the game", "Sortir de la partie"],
]

TITLES = {
    "action": ["Choose an action", "Choississez une action"],
    "history": ["History", "Historique"],
    "player": ["Players' informations", "Informations des joueurs"],
    "text": ["Text Displaying", "Affichage du texte"],
    "auction": ["Auction", "Vente aux encheres"],
    "trade": ["Trade", "Echange"],
}

TRADE = [
    ["Select your properties", "Choisis tes proprietes"],
    ["Give your money", "Donne ton argent"],
    ["Select his properties", "Choisis ses proprietes"],
    ["Get his money", "Prend son argent"],
    ["Propose", "Demande"],
]
