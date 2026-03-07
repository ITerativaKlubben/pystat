from collections import defaultdict, Counter
from datetime import datetime

def file_ownership(repo, since="2024-01-01", until=None, top_n=15):
    """Return dict of file -> Counter of author commit counts."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    file_authors = defaultdict(Counter)

    for commit in repo.iter_commits(since=since_date, until=until_date):
        author = commit.author.name
        for file in commit.stats.files.keys():
            file_authors[file][author] += 1

    return dict(file_authors)
