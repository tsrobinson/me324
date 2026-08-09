"""Extract the pretrained GloVe vectors behind lecture 8's "Visualising
embeddings" figure, and save them to assets/data/glove-words.npz.

Run from the repo root:  python3 tools/make-glove-words.py
Downloads GloVe 6B 50-d (~66MB, the gensim-data mirror; a gzipped word2vec-format
text file, cached in ~/.cache/me324/ after the first download), then keeps just
the 20 words the slide plots. No gensim needed — the file is plain text.
"""
import gzip
import pathlib
import urllib.request

import numpy as np

URL = ("https://github.com/RaRe-Technologies/gensim-data/releases/download/"
       "glove-wiki-gigaword-50/glove-wiki-gigaword-50.gz")
CACHE = pathlib.Path.home() / ".cache" / "me324" / "glove-wiki-gigaword-50.gz"

WORDS = {  # word -> category
    "dog": "animal", "cat": "animal", "horse": "animal", "cow": "animal",
    "sheep": "animal", "pig": "animal", "fish": "animal", "bird": "animal",
    "london": "city", "paris": "city", "berlin": "city",
    "rome": "city", "madrid": "city", "vienna": "city",
    "bread": "food", "cheese": "food", "butter": "food",
    "apple": "food", "banana": "food", "rice": "food",
}

if not CACHE.exists():
    print(f"Downloading {URL} ...")
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(URL, CACHE)
print(f"Reading {CACHE} ...")

found = {}
with gzip.open(CACHE, "rt", encoding="utf-8") as f:
    n_words, dim = map(int, f.readline().split())
    print(f"vocab {n_words:,}, dim {dim}")
    for line in f:
        word, rest = line.split(" ", 1)
        if word in WORDS:
            found[word] = np.fromstring(rest, sep=" ", dtype=np.float32)
            if len(found) == len(WORDS):
                break

missing = set(WORDS) - set(found)
assert not missing, f"words not in vocab: {missing}"

words = list(WORDS)
out = "assets/data/glove-words.npz"
np.savez_compressed(
    out,
    words=np.array(words),
    category=np.array([WORDS[w] for w in words]),
    vectors=np.stack([found[w] for w in words]),
)
print(f"saved {out}: {len(words)} words x {dim} dims")
