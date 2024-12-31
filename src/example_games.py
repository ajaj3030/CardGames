from games.poker import Poker
from games.blackjack import Blackjack
from games.rummy import Rummy

def main():
    # Example usage of each game
    
    # Poker with 4 players (1 human + 3 AI)
    poker_game = Poker(4)
    
    # Blackjack with 3 players (1 human + 2 AI)
    blackjack_game = Blackjack(3)
    
    # Rummy with 4 players (1 human + 3 AI)
    rummy_game = Rummy(4)
    
    # You can now implement game loops for each game
    # For example, for Blackjack:
    while blackjack_game.game_state.get_phase() != GamePhase.COMPLETE:
        current_player = blackjack_game.game_state.get_current_player()
        blackjack_game.play_turn(current_player)
        
        if blackjack_game.check_win_condition():
            blackjack_game.game_state.set_phase(GamePhase.COMPLETE)
        else:
            blackjack_game.game_state.next_turn()

if __name__ == "__main__":
    main() 