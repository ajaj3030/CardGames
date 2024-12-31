# Card Game Engine

A Python-based card game engine with graphical interface supporting multiple classic card games. Currently implements Poker, Blackjack, and Rummy with both human and AI players.

## Features

- **Multiple Games Support**
  - Texas Hold'em Poker
  - Blackjack
  - Rummy

- **Graphical Interface**
  - Built with Pygame
  - Intuitive card visualization
  - Interactive buttons for game actions
  - Card selection for Rummy

- **Game Features**
  - AI opponents
  - Multiple players (2-10 depending on the game)
  - Continuous play with multiple rounds
  - Bankroll management for Poker
  - Standard 52-card deck

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Game\ Engine
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Games

Run the main game script:
```bash
python src/example_games.py
```

Choose your game and follow the prompts to:
1. Select number of players
2. Set initial bankroll (for Poker)
3. Start playing!

## Game Controls

### Poker
- **Call**: Match the current bet
- **Raise**: Increase the bet (type amount and press Enter)
- **Fold**: Give up your hand
- **Quit**: End the game

### Blackjack
- **Hit**: Draw another card
- **Stand**: Keep your current hand
- **Quit**: End the game

### Rummy
- **Draw Deck**: Draw a card from the deck
- **Draw Discard**: Take the top card from the discard pile
- **Discard**: Discard a selected card
- **Declare Set**: Declare a set (3+ cards of same rank)
- **Declare Run**: Declare a run (3+ consecutive cards of same suit)
- **Quit**: End the game

Click cards to select/deselect them for actions in Rummy.

## Project Structure

```
Game Engine/
├── src/
│   ├── games/           # Game implementations
│   ├── models/          # Core game models
│   ├── ui/             # User interface components
│   └── utils/          # Utility functions
├── assets/             # Card images and resources
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Dependencies

- Python 3.10+
- Pygame 2.5.2
- Other dependencies listed in requirements.txt

## Game Rules

### Poker (Texas Hold'em)
- Each player gets 2 hole cards
- 5 community cards are dealt (flop, turn, river)
- Standard betting rounds
- Best 5-card hand wins
- Game ends when one player has all the money

### Blackjack
- Try to get closer to 21 than the dealer
- Face cards worth 10, Ace worth 1 or 11
- Dealer must hit on 16 and below
- Rounds continue until you quit

### Rummy
- Draw and discard cards to form sets and runs
- Sets: 3+ cards of same rank
- Runs: 3+ consecutive cards of same suit
- First to declare all cards in valid combinations wins
- Rounds continue until you quit

## Contributing

Feel free to open issues or submit pull requests for:
- Bug fixes
- New features
- Additional card games
- UI improvements
- Documentation updates

## License

This project is open source and available under the MIT License. 