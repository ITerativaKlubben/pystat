from datetime import datetime

def first_time_contributors(repo, since="2024-01-01", until=None):
    """Return dict of author -> first commit date string for new contributors in range."""
    since_date = datetime.strptime(since, "%Y-%m-%d").date()
    until_date = datetime.strptime(until, "%Y-%m-%d").date() if until else None

    first_commit = {}
    for commit in repo.iter_commits():
        author = commit.author.name
        date = commit.committed_datetime.date()
        if author not in first_commit or date < first_commit[author]:
            first_commit[author] = date

    if not first_commit:
        return {}

    new_contributors = {
        author: str(date) for author, date in first_commit.items()
        if date >= since_date and (until_date is None or date <= until_date)
    }

    return new_contributors
