import hashlib
import MySQLdb as database
import sys

# Returns the md5 hash of a string
def md5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

# Temporary DB object. Will move to Redis in the morning
class DB(object):
    def __init__(self, user='root', pw='', db='smash'):
        self.user = user
        self.pw = pw
        self.db = db
        self.con = database.connect('localhost', self.user, self.pw, self.db)
        self.cur = self.con.cursor()

    def create_db(self):
        with self.con:
          cur = self.con.cursor()
          cur.execute("CREATE TABLE IF NOT EXISTS data(Id INT PRIMARY KEY AUTO_INCREMENT, word VARCHAR(255), md5 VARCHAR(255))")

    def insert(self, word, hash):
        with self.con:
          cur = self.con.cursor()
          cur.execute("INSERT INTO data(word, md5) VALUES('%s', '%s')" % (word, hash))

    # Given an md5 hash, will return the unhashed version 
    def find(self, hash):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT word from data WHERE md5='%s'" % (hash))
            print cur.fetchone()[0]
      
class HashStore(object):
    @staticmethod
    def store_hashes(db_obj, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                w = line.strip()
                db.insert(w, md5(w))

def main(h):

    db = DB()
    #db.create_db()
    #HashStore.store_hashes(db,'/usr/share/dict/words')
    db.find(h)

if __name__ == '__main__':
    md5_hash = sys.argv[1]
    main(md5_hash)