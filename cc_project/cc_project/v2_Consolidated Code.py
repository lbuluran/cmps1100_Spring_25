#Consolidated Code
import random
import matplotlib.pyplot as plt
from collections import deque
from dataclasses import dataclass

# Card values for Hi-Lo counting system
HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Standard 52-card deck
DECK = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4

@dataclass
class Card:
    suit: str
    rank: str

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.cards = []
        for _ in range(num_decks):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

class CardCounter:
    def __init__(self, num_decks=1):
        self.running_count = 0
        self.num_decks = num_decks
        self.cards_dealt = 0

    def update_count(self, card: Card):
        if card.rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif card.rank in ['10', 'Jack', 'Queen', 'King', 'Ace']:
            self.running_count -= 1
        self.cards_dealt += 1

    def true_count(self, remaining_cards: int) -> float:
        remaining_decks = remaining_cards / 52.0
        if remaining_decks == 0:
            return self.running_count
        return self.running_count / remaining_decks

    def reset(self):
        self.running_count = 0
        self.cards_dealt = 0


def get_true_count(running_count, decks_remaining):
    return round(running_count / decks_remaining, 2) if decks_remaining > 0 else running_count


def plot_accuracy(attempts, window_size=10):
    plt.figure(figsize=(10, 6))
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
    
    plt.savefig("counting_accuracy.png")
    plt.close()


def tutorial_mode(deck_count=1):
    deck = DECK * deck_count
    random.shuffle(deck)
    running_count = 0
    cards_seen = 0
    total_cards = len(deck)
    decks_remaining = deck_count
    attempts = []

    print("Welcome to the Blackjack Card Counting Tutorial!")
    print("We will go through each card one by one. Enter the correct count after each card.")
    print("Press 'q' to quit the tutorial.\n")

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
        if len(attempts) % 1 == 0:
            plot_accuracy(attempts)
            current_accuracy = sum(attempts[-10:]) / min(10, len(attempts)) * 100
            print(f"Your recent accuracy: {current_accuracy:.1f}%")

    print("Tutorial complete! You've gone through the deck.")
    
    if attempts:
        plot_accuracy(attempts)
        final_accuracy = sum(attempts) / len(attempts) * 100
        print(f"\nFinal Statistics:")
        print(f"Total attempts: {len(attempts)}")
        print(f"Overall accuracy: {final_accuracy:.1f}%")


def automated_mode(num_decks=1):
    deck = Deck(num_decks=num_decks)
    counter = CardCounter(num_decks=num_decks)
    
    print("Starting Automated Card Counting (Hi-Lo System)...\n")
    
    while len(deck.cards) > 0:
        card = deck.deal_card()
        counter.update_count(card)
        remaining_cards = len(deck.cards)
        current_true_count = counter.true_count(remaining_cards)
        print(f"Dealt {str(card):20} | Running Count: {counter.running_count:3} | True Count: {current_true_count:5.2f}")

    print("\nFinal Running Count:", counter.running_count)


def main():
    print("Welcome to Blackjack Card Counting!")
    print("Select a mode:")
    print("1. Tutorial Mode")
    print("2. Automated Mode")
    mode = input("Enter the number of the mode you want to play: ")

    if mode == '1':
        tutorial_mode(deck_count=1)
    elif mode == '2':
        automated_mode(num_decks=1)
    else:
        print("Invalid choice! Exiting the program.")

if __name__ == "__main__":
    main()
