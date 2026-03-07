from collections import Counter
from datetime import datetime

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def busiest_weekday(repo, since="2024-01-01", until=None):
    """Print commit counts per day of the week."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    weekday_counts = Counter()

    for commit in repo.iter_commits(since=since_date, until=until_date):
        weekday = commit.committed_datetime.weekday()
        weekday_counts[weekday] += 1

    if not weekday_counts:
        print("No commits found in the given date range.")
        return

    print("Commits per weekday:")
    for day in range(7):
        count = weekday_counts.get(day, 0)
        print(f"  {WEEKDAY_NAMES[day]}: {count}")

    busiest = max(weekday_counts, key=weekday_counts.get)
    print(f"\nBusiest day: {WEEKDAY_NAMES[busiest]} ({weekday_counts[busiest]} commits)")
