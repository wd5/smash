# -*- coding: utf-8 -*-

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
#import MySQLdb as database
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
                        con.set(md5(perm), perm)
        
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

if __name__ == '__main__':
    
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    if len(sys.argv) > 1:
        h = sys.argv[1]
        print RedisStore.get(r, "%s" % h)
    else:
      print "Building Redis store. This may take a while..."
      RedisStore.create(r, '/usr/share/dict/words')