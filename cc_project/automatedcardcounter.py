import random
from dataclasses import dataclass

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
        """
        Initializes the deck with the specified number of standard 52-card decks.
        """
        self.num_decks = num_decks
        self.cards = []
        for _ in range(num_decks):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deals one card from the deck. Returns None if the deck is empty."""
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

class CardCounter:
    """
    Implements the Hi-Lo card counting system.
    
    In the Hi-Lo system:
      - Cards 2 through 6 count as +1.
      - Cards 7 through 9 count as 0.
      - Cards 10, Jack, Queen, King, and Ace count as -1.
    
    The running count is updated each time a card is dealt. The true count is calculated
    by dividing the running count by the estimated number of remaining decks.
    """
    def __init__(self, num_decks=1):
        self.running_count = 0
        self.num_decks = num_decks
        self.cards_dealt = 0

    def update_count(self, card: Card):
        """
        Updates the running count based on the card dealt.
        """
        if card.rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif card.rank in ['10', 'Jack', 'Queen', 'King', 'Ace']:
            self.running_count -= 1
        # Cards 7, 8, and 9 do not affect the count.
        self.cards_dealt += 1

    def true_count(self, remaining_cards: int) -> float:
        """
        Calculates and returns the true count.
        The true count is the running count divided by the number of remaining decks.
        """
        # Each deck has 52 cards.
        remaining_decks = remaining_cards / 52.0
        if remaining_decks == 0:
            return self.running_count
        return self.running_count / remaining_decks

    def reset(self):
        """Resets the running count and cards dealt."""
        self.running_count = 0
        self.cards_dealt = 0

def main():
    num_decks = 1  # You can adjust the number of decks used.
    deck = Deck(num_decks=num_decks)
    counter = CardCounter(num_decks=num_decks)
    
    print("Starting Automated Card Counting (Hi-Lo System)...\n")
    
    # Continue dealing cards until the deck is empty.
    while len(deck.cards) > 0:
        card = deck.deal_card()
        counter.update_count(card)
        remaining_cards = len(deck.cards)
        current_true_count = counter.true_count(remaining_cards)
        print(f"Dealt {str(card):20} | Running Count: {counter.running_count:3} | True Count: {current_true_count:5.2f}")

    print("\nFinal Running Count:", counter.running_count)

if __name__ == "__main__":
    main()
