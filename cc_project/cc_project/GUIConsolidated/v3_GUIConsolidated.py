import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from dataclasses import dataclass
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


# GUI code with Tkinter
class CardCountingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Card Counting")
        self.root.geometry("800x600")

        # Initialize deck and card counter
        self.deck = Deck(num_decks=1)
        self.counter = CardCounter(num_decks=1)
        self.running_count = 0
        self.attempts = []

        # Create canvas to display cards
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="lightgray")
        self.canvas.pack()

        # Create label for displaying running count and true count
        self.running_count_label = tk.Label(self.root, text="Running Count: 0", font=('Arial', 14))
        self.running_count_label.pack()

        self.true_count_label = tk.Label(self.root, text="True Count: 0.00", font=('Arial', 14))
        self.true_count_label.pack()

        # Buttons for choosing the mode
        self.tutorial_button = tk.Button(self.root, text="Start Tutorial Mode", width=20, command=self.start_tutorial_mode)
        self.tutorial_button.pack()

        self.automated_button = tk.Button(self.root, text="Start Automated Mode", width=20, command=self.start_automated_mode)
        self.automated_button.pack()

        # Initialize the card image as a canvas item
        self.card_image_item = None

    def start_tutorial_mode(self):
        self.counter.reset()
        self.deck.shuffle()
        self.attempts = []
        self.display_card()

    def start_automated_mode(self):
        self.counter.reset()
        self.deck.shuffle()
        self.display_card()

    def display_card(self):
        if len(self.deck.cards) == 0:
            messagebox.showinfo("Game Over", "The deck is empty.")
            return

        card = self.deck.deal_card()
        self.counter.update_count(card)
        remaining_cards = len(self.deck.cards)
        true_count = self.counter.true_count(remaining_cards)

        # Display card image (assuming the images are in a folder named 'cards' and are named by rank_suit.png)
        card_image = Image.open(f"cards/{card.rank}_{card.suit}.png")
        card_image = card_image.resize((100, 150))
        card_photo = ImageTk.PhotoImage(card_image)

        # If there's no existing card, create it on the canvas
        if self.card_image_item is None:
            self.card_image_item = self.canvas.create_image(50, 100, image=card_photo)
        else:
            # Update the image source of the existing card
            self.canvas.itemconfig(self.card_image_item, image=card_photo)

        # Store the reference to the image to avoid it being garbage collected
        self.canvas.image = card_photo

        # Update running count and true count labels
        self.running_count_label.config(text=f"Running Count: {self.counter.running_count}")
        self.true_count_label.config(text=f"True Count: {true_count:.2f}")

        # Animate card drawing by moving it on the canvas
        for i in range(0, 200, 10):
            self.canvas.coords(self.card_image_item, 50 + i, 100)
            self.root.update()

        self.root.after(500, self.display_card)

def main():
    root = tk.Tk()
    app = CardCountingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
