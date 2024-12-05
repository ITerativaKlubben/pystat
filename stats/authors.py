from collections import defaultdict
from datetime import datetime

def commits_by_author_per_month(repo, since="2024-01-01"):
    """Print commit counts grouped by author and month, and total commit counts for each author starting from a specific date."""
    commits_by_author_per_month = defaultdict(lambda: defaultdict(int))
    total_commits_by_author = defaultdict(int)
    since_date = datetime.strptime(since, "%Y-%m-%d")

    for commit in repo.iter_commits(since=since_date):
        month = commit.committed_datetime.strftime("%Y-%m")
        author = commit.author.name
        commits_by_author_per_month[month][author] += 1
        total_commits_by_author[author] += 1

    # Print commits per month by author
    for month, authors in sorted(commits_by_author_per_month.items()):
        print(f"{month}:")
        for author, count in authors.items():
            print(f"  {author}: {count}")

    # Print total commits per author
    print("\nTotal commits by author:")
    for author, count in sorted(total_commits_by_author.items(), key=lambda x: x[1], reverse=True):
        print(f"{author}: {count}")

def commits_by_author_per_day(repo, month, since="2024-01-01"):
    """Print commit counts grouped by author and day for a specific month starting from a specific date."""
    commits_by_author_per_day = defaultdict(lambda: defaultdict(int))
    since_date = datetime.strptime(since, "%Y-%m-%d")

    for commit in repo.iter_commits(since=since_date):
        day = commit.committed_datetime.strftime("%Y-%m-%d")
        if day.startswith(month):
            author = commit.author.name
            commits_by_author_per_day[day][author] += 1

    # Print commits per day by author
    for day, authors in sorted(commits_by_author_per_day.items()):
        print(f"{day}:")
        for author, count in authors.items():
            print(f"  {author}: {count}")

