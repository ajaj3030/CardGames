from abc import ABC, abstractmethod
from typing import List, Optional
from .game_state import GameState, GamePhase
from .player_state import PlayerState
from .deck import Deck
from .card import Card

class BaseGame(ABC):
    def __init__(self, num_players: int):
        if num_players < 2:
            raise ValueError("Number of players must be at least 2")
            
        self.game_state = GameState()
        self.setup_players(num_players)
        self.setup_deck()
        
    def setup_players(self, num_players: int) -> None:
        """Setup players including the human player"""
        # First player (index 0) is always the human player
        self.game_state.add_player(PlayerState('p0', 'Human Player'))
        
        # Add AI players
        for i in range(1, num_players):
            self.game_state.add_player(PlayerState(f'p{i}', f'AI Player {i}'))
    
    @abstractmethod
    def setup_deck(self) -> None:
        """Setup the deck(s) needed for the game"""
        pass
        
    @abstractmethod
    def deal_initial_cards(self) -> None:
        """Deal the initial cards for the game"""
        pass
        
    @abstractmethod
    def play_turn(self, player: PlayerState) -> None:
        """Execute a turn for the given player"""
        pass
        
    @abstractmethod
    def check_win_condition(self) -> Optional[PlayerState]:
        """Check if there's a winner. Returns winning player or None"""
        pass 