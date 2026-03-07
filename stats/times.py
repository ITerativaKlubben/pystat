from collections import Counter
from datetime import datetime

def commit_times_by_hour(repo, since="2024-01-01", until=None):
    """Analyze the most and least common commit times by hour."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None

    commit_hours = []
    for commit in repo.iter_commits(since=since_date, until=until_date):
        commit_hours.append(commit.committed_datetime.hour)

    hour_counts = Counter(commit_hours)

    if not hour_counts:
        print("No commits found in the given date range.")
        return

    sorted_hours = sorted(hour_counts.items())

    print("Commit activity by hour:")
    for hour, count in sorted_hours:
        print(f"{hour:02d}:00 - {count} commits")

    most_common = hour_counts.most_common(1)[0]
    least_common = min(hour_counts.items(), key=lambda x: x[1])

    print("\nMost common commit time:")
    print(f"{most_common[0]:02d}:00 - {most_common[1]} commits")

    print("\nLeast common commit time:")
    print(f"{least_common[0]:02d}:00 - {least_common[1]} commits")

