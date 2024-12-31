from typing import List
from .card import Card

class PlayerState:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self._hand: List[Card] = []
        self._score: int = 0

    def add_to_hand(self, cards: List[Card]) -> None:
        """Add cards to player's hand"""
        self._hand.extend(cards)

    def remove_from_hand(self, card_ids: List[str]) -> List[Card]:
        """Remove and return cards from player's hand"""
        removed_cards: List[Card] = []
        remaining_cards: List[Card] = []

        for card in self._hand:
            if card.id in card_ids:
                removed_cards.append(card)
            else:
                remaining_cards.append(card)

        self._hand = remaining_cards
        return removed_cards

    def get_hand(self) -> List[Card]:
        """Get a copy of player's hand"""
        return self._hand.copy()

    def update_score(self, points: int) -> None:
        """Update player's score"""
        self._score += points

    def get_score(self) -> int:
        """Get player's current score"""
        return self._score 