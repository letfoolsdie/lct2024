
import os
import pickle
COMPL_DEF_PATH = "/app"
COMPL_BASE_PATH = os.path.join(COMPL_DEF_PATH, "db.pkl")

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_words(node, prefix)

    def _collect_words(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char, child in node.children.items():
            words.extend(self._collect_words(child, prefix + char))
        return words

class Autocompleler():

    @staticmethod
    def save_new_query(query: str):
        if os.path.isfile(COMPL_BASE_PATH):
            print(COMPL_BASE_PATH)
            with open(COMPL_BASE_PATH, 'rb') as f:
                db = pickle.load(f)
        else:
            db = Trie()

        db.insert(query)

        with open(COMPL_BASE_PATH, 'wb') as f:
            pickle.dump(db, f)

    @staticmethod
    def search_prefix(query: str):
        if os.path.isfile(COMPL_BASE_PATH):
            with open(COMPL_BASE_PATH, 'rb') as f:
                db = pickle.load(f)

            return db.search_prefix(query.lower())
        
        return []

        

        