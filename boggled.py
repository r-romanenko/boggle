from typing import List, Tuple, Set

class TrieNode:
    def __init__(self, letter=None) -> None:
        self.letter = letter
        # add attributes for whether it is the end of a word and a collection of pointers to
        self.end_of_word = False
        # next letters
        self.next_letters = dict()

class Trie:
    def __init__(self) -> None:
        # create TrieNode root
        self.root = TrieNode("")
        self.generate_tree_from_file()

    def generate_tree_from_file(self)->None:
        words = self._load_words()
        
        # iterate through the list of words
        for word in words:
            # reverse the word
            word = word[::-1]
            cur_node = self.root

            # for every letter in the word, go through the tree
            for letter in word:
                # if the node doesn't exist, add it to the Dictionary
                if not letter in cur_node.next_letters:
                    cur_node.next_letters[letter] = TrieNode(letter)
                # go into the now guaranteed existing node
                cur_node = cur_node.next_letters[letter] 

            # set the node as an end of a word
            cur_node.end_of_word = True

        

    # helper to load words. No modifications needed
    def _load_words(self):
        words = []
        with open("words.txt", "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                words.append(word)
        return words

# This Boggle has the following special properties:
# 1) All words returned should end in a specified suffix (i.e. encode the trie in reverse)
# 2) Board tiles may have more than 1 letter (e.g. "qu" or "an")
# 3) The number of times you can use the same tile in a word is variable
class Boggled:

    # setup test initializes the game with the game board and the max number of times we can use each 
    # tile per word
    def setup_board(self, max_uses_per_tile: int, board:List[List[str]])->None:
        self.max_uses_per_tile = max_uses_per_tile
        self.board = board
        self.board_size = len(board[0])
        self.trie = Trie()
        

    
    # Returns a set of all words on the Boggle board that end in the suffix parameter string. Words can be found
    # in all 8 directions from a position on the board
    def get_all_words(self, suffix:str)->Set:
        suffix = suffix[::-1]   

        # the set of all the words you found that you will return
        self.all_words = set()
        double_letter = False

        # the 2D Array that keeps track of how much each tile has been used
        
        self.tile_uses = []

        for i in range(len(self.board)):
            self.tile_uses.append([])
            for k in range(len(self.board)):
                self.tile_uses[i].append(self.max_uses_per_tile)



        for row in range(self.board_size):
            for col in range(self.board_size):
                self.get_all_words_recursive("", suffix, row, col, self.trie.root, double_letter)

        return self.all_words


    # recursive helper for get_all_words. Customize parameters as needed; you will likely need params for 
    # at least a board position and tile
    def get_all_words_recursive(self, word:str, suffix:str, row:int, col:int, node:TrieNode, double_letter:bool):        

        tile_value = ""

        # -------------------------- BASE CASE --------------------------

        # check if the row and col are valid parts in the board
        if not (row >= 0 and row < self.board_size and col >= 0 and col < self.board_size):
            return

        # check if the node is a leaf, that means you can't add any more words, so you can immediately revert
        if len(node.next_letters) == 0 and self.board[row][col] in node.next_letters:
            return


        # check if the tile is a double letter, then check the node tree accordingly. set tile_value
        if len(self.board[row][col]) > 1: # if double letter
            if double_letter: # if the first letter has already been used                
                tile_value = self.board[row][col][0] # make the tile_value the "second" letter
                double_letter = False
            # if the first letter has not already been used
            else: 
                double_letter = True
                tile_value = self.board[row][col][1] # make the tile_value the "first" letter
        # if the tile is not a double letter
        else: 
            tile_value = self.board[row][col]

        if tile_value in node.next_letters: # check if it's in the node children
            node = node.next_letters[tile_value] # make the node the corresponding child
        else:
            return

        # check if the tile you're on has any more uses left by looking at a mirrored 2D array that has corresponding "uses" values for each tile
        if self.tile_uses[row][col] <= 0:
            return

        # if the length of the word is less than the suffix
        if len(word) < len(suffix):
            if not suffix[len(word):len(word)+1] == tile_value:
                return
        



        # ------------------------ RECURSIVE CASE ------------------------

        # make a list of the surrounding nodes
        offsets:List = [[-1, -1], [-1, 0], [-1, 1],
                        [0, -1],           [0, 1],
                        [1, -1],  [1, 0],  [1, 1]]

        # CHOOSE

        # Add the current node letter to the word
        word += tile_value

        # subtract a "use" from the corresponding tile in tile_uses
        if not double_letter:
            self.tile_uses[row][col] -= 1


        # If it's a valid word (with the boolean), add it to the set of words
        if node.end_of_word and not double_letter:
            if len(word) > len(suffix):
                self.all_words.add(word[::-1])

        # EXPLORE

        # Go into the 8 surrounding tiles
        for offset in offsets:
            new_row = row
            new_col = col
            if not double_letter:
                new_row += offset[0]
                new_col += offset[1]
            self.get_all_words_recursive(word, suffix, new_row, new_col, node, double_letter)


        # UNCHOOSE

        # Remove the last letter of the word
        word = word[:-1]
        
        # Add back 1 to the 2D array of "uses"
        if not double_letter:
            self.tile_uses[row][col] += 1