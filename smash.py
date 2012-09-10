# ============================================
#
# A script for cracking easy md5 and sha1 passwords
# Uses brute force lookups on common phrases 
# and word mutations. i.e pa55w0rd, op3n etc
#
# Currently supports only single word lookups but can easily be
# adapted to support a larger corpus of words
#
# Seeding the database takes a very long time. 
#
# ============================================

import hashlib
import MySQLdb as database
import sys
import redis

__version__ = '0.0.1'

class RedisStore(object):
    """ A Redis store """
    @staticmethod
    def add(con, word, hash):
        con.set(word, md5_hash)
    @staticmethod
    def get(con, word):
        return con.get(word)
    @staticmethod
    def create(con, file_name, tollerance=3):
        """ Stores each word along with the md5 hash of that word"""
        with open(file_name, 'r') as f:
            for word in f:
                if len(word) > tollerance:
                    w = word.strip()
                    for perm in permutations(w):
                        con.set(perm, md5(perm))
        
# These two functions are used to encode a string to an md5 or sha1 hash

def md5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()
     
def sha1(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def interpose_numerics(word):
    """ Swap out letters for numbers 
        e.g password becomes pa55w0rd etc"""
    letter_exchanges = {'e' : '3',
                        'o' : '0',
                        'l' : '1',
                        's' : '5'}
    def swap_if(letter):
        for k, v in letter_exchanges.items():
            if k == letter:
                return v
            else:
                return letter
    return "".join(map(lambda w: swap_if(w), [char for char in word.strip()]))
        
def permutations(word):
    """ Returns common password permutations of a word 
        e.g ['password', 'password1', 'pa55word'] """
    perms = []
    perms.append(word)
    perms.append(word + "1")
    perms.append(word + "123")
    perms.append(interpose_numerics(word))
    return perms

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

if __name__ == '__main__':
    
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    if len(sys.argv) > 1:
        h = sys.argv[1]
        print RedisStore.get(r, "%s" % h)
    else:
      print "Building Redis store. This may take a while..."
      RedisStore.create(r, '/usr/share/dict/words')
