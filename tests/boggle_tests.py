import datetime
from unittest import TestCase

from boggled import Boggled

class BoggleTests(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def _load_board(self, file_name):
        game_board = []
        with open(file_name, "r") as board:
            lines = board.readlines()
            for line in lines:
                board_line = []
                for letter in line.split(","):
                    board_line.append(letter.strip())
                game_board.append(board_line)
        return game_board

    def _load_words(self, file_name):
        result = set()
        with open(file_name, "r") as words:
            found_words = words.readlines()
            for word in found_words:
                result.add(word.strip())
        return result

    def test_four_board_reuse_letters(self):
        board = self._load_board(f"./tests/data/four_board_reuse.txt")
        game = Boggled()
        game.setup_board(1, board)
        start_time = datetime.datetime.now()
        found_words = game.get_all_words("eed")
        end_time = datetime.datetime.now()
        self.assertEqual(0, len(found_words))
        self.assertLess((end_time - start_time), datetime.timedelta(1))

        game = Boggled()
        game.setup_board(2, board)
        start_time = datetime.datetime.now()
        found_words = game.get_all_words("eed")
        end_time = datetime.datetime.now()
        self.assertEqual(1, len(found_words))
        self.assertIn("deed", found_words)
        self.assertLess((end_time - start_time), datetime.timedelta(1))

    def test_four_board_one_sol_no_letter_reuse(self):
        board = self._load_board(f"./tests/data/four_board.txt")
        game = Boggled()
        game.setup_board(1, board)
        start_time = datetime.datetime.now()
        found_words = game.get_all_words("est")
        end_time = datetime.datetime.now()
        self.assertEqual(1, len(found_words))
        self.assertIn("quest", found_words)
        self.assertLess((end_time - start_time), datetime.timedelta(1))

    def test_four_board_no_double_letter(self):
        board = self._load_board(f"./tests/data/four_board_no_double.txt")
        game = Boggled()
        game.setup_board(2, board)
        start_time = datetime.datetime.now()
        found_words = game.get_all_words("est")
        end_time = datetime.datetime.now()
        self.assertEqual(1, len(found_words))
        self.assertIn("best", found_words)
        self.assertLess((end_time - start_time), datetime.timedelta(1))

    def test_four_board_no_words(self):
        board = self._load_board(f"./tests/data/four_board.txt")
        game = Boggled()
        game.setup_board(2, board)
        start_time = datetime.datetime.now()
        found_words = game.get_all_words("ing")
        end_time = datetime.datetime.now()
        self.assertEqual(0, len(found_words))
        self.assertLess((end_time - start_time), datetime.timedelta(1))


    def test_six_board(self):
        board = self._load_board(f"./tests/data/six_board.txt")
        words = self._load_words(f"./tests/data/six_words.txt")
        game = Boggled()
        game.setup_board(2, board)
        start_time = datetime.datetime.now()
        found_words = game.get_all_words("ed")
        end_time = datetime.datetime.now()
           
        self.assertEqual(len(words), len(found_words))
        for word in words:
            self.assertIn(word, found_words)
        
        self.assertLess((end_time - start_time), datetime.timedelta(2))

    def test_big_board(self):
        board = self._load_board(f"./tests/data/big_board.txt")
        words = self._load_words(f"./tests/data/big_board_words.txt")
        game = Boggled()
        game.setup_board(3, board)
        start_time = datetime.datetime.now()
        found_words = game.get_all_words("ing")
        end_time = datetime.datetime.now()

        self.assertEqual(len(words), len(found_words))
        for word in words:
            self.assertIn(word, found_words)
        
        self.assertLess((end_time - start_time), datetime.timedelta(15))
       