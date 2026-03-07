from collections import defaultdict
from datetime import datetime

def commits_by_author_per_month(repo, since="2024-01-01", until=None):
    """Return commit counts grouped by author and month, and total commit counts."""
    monthly = defaultdict(lambda: defaultdict(int))
    totals = defaultdict(int)
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None

    for commit in repo.iter_commits(since=since_date, until=until_date):
        month = commit.committed_datetime.strftime("%Y-%m")
        author = commit.author.name
        monthly[month][author] += 1
        totals[author] += 1

    return dict(monthly), dict(totals)
