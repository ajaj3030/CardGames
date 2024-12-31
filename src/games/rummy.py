from typing import List, Optional, Set
from src.models.base_game import BaseGame
from src.models.card import Card
from src.models.player_state import PlayerState
from src.models.game_state import GamePhase
from src.models.deck import Deck
from src.ui.terminal_ui import TerminalUI
from src.models.player_action import PlayerAction, PlayerActionType

class Rummy(BaseGame):
    def __init__(self, num_players: int):
        if num_players > 6:
            raise ValueError("Maximum 6 players allowed in Rummy")
        super().__init__(num_players)
        self.discard_pile: List[Card] = []
        self.deal_initial_cards()
        self.has_drawn = False  # Track if player has drawn this turn
        
    def setup_deck(self) -> None:
        """Setup a standard 52-card deck"""
        from ..example import create_standard_deck
        deck = Deck('main', create_standard_deck())
        deck.shuffle()
        self.game_state.add_deck(deck)
        
    def deal_initial_cards(self) -> None:
        """Deal initial cards (7 cards for 2 players, 6 for 3-4, 5 for 5-6)"""
        num_players = len(self.game_state.get_players())
        cards_per_player = 7 if num_players == 2 else 6 if num_players <= 4 else 5
        
        deck = self.game_state.get_deck('main')
        if deck:
            for player in self.game_state.get_players():
                player.add_to_hand(deck.draw(cards_per_player))
            # Start discard pile
            self.discard_pile.extend(deck.draw(1))
            
        self.game_state.set_phase(GamePhase.IN_PROGRESS)
        
    def is_set(self, cards: List[Card]) -> bool:
        """Check if cards form a set (same rank)"""
        if len(cards) < 3:
            return False
        return len({card.rank for card in cards}) == 1
        
    def is_run(self, cards: List[Card]) -> bool:
        """Check if cards form a run (consecutive ranks of same suit)"""
        if len(cards) < 3:
            return False
            
        # Check same suit
        if len({card.suit for card in cards}) != 1:
            return False
            
        # Check consecutive ranks
        ranks = sorted(card.rank for card in cards)
        return all(ranks[i] == ranks[i-1] + 1 for i in range(1, len(ranks)))
        
    def play_turn(self, player: PlayerState) -> None:
        """Execute a turn for the given player"""
        if player.id == 'p0':  # Human player
            self._play_human_turn(player)
        else:  # AI player
            self._play_ai_turn(player)
            
    def _play_human_turn(self, player: PlayerState) -> None:
        """Handle human player's turn"""
        self.has_drawn = False
        
        while True:
            TerminalUI.display_rummy_state(player, self.discard_pile)
            action = TerminalUI.get_rummy_action(player, can_draw_discard=not self.has_drawn and bool(self.discard_pile))
            
            if action.action_type == PlayerActionType.QUIT:
                self.game_state.set_phase(GamePhase.COMPLETE)
                return
                
            if not self.has_drawn:
                if action.action_type == PlayerActionType.DRAW_DECK:
                    deck = self.game_state.get_deck('main')
                    if deck:
                        player.add_to_hand(deck.draw(1))
                        self.has_drawn = True
                elif action.action_type == PlayerActionType.DRAW_DISCARD:
                    if self.discard_pile:
                        player.add_to_hand([self.discard_pile.pop()])
                        self.has_drawn = True
            
            if self.has_drawn:
                if action.action_type == PlayerActionType.DISCARD:
                    if action.cards:
                        removed = player.remove_from_hand([action.cards[0].id])
                        self.discard_pile.extend(removed)
                        return
                elif action.action_type == PlayerActionType.DECLARE_SET:
                    if self.is_set(action.cards):
                        print("Valid set!")
                        for card in action.cards:
                            player.remove_from_hand([card.id])
                    else:
                        print("Invalid set!")
                elif action.action_type == PlayerActionType.DECLARE_RUN:
                    if self.is_run(action.cards):
                        print("Valid run!")
                        for card in action.cards:
                            player.remove_from_hand([card.id])
                    else:
                        print("Invalid run!")
            
    def _play_ai_turn(self, player: PlayerState) -> None:
        """Execute a turn for the AI player"""
        # Draw phase
        deck = self.game_state.get_deck('main')
        if deck and len(deck.draw(1)) > 0:  # AI always draws from deck
            player.add_to_hand(deck.draw(1))
            
        # Discard phase
        hand = player.get_hand()
        # Simple AI: discard highest card that's not part of a set or run
        for card in sorted(hand, key=lambda c: c.rank, reverse=True):
            remaining = [c for c in hand if c.id != card.id]
            if not self.is_set(remaining) and not self.is_run(remaining):
                removed = player.remove_from_hand([card.id])
                self.discard_pile.extend(removed)
                break
                
    def check_win_condition(self) -> Optional[PlayerState]:
        """Check if any player has won (all cards in sets or runs)"""
        for player in self.game_state.get_players():
            hand = player.get_hand()
            # This is a simplified win check - you'd want more sophisticated logic
            if self.is_set(hand) or self.is_run(hand):
                return player
        return None 