import pygame
import os
from typing import List, Tuple, Dict, Optional
from ..models.card import Card

class PygameUI:
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    
    def __init__(self, width: int = 1024, height: int = 768):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Card Game Engine")
        
        # Load card images
        self.card_images: Dict[str, pygame.Surface] = {}
        self.card_back = self._load_image("card_back.png")
        self._load_card_images()
        
        # Set up font
        self.font = pygame.font.Font(None, 36)
        
    def _load_image(self, filename: str) -> pygame.Surface:
        """Load an image from the assets directory"""
        path = os.path.join("assets", filename)
        return pygame.image.load(path)
        
    def _load_card_images(self) -> None:
        """Load all card images"""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = list(range(1, 14))  # 1-13
        
        for suit in suits:
            for rank in ranks:
                key = f"{suit}-{rank}"
                filename = f"card_{suit.lower()}_{rank}.png"
                self.card_images[key] = self._load_image(filename)
                
    def draw_card(self, card: Card, pos: Tuple[int, int], face_up: bool = True) -> None:
        """Draw a card at the specified position"""
        if face_up:
            card_image = self.card_images.get(f"{card.suit}-{card.rank}", self.card_back)
        else:
            card_image = self.card_back
        self.screen.blit(card_image, pos)
        
    def draw_text(self, text: str, pos: Tuple[int, int], color: Tuple[int, int, int] = WHITE) -> None:
        """Draw text at the specified position"""
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, pos)
        
    def draw_button(self, text: str, rect: pygame.Rect, color: Tuple[int, int, int] = BLUE) -> None:
        """Draw a button with text"""
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def is_button_clicked(self, rect: pygame.Rect, pos: Tuple[int, int]) -> bool:
        """Check if a button was clicked"""
        return rect.collidepoint(pos) 