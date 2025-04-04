import random
import matplotlib.pyplot as plt
from collections import deque

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


def plot_accuracy(attempts, window_size=10):
    """Plots the running accuracy of user's counting attempts."""
    plt.figure(figsize=(10, 6))
    
    # Calculate running accuracy
    correct_counts = [1 if result else 0 for result in attempts]
    running_accuracy = []
    window = deque(maxlen=window_size)
    
    for count in correct_counts:
        window.append(count)
        running_accuracy.append(sum(window) / len(window) * 100)
    
    plt.plot(range(1, len(running_accuracy) + 1), running_accuracy, 'b-', label='Running Accuracy')
    plt.axhline(y=100, color='g', linestyle='--', label='Perfect Accuracy')
    
    plt.title('Card Counting Accuracy Over Time')
    plt.xlabel('Number of Attempts')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    plt.savefig(f"plots\+counting_accuracy{len(attempts)}.png")
    plt.close()


def tutorial_mode(deck_count=1):
    """Runs a step-by-step tutorial for card counting."""
    deck = DECK * deck_count  # Adjust for multiple decks
    random.shuffle(deck)
    running_count = 0
    cards_seen = 0
    total_cards = len(deck)
    decks_remaining = deck_count
    attempts = []  # Track correct/incorrect attempts

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
            is_correct = user_count == running_count
            attempts.append(is_correct)
            
            if is_correct:
                print("✅ Correct! The count is updated.")
            else:
                print(f"❌ Incorrect. The correct running count is {running_count}.")
                print(f"Explanation: {card} has a value of {HI_LO_VALUES[card]}, so the new count is {running_count}.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            attempts.append(False)

        print(f"Current True Count: {true_count}\n")

        # Plot accuracy every attempt
        print(f"plots\counting_accuracy{len(attempts)}.png", f"plots\counting_accuracy{len(attempts)}.png")
        if len(attempts) % 1 == 0:
            plot_accuracy(attempts)
            current_accuracy = sum(attempts[-10:]) / min(10, len(attempts)) * 100
            print(f"Your recent accuracy: {current_accuracy:.1f}%")

    print("Tutorial complete! You've gone through the deck.")
    
    # Final accuracy plot
    if attempts:
        plot_accuracy(attempts)
        final_accuracy = sum(attempts) / len(attempts) * 100
        print(f"\nFinal Statistics:")
        print(f"Total attempts: {len(attempts)}")
        print(f"Overall accuracy: {final_accuracy:.1f}%")


if __name__ == "__main__":
    tutorial_mode(deck_count=1)