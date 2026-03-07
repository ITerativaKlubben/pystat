from datetime import datetime

def first_time_contributors(repo, since="2024-01-01", until=None):
    """Print authors whose first-ever commit falls within the date range."""
    since_date = datetime.strptime(since, "%Y-%m-%d").date()
    until_date = datetime.strptime(until, "%Y-%m-%d").date() if until else None

    # Scan full history to find each author's true first commit
    first_commit = {}
    for commit in repo.iter_commits():
        author = commit.author.name
        date = commit.committed_datetime.date()
        if author not in first_commit or date < first_commit[author]:
            first_commit[author] = date

    if not first_commit:
        print("No commits found.")
        return

    # Filter to authors whose first commit is within the date range
    new_contributors = {
        author: date for author, date in first_commit.items()
        if date >= since_date and (until_date is None or date <= until_date)
    }

    if not new_contributors:
        print("No new contributors in this period.")
        return

    print("New contributors in this period:")
    for author, date in sorted(new_contributors.items(), key=lambda x: x[1]):
        print(f"  {author}: {date}")
