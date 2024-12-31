from typing import List
import random
from .card import Card

class Deck:
    def __init__(self, id: str, initial_cards: List[Card] = None):
        self.id = id
        self._cards = initial_cards.copy() if initial_cards else []
        self._discard_pile: List[Card] = []

    def shuffle(self) -> None:
        """Shuffle the deck using Fisher-Yates algorithm"""
        random.shuffle(self._cards)

    def draw(self, count: int = 1) -> List[Card]:
        """Draw specified number of cards from the deck"""
        if count > len(self._cards):
            # Reshuffle discard pile if needed
            self._cards.extend(self._discard_pile)
            self._discard_pile.clear()
            self.shuffle()
        
        drawn_cards = self._cards[:count]
        self._cards = self._cards[count:]
        return drawn_cards

    def add_to_discard(self, cards: List[Card]) -> None:
        """Add cards to the discard pile"""
        self._discard_pile.extend(cards)

    def add_cards(self, cards: List[Card]) -> None:
        """Add cards to the deck"""
        self._cards.extend(cards)

    @property
    def remaining_cards(self) -> int:
        return len(self._cards)

    @property
    def discard_count(self) -> int:
        return len(self._discard_pile) 