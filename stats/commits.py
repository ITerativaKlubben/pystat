from collections import defaultdict

def commits_per_month(repo):
    """Print commits grouped by month."""
    commits_per_month = defaultdict(int)
    for commit in repo.iter_commits():
        month = commit.committed_datetime.strftime("%Y-%m")
        commits_per_month[month] += 1

    for month, count in sorted(commits_per_month.items()):
        print(f"{month}: {count}")

def commits_per_day(repo, month):
    """Print commits for each day in a specific month."""
    commits_per_day = defaultdict(int)
    for commit in repo.iter_commits():
        date = commit.committed_datetime.strftime("%Y-%m-%d")
        if date.startswith(month):
            commits_per_day[date] += 1

    for day, count in sorted(commits_per_day.items()):
        print(f"{day}: {count}")

