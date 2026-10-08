
"""Week 1 validation tests. Run from the project root:  pytest tests/ -v"""
import json
import re

import pandas as pd
import pytest

TAXONOMY = "data/processed/taxonomy.json"
SAMPLE = "data/processed/listing_sample.csv"


@pytest.fixture(scope="module")
def tax():
    with open(TAXONOMY) as f:
        return json.load(f)


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(SAMPLE)


def test_taxonomy_loaded(tax):
    assert len(tax["terms"]) >= 200
    assert all("id" in t and "term" in t for t in tax["terms"])


def test_taxonomy_has_8_categories(tax):
    cats = {t["category"] for t in tax["terms"]}
    assert len(cats) >= 8, f"only {len(cats)} categories: {cats}"


def test_term_ids_unique(tax):
    ids = [t["id"] for t in tax["terms"]]
    assert len(ids) == len(set(ids))


def test_sample_data_quality(df):
    assert len(df) >= 500
    assert df["remarks"].str.len().min() > 50


def test_taxonomy_coverage(tax, df):
    """At least 30% of remarks must mention one or more taxonomy terms."""
    phrases = set()
    for t in tax["terms"]:
        phrases.add(t["term"].lower())
        phrases.update(s.lower() for s in t.get("synonyms", []))
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, sorted(phrases, key=len, reverse=True))) + r")\b")
    hits = df["remarks"].str.lower().apply(lambda s: bool(pattern.search(s)))
    coverage = hits.mean()
    print(f"\nTaxonomy coverage: {coverage:.1%}")
    assert coverage >= 0.30