from src.games.poker import Poker
from src.games.blackjack import Blackjack
from src.games.rummy import Rummy
from src.models.game_state import GamePhase
from src.ui.terminal_ui import TerminalUI
from src.ui.pygame_ui import PygameUI
from src.ui.poker_view import PokerView
from src.ui.blackjack_view import BlackjackView
from src.ui.rummy_view import RummyView
from src.models.player_action import PlayerActionType
import pygame

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

def play_poker_gui(num_players: int, initial_bankroll: int) -> None:
    ui = PygameUI()
    view = PokerView(ui)
    game = Poker(num_players, initial_bankroll)
    
    while view.running:
        current_player = game.game_state.get_current_player()
        
        if current_player.id == 'p0':  # Human player
            game_state = {
                'community_cards': game.community_cards,
                'pot': game.pot,
                'current_bet': game.current_bet,
                'player': current_player
            }
            
            action = view.run_frame(game_state)
            if action:
                if action.action_type == PlayerActionType.QUIT:
                    break
                game.play_turn(current_player, action)
        else:
            game._play_ai_turn(current_player)
            
        winner = game.check_win_condition()
        if winner and len([p for p in game.game_state.get_players() if p.get_bankroll() > 0]) <= 1:
            # Only quit if someone has won all the money
            break
            
    pygame.quit()

def play_blackjack_gui(num_players: int) -> None:
    ui = PygameUI()
    view = BlackjackView(ui)
    game = Blackjack(num_players)
    
    while view.running:
        current_player = game.game_state.get_current_player()
        
        if current_player.id == 'p0':  # Human player
            game_state = {
                'dealer_hand': game.dealer_hand,
                'hide_hole_card': True,
                'player': current_player,
                'hand_value': game.calculate_hand_value(current_player.get_hand())
            }
            
            action = view.run_frame(game_state)
            if action:
                if action.action_type == PlayerActionType.QUIT:
                    break
                game.play_turn(current_player)
        else:
            game._play_ai_turn(current_player)
            
        winner = game.check_win_condition()
        if winner:
            # Show final hands
            game_state = {
                'dealer_hand': game.dealer_hand,
                'hide_hole_card': False,
                'player': winner,
                'hand_value': game.calculate_hand_value(winner.get_hand())
            }
            view.draw(game_state)
            pygame.time.wait(3000)  # Show final state for 3 seconds
            # Reset for next round instead of ending
            game = Blackjack(num_players)
            
    pygame.quit()

def play_rummy_gui(num_players: int) -> None:
    ui = PygameUI()
    view = RummyView(ui)
    game = Rummy(num_players)
    
    while view.running:
        current_player = game.game_state.get_current_player()
        
        if current_player.id == 'p0':  # Human player
            game_state = {
                'discard_pile': game.discard_pile,
                'player': current_player,
                'can_draw_discard': not game.has_drawn
            }
            
            action = view.run_frame(game_state)
            if action:
                if action.action_type == PlayerActionType.QUIT:
                    break
                game.play_turn(current_player)
        else:
            game._play_ai_turn(current_player)
            
        winner = game.check_win_condition()
        if winner:
            # Show winner state
            view.draw(game_state)
            pygame.time.wait(3000)  # Show final state for 3 seconds
            # Reset for next round instead of ending
            game = Rummy(num_players)
            
    pygame.quit()

def main():
    while True:
        game_choice = get_game_choice()
        if game_choice.lower() == 'q':
            break
            
        num_players = get_num_players(game_choice)
        
        if game_choice == '1':  # Poker
            initial_bankroll = TerminalUI.get_initial_bankroll()
            play_poker_gui(num_players, initial_bankroll)
        elif game_choice == '2':  # Blackjack
            play_blackjack_gui(num_players)
        else:  # Rummy
            play_rummy_gui(num_players)
            
        play_again = input("\nPlay another game? (y/n): ")
        if play_again.lower() != 'y':
            break

if __name__ == "__main__":
    main()