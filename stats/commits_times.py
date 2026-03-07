from collections import defaultdict
from datetime import datetime

def commits_over_time(repo, since="2024-01-01", until=None):
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    commit_trends = defaultdict(int)
    for commit in repo.iter_commits(since=since_date, until=until_date):
        week = commit.committed_datetime.strftime("%Y-%W")
        commit_trends[week] += 1

    print("Commits over time (by week):")
    for week, count in sorted(commit_trends.items()):
        print(f"Week {week}: {count} commits")

