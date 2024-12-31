from typing import List, Optional
from ..models.card import Card
from ..models.player_action import PlayerAction, PlayerActionType
from ..models.player_state import PlayerState

class TerminalUI:
    @staticmethod
    def display_cards(cards: List[Card], hidden: bool = False) -> None:
        if hidden:
            print(" [Hidden Card]" * len(cards))
        else:
            print(" ".join(f"[{card.name}]" for card in cards))
            
    @staticmethod
    def display_poker_state(player: PlayerState, community_cards: List[Card], pot: int) -> None:
        print("\n" + "="*50)
        print(f"Current pot: ${pot}")
        print("Community cards:", end=" ")
        TerminalUI.display_cards(community_cards)
        print("\nYour hand:", end=" ")
        TerminalUI.display_cards(player.get_hand())
        print(f"Your score: ${player.get_score()}")
        
    @staticmethod
    def display_blackjack_state(player: PlayerState, dealer_hand: List[Card], 
                              dealer_hidden: bool = True) -> None:
        print("\n" + "="*50)
        print("Dealer's hand:", end=" ")
        if dealer_hidden:
            TerminalUI.display_cards([dealer_hand[0]])
            print(" [Hidden Card]")
        else:
            TerminalUI.display_cards(dealer_hand)
        print("\nYour hand:", end=" ")
        TerminalUI.display_cards(player.get_hand())
        
    @staticmethod
    def display_rummy_state(player: PlayerState, discard_pile: List[Card]) -> None:
        print("\n" + "="*50)
        print("Top of discard pile:", end=" ")
        if discard_pile:
            TerminalUI.display_cards([discard_pile[-1]])
        print("\nYour hand:", end=" ")
        TerminalUI.display_cards(player.get_hand())
        
    @staticmethod
    def get_poker_action() -> PlayerAction:
        print("\nAvailable actions:")
        print("1. Call")
        print("2. Raise")
        print("3. Fold")
        print("4. Quit")
        
        while True:
            choice = input("Your action (1-4): ")
            if choice == "1":
                return PlayerAction(PlayerActionType.CALL)
            elif choice == "2":
                try:
                    amount = int(input("Raise amount: $"))
                    return PlayerAction(PlayerActionType.RAISE, amount=amount)
                except ValueError:
                    print("Please enter a valid amount")
            elif choice == "3":
                return PlayerAction(PlayerActionType.FOLD)
            elif choice == "4":
                return PlayerAction(PlayerActionType.QUIT)
            else:
                print("Invalid choice")
                
    @staticmethod
    def get_blackjack_action() -> PlayerAction:
        print("\nAvailable actions:")
        print("1. Hit")
        print("2. Stand")
        print("3. Quit")
        
        while True:
            choice = input("Your action (1-3): ")
            if choice == "1":
                return PlayerAction(PlayerActionType.HIT)
            elif choice == "2":
                return PlayerAction(PlayerActionType.STAND)
            elif choice == "3":
                return PlayerAction(PlayerActionType.QUIT)
            else:
                print("Invalid choice")
                
    @staticmethod
    def get_rummy_action(player: PlayerState, can_draw_discard: bool = True) -> PlayerAction:
        print("\nAvailable actions:")
        print("1. Draw from deck")
        if can_draw_discard:
            print("2. Draw from discard pile")
        print("3. Discard a card")
        print("4. Declare set")
        print("5. Declare run")
        print("6. Quit")
        
        while True:
            choice = input("Your action (1-6): ")
            if choice == "1":
                return PlayerAction(PlayerActionType.DRAW_DECK)
            elif choice == "2" and can_draw_discard:
                return PlayerAction(PlayerActionType.DRAW_DISCARD)
            elif choice == "3":
                # Show cards with numbers
                hand = player.get_hand()
                for i, card in enumerate(hand, 1):
                    print(f"{i}. {card.name}")
                try:
                    card_idx = int(input("Choose card to discard (number): ")) - 1
                    if 0 <= card_idx < len(hand):
                        return PlayerAction(PlayerActionType.DISCARD, cards=[hand[card_idx]])
                    print("Invalid card number")
                except ValueError:
                    print("Please enter a valid number")
            elif choice == "4":
                # Select cards for set
                hand = player.get_hand()
                selected_cards = []
                print("\nSelect cards for set (enter card numbers, one at a time, 0 to finish):")
                for i, card in enumerate(hand, 1):
                    print(f"{i}. {card.name}")
                while True:
                    try:
                        card_idx = int(input("Card number (0 to finish): ")) - 1
                        if card_idx == -1:
                            break
                        if 0 <= card_idx < len(hand) and hand[card_idx] not in selected_cards:
                            selected_cards.append(hand[card_idx])
                    except ValueError:
                        print("Please enter a valid number")
                return PlayerAction(PlayerActionType.DECLARE_SET, cards=selected_cards)
            elif choice == "5":
                # Select cards for run
                hand = player.get_hand()
                selected_cards = []
                print("\nSelect cards for run (enter card numbers, one at a time, 0 to finish):")
                for i, card in enumerate(hand, 1):
                    print(f"{i}. {card.name}")
                while True:
                    try:
                        card_idx = int(input("Card number (0 to finish): ")) - 1
                        if card_idx == -1:
                            break
                        if 0 <= card_idx < len(hand) and hand[card_idx] not in selected_cards:
                            selected_cards.append(hand[card_idx])
                    except ValueError:
                        print("Please enter a valid number")
                return PlayerAction(PlayerActionType.DECLARE_RUN, cards=selected_cards)
            elif choice == "6":
                return PlayerAction(PlayerActionType.QUIT)
            else:
                print("Invalid choice") 

    @staticmethod
    def get_initial_bankroll() -> int:
        while True:
            try:
                amount = int(input("\nEnter initial bankroll for all players ($): "))
                if amount > 0:
                    return amount
                print("Please enter a positive amount")
            except ValueError:
                print("Please enter a valid number")

    @staticmethod
    def display_winner(winner: PlayerState, game_type: str, **kwargs) -> None:
        print(f"\n{winner.name} wins!")
        print(f"Winning hand:", end=" ")
        TerminalUI.display_cards(winner.get_hand())
        
        if game_type == "Poker":
            print(f"Community cards:", end=" ")
            TerminalUI.display_cards(kwargs.get('community_cards', []))
            print(f"Final pot: ${kwargs.get('pot', 0)}")
            print(f"Remaining bankroll: ${winner.get_bankroll()}")
        elif game_type == "Blackjack":
            print(f"Dealer's hand:", end=" ")
            TerminalUI.display_cards(kwargs.get('dealer_hand', []))
            print(f"Hand value: {kwargs.get('hand_value', 0)}") 