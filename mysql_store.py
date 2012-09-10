# -*- coding: utf-8 -*-

# ==============================
#
# An adpater for MySQL
#
# ==============================

import MySQLdb as database

class DB(object):
    
    """ An alternative MySQL store """
    
    def __init__(self, user='root', pw='', db='smash'):
        self.user = user
        self.pw = pw
        self.db = db
        self.con = self.try_connect()
        self.cur = self.con.cursor()

    def try_connect(self):
        try:
            return database.connect('localhost', self.user, self.pw, self.db)
        except database.OperationalError, e:
            exit(e)
      
    def create_db(self):
        """ Create the database tables """
        try:
            with self.con:
              cur = self.con.cursor()
              cur.execute("CREATE TABLE IF NOT EXISTS \
                  data(Id INT PRIMARY KEY AUTO_INCREMENT, \
                  word VARCHAR(255), md5 VARCHAR(255), sha1 VARCHAR(255))")
        except Exception, e:
            print e

    def insert(self, word, md5, sha1):
        """ Insert an item into the database """
        with self.con:
          cur = self.con.cursor()
          cur.execute("INSERT INTO data(word, md5, sha1) VALUES('%s', '%s', '%s')" % (word, md5, sha1))

    def find_md5(self, hash):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT word from data WHERE md5='%s'" % (hash))
            print cur.fetchone()[0]
 
    def find_sha1(self, hash):
       with self.con:
           cur = self.con.cursor()
           cur.execute("SELECT word from data WHERE sha1='%s'" % (hash))
           print cur.fetchone()[0]
      
class HashStore(object):
    @staticmethod
    def store_words(db_obj, word, tollerance=3, *args):
        """ Store permutations of a word in the database
            along with the hash of that word """ 
        # ignore words less than 4 letters
        if len(word) > tollerance:
            w = word.strip()
            for perm in permutations(w):
                db_obj.insert(perm, md5(perm), sha1(perm))

    @staticmethod
    def store_hashes(db_obj, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                  HashStore.store_words(db_obj, line)
                 
def create_database():
    db = DB()
    db.create_db()
    HashStore.store_hashes(db,'/usr/share/dict/words')

def main(h):
    DB().find_md5(h)