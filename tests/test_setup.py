"""Week 0 setup check. Run with:  pytest tests/test_setup.py -v"""
import sys

import pytest


def test_python_version():
    found = sys.version.split()[0]
    assert sys.version_info >= (3, 11), f"Python 3.11+ required, found {found}"


def test_packages():
    import mysql.connector  # noqa: F401
    import nltk  # noqa: F401
    import pandas  # noqa: F401
    import spacy  # noqa: F401


def test_mysql_connection():
    import mysql.connector

    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            database="real_estate",
            connection_timeout=5,
        )
    except mysql.connector.Error as e:
        pytest.fail(f"MySQL not reachable ({e}). Run `docker compose up -d` and retry.")

    cur = conn.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()[0]
    conn.close()
    assert version.startswith("8.0"), f"Expected MySQL 8.0, got {version}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
