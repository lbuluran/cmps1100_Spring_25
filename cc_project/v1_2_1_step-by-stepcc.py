import random

# Card values for Hi-Lo counting system
HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Standard 52-card deck
DECK = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4


def get_true_count(running_count, decks_remaining):
    """Calculates the true count based on remaining decks."""
    return round(running_count / decks_remaining, 2) if decks_remaining > 0 else running_count


def tutorial_mode(deck_count=1):
    """Runs a step-by-step tutorial for card counting."""
    deck = DECK * deck_count  # Adjust for multiple decks
    random.shuffle(deck)
    running_count = 0
    cards_seen = 0
    total_cards = len(deck)
    decks_remaining = deck_count

    print("Welcome to the Blackjack Card Counting Tutorial!")
    print("We will go through each card one by one. Enter the correct count after each card.")
    print("Press 'q' to quit the tutorial at any time.\n")

    while deck:
        card = deck.pop(0)
        cards_seen += 1
        running_count += HI_LO_VALUES[card]
        decks_remaining = max(1, round((total_cards - cards_seen) / 52))  # Approximate decks left
        true_count = get_true_count(running_count, decks_remaining)

        print(f"Card drawn: {card}")
        user_input = input("Enter the running count: ")

        if user_input.lower() == 'q':
            print("Exiting tutorial. Thanks for playing!")
            break

        try:
            user_count = int(user_input)
            if user_count == running_count:
                print("✅ Correct! The count is updated.")
            else:
                print(f"❌ Incorrect. The correct running count is {running_count}.")
                print(f"Explanation: {card} has a value of {HI_LO_VALUES[card]}, so the new count is {running_count}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

        print(f"Current True Count: {true_count}\n")

    print("Tutorial complete! You’ve gone through the deck.")


if __name__ == "__main__":
    tutorial_mode(deck_count=1)


