from datetime import datetime

def coauthored_commits(repo, since="2024-01-01", until=None):
    """Return count of co-authored commits."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    coauthored_count = 0

    for commit in repo.iter_commits(since=since_date, until=until_date):
        if "Co-authored-by" in commit.message:
            coauthored_count += 1

    return coauthored_count
