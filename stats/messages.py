from collections import Counter
from datetime import datetime
import re

def most_and_least_frequent_words(repo, since="2024-01-01", until=None):
    """Return a Counter of word frequencies in commit messages."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    word_counter = Counter()

    for commit in repo.iter_commits(since=since_date, until=until_date):
        words = re.findall(r'\b\w+\b', commit.message.lower())
        word_counter.update(words)

    return word_counter
