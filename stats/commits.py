from collections import defaultdict
from datetime import datetime

def commits_per_month(repo, since="2024-01-01", until=None):
    """Print commits grouped by month starting from a specific date."""
    commits_per_month = defaultdict(int)
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None

    for commit in repo.iter_commits(since=since_date, until=until_date):
        month = commit.committed_datetime.strftime("%Y-%m")
        commits_per_month[month] += 1

    for month, count in sorted(commits_per_month.items()):
        print(f"{month}: {count}")

def commits_per_day(repo, since="2024-01-01", until=None):
    """Print commits for each day in the given date range."""
    commits_per_day = defaultdict(int)
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None

    for commit in repo.iter_commits(since=since_date, until=until_date):
        date = commit.committed_datetime.strftime("%Y-%m-%d")
        commits_per_day[date] += 1

    for day, count in sorted(commits_per_day.items()):
        print(f"{day}: {count}")

