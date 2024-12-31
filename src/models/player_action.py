from dataclasses import dataclass
from typing import List, Optional
from .card import Card

@dataclass
class PlayerAction:
    action_type: str
    cards: List[Card] = None
    amount: int = 0
    
    def __post_init__(self):
        self.cards = self.cards or []

class PlayerActionType:
    # Common actions
    QUIT = "quit"
    
    # Poker actions
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"
    
    # Blackjack actions
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    
    # Rummy actions
    DRAW_DECK = "draw_deck"
    DRAW_DISCARD = "draw_discard"
    DISCARD = "discard"
    DECLARE_SET = "declare_set"
    DECLARE_RUN = "declare_run" 