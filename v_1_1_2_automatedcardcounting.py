import random
import logging
import unittest
from dataclasses import dataclass


# Setup logging for debugging and information output
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')


@dataclass(frozen=True)
class Card:
   __slots__ = ('suit', 'rank')
   suit: str
   rank: str

   def __str__(self):
       return f"{self.rank} of {self.suit}"

   def __format__(self, format_spec):
       return format(str(self), format_spec)


class Deck:
   suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
   ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
   
   def __init__(self, num_decks=1, reshuffle_threshold=0.25):
       self.num_decks = num_decks
       self.reshuffle_threshold = reshuffle_threshold
       self._initial_deck_size = 52 * num_decks
       self.cards = self._create_deck()
       self.shuffle()

   def _create_deck(self):
       return [Card(suit, rank)
               for _ in range(self.num_decks)
               for suit in self.suits
               for rank in self.ranks]

   def shuffle(self):
       random.shuffle(self.cards)

   def reshuffle_if_needed(self):
       if len(self.cards) < self.reshuffle_threshold * self._initial_deck_size:
           logging.info("Reshuffling deck as threshold reached.")
           self.cards = self._create_deck()
           self.shuffle()
           return True
       return False

   def deal_card(self):
       if not self.cards:
           raise ValueError("No cards left in the deck!")
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



def simulate_deal(num_decks=1, total_deals=100):
    deck = Deck(num_decks=num_decks, reshuffle_threshold=0.25)
    counter = CardCounter(num_decks=num_decks)
    deals = 0

    while deals < total_deals:
        user_input = input(f"Press Enter to deal round {deals + 1} or type 'q' to quit: ")

        if user_input.lower() == "q":
            print("Exiting program...")
            break
       
        try:
            card = deck.deal_card()

        except ValueError as e:
            logging.error(e)
            break

        counter.update_count(card)
        deals += 1

        remaining_cards = len(deck.cards)
        current_true_count = counter.true_count(remaining_cards)
        logging.info(f"Dealt: {card:20} | Running Count: {counter.running_count:3} | True Count: {current_true_count:5.2f}")

        if deck.reshuffle_if_needed():
            counter.reset()
            logging.info("Counter reset after reshuffle.")

    logging.info(f"Simulation complete. Total deals: {deals}. Final Running Count: {counter.running_count}")
    return counter.running_count, counter.cards_dealt


class TestCardCounting(unittest.TestCase):
   def test_update_count(self):
       counter = CardCounter()
       card1 = Card("Hearts", "5")
       counter.update_count(card1)
       self.assertEqual(counter.running_count, 1)
       card2 = Card("Spades", "King")
       counter.update_count(card2)
       self.assertEqual(counter.running_count, 0)
       card3 = Card("Clubs", "8")
       counter.update_count(card3)
       self.assertEqual(counter.running_count, 0)

   def test_true_count(self):
       counter = CardCounter()
       counter.update_count(Card("Diamonds", "3"))
       counter.update_count(Card("Diamonds", "4"))
       self.assertAlmostEqual(counter.true_count(40), counter.running_count / (40 / 52))

   def test_deck_reshuffle(self):
       deck = Deck(num_decks=1, reshuffle_threshold=0.5)
       initial_size = len(deck.cards)
       for _ in range(int(initial_size * 0.6)):
           deck.deal_card()
       reshuffled = deck.reshuffle_if_needed()
       self.assertTrue(reshuffled)
       self.assertEqual(len(deck.cards), 52)

   def test_deal_card_error(self):
       deck = Deck(num_decks=1)
       for _ in range(52):
           deck.deal_card()
       with self.assertRaises(ValueError):
           deck.deal_card()


if __name__ == "__main__":
   import sys
   if len(sys.argv) > 1 and sys.argv[1] == "test":
       unittest.main(argv=[sys.argv[0]])
   else:
       simulate_deal(num_decks=1, total_deals=100)
