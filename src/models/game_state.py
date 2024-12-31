from typing import List, Dict, Optional
from .player_state import PlayerState
from .deck import Deck

class GamePhase:
    SETUP = "setup"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"

class GameState:
    def __init__(self):
        self._players: List[PlayerState] = []
        self._current_player_index: int = 0
        self._phase: str = GamePhase.SETUP
        self._decks: Dict[str, Deck] = {}

    def add_player(self, player: PlayerState) -> None:
        """Add a player to the game"""
        self._players.append(player)

    def add_deck(self, deck: Deck) -> None:
        """Add a deck to the game"""
        self._decks[deck.id] = deck

    def get_current_player(self) -> PlayerState:
        """Get the current player"""
        return self._players[self._current_player_index]

    def next_turn(self) -> None:
        """Advance to the next player's turn"""
        self._current_player_index = (self._current_player_index + 1) % len(self._players)

    def set_phase(self, phase: str) -> None:
        """Set the game phase"""
        self._phase = phase

    def get_phase(self) -> str:
        """Get the current game phase"""
        return self._phase

    def get_deck(self, deck_id: str) -> Optional[Deck]:
        """Get a deck by its ID"""
        return self._decks.get(deck_id)

    def get_players(self) -> List[PlayerState]:
        """Get a list of all players"""
        return self._players.copy() 