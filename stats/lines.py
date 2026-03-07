from collections import defaultdict
from datetime import datetime

def lines_by_author(repo, since="2024-01-01", until=None):
    """Print the number of lines added and removed by each author."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    lines_stats = defaultdict(lambda: {"added": 0, "removed": 0})

    for commit in repo.iter_commits(since=since_date, until=until_date):
        author = commit.author.name
        stats = commit.stats

        # Sum lines added and removed
        for file_stat in stats.files.values():
            lines_stats[author]["added"] += file_stat["insertions"]
            lines_stats[author]["removed"] += file_stat["deletions"]

    print("Lines added and removed per author:")
    for author, stats in lines_stats.items():
        print(f"{author}: {stats['added']} lines added, {stats['removed']} lines removed")

