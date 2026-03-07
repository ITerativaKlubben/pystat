from collections import defaultdict
from datetime import datetime

def commits_per_month(repo, since="2024-01-01", until=None):
    """Return commits grouped by month."""
    result = defaultdict(int)
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None

    for commit in repo.iter_commits(since=since_date, until=until_date):
        month = commit.committed_datetime.strftime("%Y-%m")
        result[month] += 1

    return dict(result)
