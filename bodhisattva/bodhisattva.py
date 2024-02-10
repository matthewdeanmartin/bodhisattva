import random
from typing import List


class Card:
    def __init__(self, name: str, card_type: str, abilities: List[str]):
        self.name = name
        self.card_type = card_type
        self.abilities = abilities

class BodhisattvaCard(Card):
    def __init__(self, name: str, abilities: List[str]):
        super().__init__(name, "bodhisattva", abilities)
        self.merit = 3

class ActionCard(Card):
    def __init__(self, name: str, abilities: List[str]):
        super().__init__(name, "action", abilities)

class Realm:
    def __init__(self, name: str, rules: List[str]):
        self.name = name
        self.rules = rules
        self.sentient_being = None

class SentientBeing:
    def __init__(self, name: str, abilities: List[str]):
        self.name = name
        self.abilities = abilities
        self.health = 3
        self.karma = -3

class Player:
    def __init__(self, name: str, deck: List[Card]):
        self.name = name
        self.deck = deck
        self.hand = []
        self.points = 0
        self.opponent = None
        self.action_cards_in_play = []
        self.bodhisattva_in_play = None

# Create a list of Bodhisattva cards
bodhisattva_cards = [
    BodhisattvaCard("Avalokiteshvara", ["heal", "protect"]),
    BodhisattvaCard("Manjushri", ["enlighten", "cut through delusion"]),
    BodhisattvaCard("Vajrapani", ["purify", "destroy obstacles"]),
]

# Create a list of action cards
action_cards = [
    ActionCard("Meditation", ["draw two cards"]),
    ActionCard("Compassion", ["heal all realms"]),
    ActionCard("Wisdom", ["reveal opponent's hand"]),
]

# Create a list of realms
realms = [
    Realm("Heaven", ["bodhisattvas can only heal"]),
    Realm("Asura", ["bodhisattvas can only protect"]),
    Realm("Human", ["bodhisattvas can use any ability"]),
    Realm("Animal", ["bodhisattvas can only heal"]),
    Realm("Hungry Ghost", ["bodhisattvas can only purify"]),
    Realm("Hell", ["bodhisattvas can only protect"]),
]

# Create a list of sentient beings
sentient_beings = [
    SentientBeing("Deva", ["grant extra points"]),
    SentientBeing("Asura", ["steal points from opponent"]),
    SentientBeing("Human", ["draw extra card"]),
    SentientBeing("Animal", ["nothing"]),
    SentientBeing("Hungry Ghost", ["nothing"]),
    SentientBeing("Hell Being", ["nothing"]),
]

# Shuffle the lists of cards and realms
random.shuffle(bodhisattva_cards)
random.shuffle(action_cards)
random.shuffle(realms)

# Create the deck for player 1 by combining the Bodhisattva and action cards
player1_deck = bodhisattva_cards + action_cards

# Create the player 1 object
player1 = Player("Player 1", player1_deck)

# Repeat the process for player 2
player2_deck = bodhisattva_cards + action_cards
random.shuffle(player2_deck)
player2 = Player("Player 2", player2_deck)

player2.opponent = player1
player1.opponent = player2

# Initialize the game state
random.shuffle(player1.deck)
player1.hand = player1.deck[:5]
random.shuffle(player2.deck)
player2.hand = player2.deck[:5]
random.shuffle(realms)
current_realm = realms[0]
current_player = player1

def display_table(realms: List[Realm]):
    for realm in realms:
        if realm.sentient_being is None:
            print(f"{realm.name}: empty")
        else:
            print(f"{realm.name}: {realm.sentient_being.name}")

def calculate_liberation(realm: Realm,
                         player1: Player,
                         player2: Player) -> True:
    # Check if either player has the "liberate" ability
    resolved = False
    for action_card in player1.action_cards_in_play:
        if "liberate" in action_card.abilities:
            player1.points += 1
            resolved = True
        if "liberate" in action_card.abilities:
            player2.points += 1
            resolved = True
    if resolved:
        return True

    # If neither player has the "liberate" ability, check the realm's rules
    if "bodhisattvas can use any ability" in realm.rules:
        # If the realm's rules allow any ability to be used, return the player with the most points
        if player1.points > player2.points:
            player1.points += 1
            return player1
        else:
            player2.points += 1
            return player2
    else:
        # If the realm's rules restrict the abilities that can be used, return the player with the ability that is allowed
        for ability in realm.rules:
            if ability in player1.abilities:
                player1.points += 1
                return player1
            elif ability in player2.abilities:
                player2.points += 1
                return player2


# Start the game loop
while True:
    # Display the current game state
    print(f"Current realm: {current_realm.name}", end="")
    if current_realm.sentient_being:
        print(f" occupied by a {current_realm.sentient_being.name}")
    else:
        print()

    display_table(realms)
    print(f"{player1.name}'s hand: {[card.name for card in player1.hand]}")
    print(f"{player2.name}'s hand: {[card.name for card in player2.hand]}")

    # Allow the current player to play a card
    print(f"{current_player.name}, choose a card to play:")
    for i, card in enumerate(current_player.hand):
        print(f"{i + 1}: {card.name}")
    chosen_card = int(input()) - 1
    played_card = current_player.hand[chosen_card]

    current_player.hand.remove(played_card)

    # Use the played card's abilities
    if played_card.card_type == "bodhisattva":
        current_player.bodhisattva_in_play  = played_card
        print("Choose an ability to use:")
        for i, ability in enumerate(played_card.abilities):
            print(f"{i + 1}: {ability}")
        chosen_ability = int(input()) - 1
        ability = played_card.abilities[chosen_ability]
        if ability == "heal":
            current_realm.sentient_being.health += 1
        elif ability == "protect":
            current_realm.sentient_being.protection += 1
        elif played_card.card_type == "action":
            current_player.action_cards_in_play.append(played_card)
            print("Choose an ability to use:")
            for i, ability in enumerate(played_card.abilities):
                print(f"{i + 1}: {ability}")
            chosen_ability = int(input()) - 1
            ability = played_card.abilities[chosen_ability]
            if ability == "draw two cards":
                current_player.hand += current_player.deck[:2]
                current_player.deck = current_player.deck[2:]
            elif ability == "heal all realms":
                for realm in realms:
                    realm.sentient_being.health += 1
            elif ability == "reveal opponent's hand":
                print(
                    f"{current_player.name}'s opponent's hand: {[card.name for card in current_player.opponent.hand]}")

        # Liberation check
        calculate_liberation()

        # Draw a new realm card and place it in the current realm
        current_realm = realms[0]
        realms = realms[1:]
        current_realm.sentient_being = sentient_beings[0]
        sentient_beings = sentient_beings[1:]

        # Switch the current player
        if current_player == player1:
            current_player = player2
        else:
            current_player = player1

        # Check if a player has won
        if player1.points >= 10:
            print(f"{player1.name} wins!")
            break
        elif player2.points >= 10:
            print(f"{player2.name} wins!")
            break

        # If the realm deck is empty, shuffle the discard pile and use it as the new realm deck
        if not realms:
            realms = random.shuffle(realms)

