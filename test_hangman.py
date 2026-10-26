"""
Unit tests and verification for hangman.py
"""
import unittest
import hangman

class TestHangmanGame(unittest.TestCase):
    def test_word_list_scope(self):
        """Verify scope requirement: Exactly 5 predefined words"""
        self.assertEqual(len(hangman.WORD_COLLECTION), 5, "Word list must contain exactly 5 words.")
        for item in hangman.WORD_COLLECTION:
            self.assertIn("word", item)
            self.assertIn("category", item)
            self.assertIn("hint", item)
            self.assertTrue(item["word"].isupper(), "Words should be uppercase.")
            self.assertTrue(item["word"].isalpha(), "Words should be alphabetic.")

    def test_max_incorrect_guesses_scope(self):
        """Verify scope requirement: Limit incorrect guesses to 6"""
        self.assertEqual(hangman.MAX_INCORRECT_GUESSES, 6)

    def test_stages_count(self):
        """Verify stages from 0 to 6 mistakes (7 stages total)"""
        self.assertEqual(len(hangman.HANGMAN_STAGES), 7)

    def test_masked_word_display(self):
        """Verify masked word reveals only guessed letters"""
        secret = "PYTHON"
        guessed = ["P", "O"]
        masked = hangman.get_masked_word(secret, guessed)
        # Should contain P, O and underscores for Y, T, H, N
        self.assertIn("P", masked)
        self.assertIn("O", masked)
        self.assertIn("_", masked)

    def test_all_revealed_condition(self):
        """Verify win condition logic"""
        secret = "GALAXY"
        guessed = ["G", "A", "L", "X", "Y"]
        all_revealed = all(char in guessed for char in secret)
        self.assertTrue(all_revealed)

        guessed_partial = ["G", "A", "L"]
        all_revealed_partial = all(char in guessed_partial for char in secret)
        self.assertFalse(all_revealed_partial)

if __name__ == "__main__":
    unittest.main()
