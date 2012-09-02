import hashlib
import MySQLdb as database
import sys

__version__ = '0.0.1'

# These two functions are used to encode a string to an md5 or sha1 hash

def md5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()
     
def sha1(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

# Temporary. 
# Will move to Redis and tidy up when I get time
#
class DB(object):
    def __init__(self, user='root', pw='', db='smash'):
        self.user = user
        self.pw = pw
        self.db = db
        self.con = database.connect('localhost', self.user, self.pw, self.db)
        self.cur = self.con.cursor()

    def create_db(self):
        """ Create the database tables """
        with self.con:
          cur = self.con.cursor()
          cur.execute("CREATE TABLE IF NOT EXISTS \
              data(Id INT PRIMARY KEY AUTO_INCREMENT, \
              word VARCHAR(255), md5 VARCHAR(255), sha1 VARCHAR(255))")

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
    def store_hashes(db_obj, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                # ignore words less than 4 letters
                if len(line) > 3:
                  w = line.strip()
                  db_obj.insert(w, md5(w), sha1(w))
                
def create_database():
    db = DB()
    db.create_db()
    HashStore.store_hashes(db,'/usr/share/dict/words')

def main(h):
    DB().find_md5(h)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        md5_hash = sys.argv[1]
        main(md5_hash)
    else:
      print "Building database. This may take a while..."
      create_database()