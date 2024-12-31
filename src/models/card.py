from dataclasses import dataclass
from typing import Dict, List, Union

# Type aliases
CardAttributeValue = Union[int, str, bool]
CardAttributes = Dict[str, CardAttributeValue]

@dataclass
class CardEffect:
    effect_type: str
    value: int

@dataclass
class Card:
    id: str
    name: str
    suit: str
    rank: int
    type: str
    attributes: CardAttributes = None
    effects: List[CardEffect] = None

    def __post_init__(self):
        self.attributes = self.attributes or {}
        self.effects = self.effects or []

    def clone(self) -> 'Card':
        return Card(
            id=self.id,
            name=self.name,
            suit=self.suit,
            rank=self.rank,
            type=self.type,
            attributes=self.attributes.copy(),
            effects=self.effects.copy()
        ) 