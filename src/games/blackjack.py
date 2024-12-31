from typing import List, Optional
from src.models.base_game import BaseGame
from src.models.card import Card
from src.models.player_state import PlayerState
from src.models.game_state import GamePhase
from src.models.deck import Deck
from ..ui.terminal_ui import TerminalUI
from ..models.player_action import PlayerActionType

class Blackjack(BaseGame):
    def __init__(self, num_players: int):
        if num_players > 7:
            raise ValueError("Maximum 7 players allowed in Blackjack")
        super().__init__(num_players)
        self.dealer_hand: List[Card] = []
        self.deal_initial_cards()
        
    def setup_deck(self) -> None:
        """Setup a standard 52-card deck"""
        from ..example import create_standard_deck
        # Typically uses multiple decks
        deck = Deck('main', create_standard_deck() * 6)  # 6 decks
        deck.shuffle()
        self.game_state.add_deck(deck)
        
    def deal_initial_cards(self) -> None:
        """Deal 2 cards to each player and dealer"""
        deck = self.game_state.get_deck('main')
        if deck:
            # Deal first card to all players
            for player in self.game_state.get_players():
                player.add_to_hand(deck.draw(1))
            self.dealer_hand.extend(deck.draw(1))
            
            # Deal second card
            for player in self.game_state.get_players():
                player.add_to_hand(deck.draw(1))
            self.dealer_hand.extend(deck.draw(1))
            
        self.game_state.set_phase(GamePhase.IN_PROGRESS)
        
    def calculate_hand_value(self, cards: List[Card]) -> int:
        """Calculate the value of a blackjack hand"""
        value = 0
        aces = 0
        
        for card in cards:
            if card.rank == 1:  # Ace
                aces += 1
            elif card.rank > 10:  # Face cards
                value += 10
            else:
                value += card.rank
                
        # Add aces
        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
                
        return value
        
    def play_turn(self, player: PlayerState) -> None:
        """Execute a turn for the given player"""
        if player.id == 'p0':  # Human player
            self._play_human_turn(player)
        else:  # AI player
            self._play_ai_turn(player)
            
    def _play_human_turn(self, player: PlayerState) -> None:
        """Handle human player's turn"""
        while True:
            TerminalUI.display_blackjack_state(player, self.dealer_hand)
            action = TerminalUI.get_blackjack_action()
            
            if action.action_type == PlayerActionType.QUIT:
                self.game_state.set_phase(GamePhase.COMPLETE)
                return
                
            if action.action_type == PlayerActionType.HIT:
                deck = self.game_state.get_deck('main')
                if deck:
                    player.add_to_hand(deck.draw(1))
                    if self.calculate_hand_value(player.get_hand()) > 21:
                        print("Bust!")
                        return
            elif action.action_type == PlayerActionType.STAND:
                return
                
    def _play_ai_turn(self, player: PlayerState) -> None:
        """Handle AI player's turn"""
        hand_value = self.calculate_hand_value(player.get_hand())
        
        if hand_value < 17:  # Basic AI strategy
            deck = self.game_state.get_deck('main')
            if deck:
                player.add_to_hand(deck.draw(1))
                
    def play_dealer_turn(self) -> None:
        """Execute the dealer's turn"""
        deck = self.game_state.get_deck('main')
        while deck and self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.extend(deck.draw(1))
            
    def check_win_condition(self) -> Optional[PlayerState]:
        """Check for winners against the dealer"""
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        if dealer_value > 21:  # Dealer busts
            # All players who haven't busted win
            for player in self.game_state.get_players():
                player_value = self.calculate_hand_value(player.get_hand())
                if player_value <= 21:
                    player.update_score(1)  # Award 1 point for winning
                    return player
                    
        # Find highest hand that beats dealer
        best_player = None
        best_value = dealer_value
        
        for player in self.game_state.get_players():
            player_value = self.calculate_hand_value(player.get_hand())
            if player_value <= 21 and player_value > best_value:
                best_value = player_value
                best_player = player
                
        if best_player:
            best_player.update_score(1)  # Award 1 point for winning
            
        return best_player