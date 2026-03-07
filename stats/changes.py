from collections import Counter
from datetime import datetime


def most_changed_files(repo, since="2024-01-01", until=None):
    """Return a Counter of file change frequencies."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    file_changes = Counter()

    for commit in repo.iter_commits(since=since_date, until=until_date):
        for file in commit.stats.files.keys():
            file_changes[file] += 1

    return file_changes
