from typing import List, Dict, Optional
import pygame
from .game_view import GameView
from .pygame_ui import PygameUI
from ..models.player_action import PlayerAction, PlayerActionType
from ..models.player_state import PlayerState
from ..models.card import Card

class PokerView(GameView):
    def __init__(self, ui: PygameUI):
        super().__init__(ui)
        
        # Define button rectangles
        self.buttons = {
            'call': pygame.Rect(50, 650, 100, 40),
            'raise': pygame.Rect(170, 650, 100, 40),
            'fold': pygame.Rect(290, 650, 100, 40),
        }
        
        self.raise_amount = 0
        self.showing_raise_input = False
        
    def draw_player_info(self, player: PlayerState, pos: tuple) -> None:
        """Draw player information"""
        self.ui.draw_text(f"{player.name}: ${player.get_bankroll()}", pos)
        
    def draw_community_cards(self, cards: List[Card]) -> None:
        """Draw community cards"""
        for i, card in enumerate(cards):
            self.ui.draw_card(card, (250 + i * 80, 300))
            
    def draw_player_hand(self, cards: List[Card], pos: tuple) -> None:
        """Draw player's hand"""
        for i, card in enumerate(cards):
            self.ui.draw_card(card, (pos[0] + i * 80, pos[1]))
            
    def draw(self, game_state: dict) -> None:
        """Draw the poker game state"""
        self.ui.screen.fill(PygameUI.GREEN)
        
        # Draw community cards
        self.ui.draw_text("Community Cards:", (250, 250))
        self.draw_community_cards(game_state['community_cards'])
        
        # Draw pot
        self.ui.draw_text(f"Pot: ${game_state['pot']}", (450, 200))
        
        # Draw player's hand
        self.ui.draw_text("Your Hand:", (50, 500))
        self.draw_player_hand(game_state['player'].get_hand(), (50, 550))
        
        # Draw current bet
        self.ui.draw_text(f"Current Bet: ${game_state['current_bet']}", (50, 450))
        
        # Draw buttons
        for text, rect in self.buttons.items():
            self.ui.draw_button(text.capitalize(), rect)
            
        if self.showing_raise_input:
            self.ui.draw_text(f"Raise Amount: ${self.raise_amount}", (400, 650))
            
        pygame.display.flip()
        
    def handle_click(self, pos: tuple) -> Optional[PlayerAction]:
        """Handle mouse clicks"""
        for action, rect in self.buttons.items():
            if self.ui.is_button_clicked(rect, pos):
                if action == 'call':
                    return PlayerAction(PlayerActionType.CALL)
                elif action == 'fold':
                    return PlayerAction(PlayerActionType.FOLD)
                elif action == 'raise':
                    self.showing_raise_input = True
                    return None
                    
        return None
        
    def handle_events(self) -> Optional[PlayerAction]:
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.handle_click(event.pos)
            if event.type == pygame.KEYDOWN and self.showing_raise_input:
                if event.key == pygame.K_RETURN:
                    self.showing_raise_input = False
                    return PlayerAction(PlayerActionType.RAISE, amount=self.raise_amount)
                elif event.key == pygame.K_BACKSPACE:
                    self.raise_amount = self.raise_amount // 10
                elif event.unicode.isdigit():
                    self.raise_amount = self.raise_amount * 10 + int(event.unicode)
                    
        return None 