from src.games.poker import Poker
from src.games.blackjack import Blackjack
from src.games.rummy import Rummy
from src.models.game_state import GamePhase
from src.ui.terminal_ui import TerminalUI

def get_game_choice() -> str:
    print("\nAvailable games:")
    print("1. Poker")
    print("2. Blackjack") 
    print("3. Rummy")
    
    while True:
        choice = input("\nWhich game would you like to play? (1-3): ")
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def get_num_players(game_type: str) -> int:
    max_players = {
        '1': 10,  # Poker
        '2': 7,   # Blackjack
        '3': 6    # Rummy
    }
    
    while True:
        try:
            num = int(input(f"\nHow many players? (2-{max_players[game_type]}): "))
            if 2 <= num <= max_players[game_type]:
                return num
            print(f"Please enter a number between 2 and {max_players[game_type]}")
        except ValueError:
            print("Please enter a valid number")

def main():
    while True:
        game_choice = get_game_choice()
        if game_choice.lower() == 'q':
            break
            
        num_players = get_num_players(game_choice)
        
        # Initialize the chosen game
        if game_choice == '1':
            game = Poker(num_players)
            print("\nStarting Poker game...")
        elif game_choice == '2':
            game = Blackjack(num_players)
            print("\nStarting Blackjack game...")
        else:
            game = Rummy(num_players)
            print("\nStarting Rummy game...")
        
        # Game loop
        try:
            while game.game_state.get_phase() != GamePhase.COMPLETE:
                current_player = game.game_state.get_current_player()
                game.play_turn(current_player)
                
                winner = game.check_win_condition()
                if winner:
                    print(f"\nGame Over! {winner.name} wins!")
                    game.game_state.set_phase(GamePhase.COMPLETE)
                else:
                    game.game_state.next_turn()
        except KeyboardInterrupt:
            print("\nGame interrupted!")
            
        play_again = input("\nPlay another game? (y/n): ")
        if play_again.lower() != 'y':
            break

if __name__ == "__main__":
    main()