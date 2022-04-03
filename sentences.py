from dataclasses import dataclass

from constants import LANG

dicts_sentences = {
    "congratulations": [
        lambda x: f"Congratulations {x} ! You won the game !!!",
        lambda x: f"Felicitations {x} ! Vous avez gagne la partie !!!",
    ],
    "current_curn": [lambda x: f"{x}'s turn", lambda x: f"Au tour de {x}"],
    "draw_card": [lambda x: f"Draw {x}", lambda x: f"Vous tirez une carte {x}"],
    "pay_to": [lambda x: f"you pay a rent to {x}", lambda x: f"Vous payez a {x}"],
    "player_buy": [lambda x: f"{x} bought", lambda x: f"{x} a achete"],
    "nbr_turn": ["Number of turn", "Nombre de tour"],
    "money": ["Money", "Argent"],
    "location": ["Location", "Position"],
    "owning": ["Owning", "Possession"],
    "dice": ["You did", "Vous avez fait"],
    "buy": ["You get", "Vous achetez"],
    "buy_building": ["Building on", "Construction sur"],
    "sell_building": ["Sale on", "Vente sur"],
    "is_mortgaged": ["is mortgaged", "est hypotheque"],
    "unmortgage": ["is no longer mortgaged", "n'est plus hypotheque"],
    "salary": ["You get your salary", "Vous recevez votre salaire"],
    "get_free_jail_card": [
        "You get the get out of jail free card",
        "Vous recevez la carte Libere de prison",
    ],
    "use_free_jail_card": [
        "You use the get out of jail free card",
        "Vous utilisez la carte Libere de prison",
    ],
    "mortgaged": ["Mortgaged", "Hypotheque"],
    "house": ["house", "maison"],
    "hotel": ["hotel", "hotel"],
    "remaining_houses": ["Remaining Houses", "Maisons restantes"],
    "remaining_hotels": ["Remaining Hotels", "Hotels restants"],
    "lost": ["You lost", "Vous avez perdu"],
    "win": ["You earn", "Vous avez gagne"],
    "out_of_fail": ["You get out of jail", "Vous sortez de prison"],
    "move_to_jail": ["You go to jail", "Vous allez en prison"],
    "lostGame": [
        "Vous have lost the game :( ....",
        "Vous avez perdu la partie :( ....",
    ],
    "bankruptcy": ["Bankrupt", "En faillite"],
    "money_sign": ["£", "€"],
    "accept_trade": ["accept the deal", "a accepte l'echange"],
    "decline_trade": ["decline the deal", "a refuse l'echange"],
    "is_out": ["is out", "est sorti"],
    "win_auction": ["won the auction", "a gagne la vente aux encheres"],
    "offers": ["offers", "propose"],
    "bid_amount": ["Bis's amount", "Montant de l'encheres"],
    "remains": ["Remaining bidders", "Offreurs restants"],
    "auction_object": ["Object of the auction", "Objet de l'encheres"],
    "choose_tile": [
        "Choose any property you own by entering his id",
        "Choississez la propriete en rentrant son id",
    ],
    "choose_player_pentence": [
        "Choose any player you want to trade with",
        "Choississez le joueur avec qui vous voulez echanger",
    ],
    "choose_number": ["Choose an amount", "Choississez un montant"],
    "action": ["Choose an action", "Choississez une action"],
    "history": ["History", "Historique"],
    "player": ["Players' informations", "Informations des joueurs"],
    "text": ["Text Displaying", "Affichage du texte"],
    "auction": ["Auction", "Vente aux encheres"],
    "trade": ["Trade", "Echange"],
}

menus = {
    "action": [
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
    ],
    "trade": [
        ["Select your properties", "Choisis tes proprietes"],
        ["Give your money", "Donne ton argent"],
        ["Select his properties", "Choisis ses proprietes"],
        ["Get his money", "Prend son argent"],
        ["Propose", "Demande"],
    ],
    "response_trade": [["Accept", "Accepter"], ["Decline", "Decliner"],],
    "buy": [["Buy", "Acheter"], ["Auction", "Mettre aux encheres"],],
    "auction": [["Bid", "Offre"], ["Get out", "Sortir"],],
}


@dataclass
class SentenceStorage:
    data: dict

    def __getitem__(self, item):
        return self.data[item][LANG]


@dataclass
class MenuStorage:
    data: dict

    def __getitem__(self, item):
        return list(map(lambda x: x[LANG], self.data[item]))
    
    
SENTENCES = SentenceStorage(dicts_sentences)
MENUS = MenuStorage(menus)


def format_name(name: str):
    return name.split(",")[LANG].replace("_", " ").title()