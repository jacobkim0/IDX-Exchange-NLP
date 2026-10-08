"""Week 1: mine frequent n-grams from remarks as taxonomy candidates."""
from collections import Counter

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.util import ngrams

for res in ["punkt", "punkt_tab", "stopwords"]:
    nltk.download(res, quiet=True)

df = pd.read_csv("data/processed/listing_sample.csv")
STOP = set(stopwords.words("english"))

rows = []
for text in df["remarks"].dropna().str.lower():
    tokens = [t for t in nltk.word_tokenize(text) if any(c.isalpha() for c in t)]
    rows.append(tokens)


def count(n):
    c = Counter()
    for tokens in rows:
        for gram in ngrams(tokens, n):
            if gram[0] in STOP or gram[-1] in STOP:
                continue
            c[" ".join(gram)] += 1
    return c


results = []
for n, top in [(1, 300), (2, 200), (3, 100)]:
    for term, freq in count(n).most_common(top):
        results.append({"ngram": term, "n": n, "count": freq})

out = pd.DataFrame(results)
out.to_csv("data/processed/ngram_candidates.csv", index=False)

print("Top 30 bigrams:")
for _, r in out[out.n == 2].head(30).iterrows():
    print(f"  {r.ngram}: {r['count']}")
print(f"\nSaved {len(out)} candidates to data/processed/ngram_candidates.csv")
