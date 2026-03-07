from collections import Counter
from datetime import datetime

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def busiest_weekday(repo, since="2024-01-01", until=None):
    """Return a Counter of commits per weekday (0=Monday .. 6=Sunday)."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    weekday_counts = Counter()

    for commit in repo.iter_commits(since=since_date, until=until_date):
        weekday = commit.committed_datetime.weekday()
        weekday_counts[weekday] += 1

    if not weekday_counts:
        return None

    return weekday_counts
