import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Importing the classes from the main script
from __main__ import CardCountingGUI, Deck, CardCounter

class TestCardCountingGUI(unittest.TestCase):

    @patch('tkinter.Tk')  # Mock Tkinter root window
    def test_gui_initialization(self, mock_tk):
        root = MagicMock()  # Mocking the Tk root window
        app = CardCountingGUI(root)
        self.assertIsNotNone(app.root)
        self.assertIsNotNone(app.canvas)
        self.assertIsNotNone(app.running_count_label)
        self.assertIsNotNone(app.true_count_label)

    @patch('tkinter.messagebox.showinfo')  # Mock messagebox
    @patch.object(CardCountingGUI, 'display_card', return_value=None)
    def test_start_tutorial_mode(self, mock_display, mock_messagebox):
        root = MagicMock()  # Mocking the Tk root window
        app = CardCountingGUI(root)
        app.start_tutorial_mode()
        self.assertEqual(app.mode, "tutorial")
        self.assertTrue(mock_display.called)

    @patch('tkinter.messagebox.showinfo')  # Mock messagebox
    @patch.object(CardCountingGUI, 'display_card', return_value=None)
    def test_start_automated_mode(self, mock_display, mock_messagebox):
        root = MagicMock()  # Mocking the Tk root window
        app = CardCountingGUI(root)
        app.start_automated_mode()
        self.assertEqual(app.mode, "automated")
        self.assertTrue(mock_display.called)

    @patch('tkinter.messagebox.showinfo')  # Mock messagebox to avoid popups
    def test_check_guess_correct(self, mock_messagebox):
        root = MagicMock()  # Mocking the Tk root window
        app = CardCountingGUI(root)
        app.start_tutorial_mode()

        # Mock the user entering the correct guess (Running count = 0)
        app.counter.running_count = 0  # Correct guess
        with patch('builtins.input', return_value='0'):  # Simulate user typing '0' in the input field
            app.check_guess()
        mock_messagebox.assert_called_with("Correct Guess", "✅ Correct! The count is updated.")

    @patch('tkinter.messagebox.showinfo')  # Mock messagebox to avoid popups
    def test_check_guess_incorrect(self, mock_messagebox):
        root = MagicMock()  # Mocking the Tk root window
        app = CardCountingGUI(root)
        app.start_tutorial_mode()

        # Mock the user entering the incorrect guess (Running count = 0 but user enters '1')
        app.counter.running_count = 0  # Correct guess would be 0
        with patch('builtins.input', return_value='1'):  # Simulate user typing '1' in the input field
            app.check_guess()
        mock_messagebox.assert_called_with("Incorrect Guess", "❌ Incorrect. The correct running count is 0.")

    @patch('tkinter.messagebox.showinfo')  # Mock messagebox to avoid popups
    @patch.object(CardCountingGUI, 'display_card', return_value=None)
    def test_deal_card_automated_mode(self, mock_display, mock_messagebox):
        root = MagicMock()  # Mocking the Tk root window
        app = CardCountingGUI(root)
        app.start_automated_mode()

        # Simulate pressing Enter to deal the next card in automated mode
        app.handle_enter_key()
        self.assertTrue(mock_display.called)

    @patch('tkinter.messagebox.showinfo')  # Mock messagebox to avoid popups
    @patch.object(CardCountingGUI, 'display_card', return_value=None)
    def test_deal_card_tutorial_mode(self, mock_display, mock_messagebox):
        root = MagicMock()  # Mocking the Tk root window
        app = CardCountingGUI(root)
        app.start_tutorial_mode()

        # Simulate pressing Enter to move to the next card
        app.handle_enter_key()
        self.assertTrue(mock_display.called)

    @patch('tkinter.messagebox.showinfo')  # Mock messagebox to avoid popups
    def test_quit_program(self, mock_messagebox):
        root = MagicMock()  # Mocking the Tk root window
        app = CardCountingGUI(root)

        with patch('builtins.input', return_value='q'):  # Simulate the user pressing 'q' to quit
            app.quit_program()
        mock_messagebox.assert_called_with("Game Over", "The deck is empty.")  # Simulate game over message

if __name__ == "__main__":
    unittest.main(exit=False)  # Prevent unittest from closing the program
