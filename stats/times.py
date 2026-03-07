from collections import Counter
from datetime import datetime

def commit_times_by_hour(repo, since="2024-01-01", until=None):
    """Return a Counter of commit counts by hour of day."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None

    commit_hours = []
    for commit in repo.iter_commits(since=since_date, until=until_date):
        commit_hours.append(commit.committed_datetime.hour)

    hour_counts = Counter(commit_hours)

    if not hour_counts:
        return None

    return hour_counts
