from typing import List, Dict, Optional
from src.models.base_game import BaseGame
from src.models.card import Card
from src.models.player_state import PlayerState
from src.models.game_state import GamePhase
from src.models.deck import Deck
from src.ui.terminal_ui import TerminalUI
from src.models.player_action import PlayerAction, PlayerActionType

class PokerHand:
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

class Poker(BaseGame):
    def __init__(self, num_players: int):
        if num_players > 10:
            raise ValueError("Maximum 10 players allowed in Poker")
        super().__init__(num_players)
        self.pot = 0
        self.community_cards: List[Card] = []
        self.current_bet = 0
        self.deal_initial_cards()
        self.betting_round = 0  # 0: pre-flop, 1: flop, 2: turn, 3: river
        
    def setup_deck(self) -> None:
        """Setup a standard 52-card deck"""
        from ..example import create_standard_deck
        deck = Deck('main', create_standard_deck())
        deck.shuffle()
        self.game_state.add_deck(deck)
        
    def deal_initial_cards(self) -> None:
        """Deal 2 cards to each player"""
        deck = self.game_state.get_deck('main')
        if deck:
            for player in self.game_state.get_players():
                player.add_to_hand(deck.draw(2))
        self.game_state.set_phase(GamePhase.IN_PROGRESS)
        
    def deal_community_cards(self, count: int) -> None:
        """Deal community cards (flop, turn, or river)"""
        deck = self.game_state.get_deck('main')
        if deck:
            self.community_cards.extend(deck.draw(count))
            
    def evaluate_hand(self, player: PlayerState) -> int:
        """Evaluate the poker hand strength"""
        all_cards = player.get_hand() + self.community_cards
        
        # Sort cards by rank
        sorted_cards = sorted(all_cards, key=lambda x: x.rank)
        
        # Check for flush
        suits = {}
        for card in all_cards:
            suits[card.suit] = suits.get(card.suit, 0) + 1
        has_flush = any(count >= 5 for count in suits.values())
        
        # Check for straight
        has_straight = False
        for i in range(len(sorted_cards) - 4):
            if sorted_cards[i+4].rank - sorted_cards[i].rank == 4:
                has_straight = True
                break
                
        # Count ranks
        rank_counts = {}
        for card in all_cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
            
        # Check for various hands
        has_four = any(count == 4 for count in rank_counts.values())
        has_three = any(count == 3 for count in rank_counts.values())
        pairs = sum(1 for count in rank_counts.values() if count == 2)
        
        # Determine hand value
        if has_straight and has_flush:
            if max(card.rank for card in all_cards) == 13:  # Ace high
                return PokerHand.ROYAL_FLUSH
            return PokerHand.STRAIGHT_FLUSH
        elif has_four:
            return PokerHand.FOUR_OF_A_KIND
        elif has_three and pairs >= 1:
            return PokerHand.FULL_HOUSE
        elif has_flush:
            return PokerHand.FLUSH
        elif has_straight:
            return PokerHand.STRAIGHT
        elif has_three:
            return PokerHand.THREE_OF_A_KIND
        elif pairs == 2:
            return PokerHand.TWO_PAIR
        elif pairs == 1:
            return PokerHand.PAIR
        else:
            return PokerHand.HIGH_CARD
        
    def play_turn(self, player: PlayerState) -> None:
        """Execute a betting round for the player"""
        if player.id == 'p0':  # Human player
            self._play_human_turn(player)
        else:  # AI player
            self._play_ai_turn(player)
            
        # After each round of betting, deal community cards
        if all(p.get_score() == self.current_bet for p in self.game_state.get_players()):
            self._advance_betting_round()
            
    def _play_human_turn(self, player: PlayerState) -> None:
        """Handle human player's turn"""
        TerminalUI.display_poker_state(player, self.community_cards, self.pot)
        action = TerminalUI.get_poker_action()
        
        if action.action_type == PlayerActionType.QUIT:
            self.game_state.set_phase(GamePhase.COMPLETE)
            return
            
        if action.action_type == PlayerActionType.FOLD:
            self.game_state._players.remove(player)
        elif action.action_type == PlayerActionType.CALL:
            call_amount = self.current_bet - player.get_score()
            self.pot += call_amount
            player.update_score(-call_amount)
        elif action.action_type == PlayerActionType.RAISE:
            raise_amount = action.amount
            if raise_amount > self.current_bet:
                self.pot += raise_amount
                self.current_bet = raise_amount
                player.update_score(-raise_amount)
            else:
                print("Raise must be greater than current bet")
                self._play_human_turn(player)
                
    def _play_ai_turn(self, player: PlayerState) -> None:
        """Handle AI player's turn"""
        hand_value = self.evaluate_hand(player)
        
        if hand_value >= PokerHand.THREE_OF_A_KIND:
            # Strong hand - raise
            raise_amount = self.current_bet + 10
            self.pot += raise_amount
            self.current_bet = raise_amount
            player.update_score(-raise_amount)
        elif hand_value >= PokerHand.PAIR:
            # Medium hand - call
            call_amount = self.current_bet - player.get_score()
            self.pot += call_amount
            player.update_score(-call_amount)
        else:
            # Weak hand - fold
            self.game_state._players.remove(player)
            
    def _advance_betting_round(self) -> None:
        """Deal community cards based on betting round"""
        if self.betting_round == 0:  # Deal flop
            self.deal_community_cards(3)
        elif self.betting_round in [1, 2]:  # Deal turn or river
            self.deal_community_cards(1)
        self.betting_round += 1
        
    def check_win_condition(self) -> Optional[PlayerState]:
        """Check for a winner - typically after all betting rounds"""
        if len(self.game_state.get_players()) == 1:
            winner = self.game_state.get_players()[0]
            winner.update_score(self.pot)
            return winner
            
        # Compare hands of remaining players
        best_hand = -1
        winner = None
        
        for player in self.game_state.get_players():
            hand_value = self.evaluate_hand(player)
            if hand_value > best_hand:
                best_hand = hand_value
                winner = player
                
        if winner:
            winner.update_score(self.pot)
            
        return winner