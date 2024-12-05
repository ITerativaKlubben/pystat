from collections import defaultdict
from datetime import datetime

def commits_per_month(repo, since="2024-01-01"):
    """Print commits grouped by month starting from a specific date."""
    commits_per_month = defaultdict(int)
    since_date = datetime.strptime(since, "%Y-%m-%d")

    for commit in repo.iter_commits(since=since_date):
        month = commit.committed_datetime.strftime("%Y-%m")
        commits_per_month[month] += 1

    for month, count in sorted(commits_per_month.items()):
        print(f"{month}: {count}")

def commits_per_day(repo, month, since="2024-01-01"):
    """Print commits for each day in a specific month starting from a specific date."""
    commits_per_day = defaultdict(int)
    since_date = datetime.strptime(since, "%Y-%m-%d")

    for commit in repo.iter_commits(since=since_date):
        date = commit.committed_datetime.strftime("%Y-%m-%d")
        if date.startswith(month):
            commits_per_day[date] += 1

    for day, count in sorted(commits_per_day.items()):
        print(f"{day}: {count}")

