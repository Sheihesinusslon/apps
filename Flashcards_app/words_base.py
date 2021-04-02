import sqlite3

class Wordsbase:
    '''Class creates connection to SQL database and performs main operations with it'''
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_sets(self):
        '''Get names of existing card sets'''
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT `Set` FROM `Words`").fetchall()

    def find_word(self, word):
        '''By a given word find full card info and return it'''
        with self.connection:
            return self.cursor.execute("SELECT * FROM `Words` WHERE Word=?", (word,)).fetchone()

    def exists(self, word):
        '''Check if a given word matches any card/word in db'''
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) FROM `Words` WHERE Word=?", (word,)).fetchall()

    def get_words(self, set_name):
        '''Get all cards/words from the card set. If param = 'all', return all existing cards'''
        with self.connection:
            if set_name == 'all':
                return self.cursor.execute("SELECT * FROM `Words`").fetchall()
            else:
                return self.cursor.execute("SELECT * FROM `Words` WHERE `Set`=?", (set_name,)).fetchall()

    def add_word(self, set, word, definition):
        '''Add new card to the card set'''
        with self.connection:
            return self.cursor.execute("INSERT INTO `Words` (`Set`, `Word`, `Definition`) VALUES(?,?,?)", (set,word,definition))

    def update_word(self, set, word, definition):
        ''' Update info about existing card '''
        with self.connection:
            return self.cursor.execute("UPDATE `Words` SET `Set`=?, Definition=? WHERE Word=?", (set,definition,word))

    def delete_word(self, word):
        ''' Delete a card from the card set '''
        with self.connection:
            return self.cursor.execute("DELETE FROM `Words` WHERE Word=?", (word,))
