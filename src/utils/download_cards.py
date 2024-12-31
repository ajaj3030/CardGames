import os
import urllib.request

def download_and_setup_cards():
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Base URL for raw GitHub content
    base_url = "https://raw.githubusercontent.com/hanhaechi/playing-cards/master"
    
    # Define card names
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    faces = ['A', 'J', 'Q', 'K']
    
    print("Downloading card images...")
    cards_processed = 0
    
    try:
        # Download card back
        print("Downloading card back...")
        urllib.request.urlretrieve(
            f"{base_url}/back_dark.png",
            os.path.join("assets", "card_back.png")
        )

        # Download all cards
        for suit in suits:
            # Download number cards
            for num in numbers:
                filename = f"{suit}_{num}.png"
                new_filename = f"card_{suit}_{num}.png"
                print(f"Downloading {filename}...")
                
                urllib.request.urlretrieve(
                    f"{base_url}/{filename}",
                    os.path.join("assets", new_filename)
                )
                cards_processed += 1
            
            # Download face cards
            for face in faces:
                filename = f"{suit}_{face}.png"
                # Convert face cards to numbers (A=1, J=11, Q=12, K=13)
                number = '1' if face == 'A' else str(10 + "JQK".index(face) + 11)
                new_filename = f"card_{suit}_{number}.png"
                print(f"Downloading {filename}...")
                
                urllib.request.urlretrieve(
                    f"{base_url}/{filename}",
                    os.path.join("assets", new_filename)
                )
                cards_processed += 1

        print(f"\nProcessed {cards_processed} cards")
        if cards_processed != 52:
            print(f"Warning: Expected 52 cards but processed {cards_processed}")
            
        print("Card setup complete! Images are in the assets folder.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    download_and_setup_cards() 