from typing import List, Dict, Optional
import pygame
from .game_view import GameView
from .pygame_ui import PygameUI
from ..models.player_action import PlayerAction, PlayerActionType
from ..models.player_state import PlayerState
from ..models.card import Card

class BlackjackView(GameView):
    def __init__(self, ui: PygameUI):
        super().__init__(ui)
        
        # Define button rectangles
        self.buttons = {
            'hit': pygame.Rect(50, 650, 100, 40),
            'stand': pygame.Rect(170, 650, 100, 40),
        }
        
    def draw_dealer_hand(self, dealer_hand: List[Card], hide_hole_card: bool = True) -> None:
        """Draw dealer's hand"""
        self.ui.draw_text("Dealer's Hand:", (50, 50))
        # Show first card
        self.ui.draw_card(dealer_hand[0], (50, 100))
        # Hide second card (hole card) if required
        if len(dealer_hand) > 1:
            for i, card in enumerate(dealer_hand[1:], 1):
                self.ui.draw_card(card, (50 + i * 80, 100), face_up=not hide_hole_card)
                
    def draw_player_hand(self, player: PlayerState, hand_value: int) -> None:
        """Draw player's hand"""
        self.ui.draw_text(f"{player.name}'s Hand (Value: {hand_value}):", (50, 300))
        for i, card in enumerate(player.get_hand()):
            self.ui.draw_card(card, (50 + i * 80, 350))
            
    def draw(self, game_state: dict) -> None:
        """Draw the blackjack game state"""
        self.ui.screen.fill(PygameUI.GREEN)
        
        # Draw dealer's hand
        self.draw_dealer_hand(game_state['dealer_hand'], game_state['hide_hole_card'])
        
        # Draw player's hand
        self.draw_player_hand(game_state['player'], game_state['hand_value'])
        
        # Draw buttons
        for text, rect in self.buttons.items():
            self.ui.draw_button(text.capitalize(), rect)
            
        pygame.display.flip()
        
    def handle_click(self, pos: tuple) -> Optional[PlayerAction]:
        """Handle mouse clicks"""
        for action, rect in self.buttons.items():
            if self.ui.is_button_clicked(rect, pos):
                if action == 'hit':
                    return PlayerAction(PlayerActionType.HIT)
                elif action == 'stand':
                    return PlayerAction(PlayerActionType.STAND)
        return None 