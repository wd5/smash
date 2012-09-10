# Smash

Really quick and dirty script for reverse lookup MD5 hashes for dictionary words. 

Currently supports lookup of SHA1 and MD5 hash values.

Requires Redis and Flask

## Use

We have an MD5 hash (5f4dcc3b5aa765d61d8327deb882cf99) and want to crack it.

The first thing we need to do is create a lookup table using a text file of common words. 

On OSX we can use the built in dictionary found in /usr/share/dict/words

```
python smash.py
```

Then we can very quickly crack the hash if it's a common dictionary word

```bash
python smash.py 5f4dcc3b5aa765d61d8327deb882cf99
```

Returns 'password'

# TODO 

Move to Redis (done)
Web app (partially done)