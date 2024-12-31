from typing import List, Dict, Optional
import pygame
from .game_view import GameView
from .pygame_ui import PygameUI
from ..models.player_action import PlayerAction, PlayerActionType
from ..models.player_state import PlayerState
from ..models.card import Card

class RummyView(GameView):
    def __init__(self, ui: PygameUI):
        super().__init__(ui)
        
        # Define button rectangles
        self.buttons = {
            'draw_deck': pygame.Rect(50, 650, 120, 40),
            'draw_discard': pygame.Rect(190, 650, 140, 40),
            'discard': pygame.Rect(350, 650, 100, 40),
            'declare_set': pygame.Rect(470, 650, 120, 40),
            'declare_run': pygame.Rect(610, 650, 120, 40),
        }
        
        self.selected_cards: List[Card] = []
        self.card_rects: Dict[str, pygame.Rect] = {}  # Map card IDs to their rectangles
        
    def draw_discard_pile(self, discard_pile: List[Card]) -> None:
        """Draw the discard pile"""
        self.ui.draw_text("Discard Pile:", (50, 50))
        if discard_pile:
            self.ui.draw_card(discard_pile[-1], (50, 100))
            
    def draw_deck(self) -> None:
        """Draw the deck"""
        self.ui.draw_text("Deck:", (200, 50))
        # Draw face-down card representing the deck
        self.ui.draw_card(None, (200, 100), face_up=False)
        
    def draw_player_hand(self, player: PlayerState) -> None:
        """Draw player's hand with selectable cards"""
        self.ui.draw_text(f"{player.name}'s Hand:", (50, 300))
        self.card_rects.clear()
        
        for i, card in enumerate(player.get_hand()):
            pos = (50 + i * 80, 350)
            rect = pygame.Rect(pos[0], pos[1], 71, 96)  # Standard card size
            self.card_rects[card.id] = rect
            
            # Draw highlight for selected cards
            if card in self.selected_cards:
                pygame.draw.rect(self.ui.screen, PygameUI.BLUE, rect, 3)
                
            self.ui.draw_card(card, pos)
            
    def draw(self, game_state: dict) -> None:
        """Draw the rummy game state"""
        self.ui.screen.fill(PygameUI.GREEN)
        
        # Draw discard pile and deck
        self.draw_discard_pile(game_state['discard_pile'])
        self.draw_deck()
        
        # Draw player's hand
        self.draw_player_hand(game_state['player'])
        
        # Draw buttons
        for text, rect in self.buttons.items():
            if text == 'draw_discard' and not game_state['can_draw_discard']:
                continue
            button_text = text.replace('_', ' ').capitalize()
            self.ui.draw_button(button_text, rect)
            
        pygame.display.flip()
        
    def handle_click(self, pos: tuple) -> Optional[PlayerAction]:
        """Handle mouse clicks"""
        # Check card clicks for selection
        for card_id, rect in self.card_rects.items():
            if rect.collidepoint(pos):
                card = next((c for c in self.game_state['player'].get_hand() if c.id == card_id), None)
                if card:
                    if card in self.selected_cards:
                        self.selected_cards.remove(card)
                    else:
                        self.selected_cards.append(card)
                    return None
        
        # Check button clicks
        for action, rect in self.buttons.items():
            if self.ui.is_button_clicked(rect, pos):
                if action == 'draw_deck':
                    return PlayerAction(PlayerActionType.DRAW_DECK)
                elif action == 'draw_discard':
                    return PlayerAction(PlayerActionType.DRAW_DISCARD)
                elif action == 'discard':
                    if len(self.selected_cards) == 1:
                        action = PlayerAction(PlayerActionType.DISCARD, cards=self.selected_cards.copy())
                        self.selected_cards.clear()
                        return action
                elif action == 'declare_set':
                    if len(self.selected_cards) >= 3:
                        action = PlayerAction(PlayerActionType.DECLARE_SET, cards=self.selected_cards.copy())
                        self.selected_cards.clear()
                        return action
                elif action == 'declare_run':
                    if len(self.selected_cards) >= 3:
                        action = PlayerAction(PlayerActionType.DECLARE_RUN, cards=self.selected_cards.copy())
                        self.selected_cards.clear()
                        return action
        return None 