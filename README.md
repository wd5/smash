# Smash

Really quick and dirty script for reverse lookup MD5 hashes for dictionary words

## Use

We have an MD5 hash (5f4dcc3b5aa765d61d8327deb882cf99) and want to crack it.

```bash
python smash.py 5f4dcc3b5aa765d61d8327deb882cf99
```

Returns 'password'

# TODO 

Reverse lookup and move to Redis