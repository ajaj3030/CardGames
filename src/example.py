from models.card import Card, CardEffect
from models.deck import Deck
from models.game_state import GameState, GamePhase
from models.player_state import PlayerState
from typing import List

def create_standard_deck() -> List[Card]:
    """Create a standard 52-card deck"""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    cards = []
    
    for suit in suits:
        for rank in range(1, 14):
            name = f"{rank if rank not in {1,11,12,13} else {1:'Ace',11:'Jack',12:'Queen',13:'King'}[rank]} of {suit}"
            cards.append(Card(
                id=f"{suit}-{rank}",
                name=name,
                suit=suit,
                rank=rank,
                type='standard'
            ))
    
    return cards

def main():
    # Create game instance
    game = GameState()

    # Create and add players
    player1 = PlayerState('p1', 'Alice')
    player2 = PlayerState('p2', 'Bob')
    game.add_player(player1)
    game.add_player(player2)

    # Create and add deck
    main_deck = Deck('main', create_standard_deck())
    main_deck.shuffle()
    game.add_deck(main_deck)

    # Deal initial hands
    deck = game.get_deck('main')
    if deck:
        player1.add_to_hand(deck.draw(5))
        player2.add_to_hand(deck.draw(5))

    game.set_phase(GamePhase.IN_PROGRESS)

if __name__ == "__main__":
    main() 