import pygame
from typing import Optional, List, Dict
from .pygame_ui import PygameUI
from ..models.card import Card
from ..models.player_state import PlayerState
from ..models.player_action import PlayerAction

class GameView:
    def __init__(self, ui: PygameUI):
        self.ui = ui
        self.running = True
        self.clock = pygame.time.Clock()
        
    def handle_events(self) -> Optional[PlayerAction]:
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.handle_click(event.pos)
        return None
        
    def handle_click(self, pos: tuple) -> Optional[PlayerAction]:
        """Handle mouse clicks"""
        return None
        
    def draw(self, game_state: dict) -> None:
        """Draw the game state"""
        self.ui.screen.fill(PygameUI.GREEN)
        pygame.display.flip()
        
    def run_frame(self, game_state: dict) -> Optional[PlayerAction]:
        """Run one frame of the game"""
        action = self.handle_events()
        self.draw(game_state)
        self.clock.tick(60)
        return action 