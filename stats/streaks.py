from datetime import datetime, timedelta

def longest_streak(repo, since="2024-01-01", until=None):
    """Find the longest consecutive days with at least one commit."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    commit_days = set()

    for commit in repo.iter_commits(since=since_date, until=until_date):
        day = commit.committed_datetime.date()
        commit_days.add(day)

    if not commit_days:
        print("No commits found in the given date range.")
        return

    sorted_days = sorted(commit_days)
    best_streak = 1
    best_start = sorted_days[0]
    current_streak = 1
    current_start = sorted_days[0]

    for i in range(1, len(sorted_days)):
        if sorted_days[i] - sorted_days[i - 1] == timedelta(days=1):
            current_streak += 1
        else:
            if current_streak > best_streak:
                best_streak = current_streak
                best_start = current_start
            current_streak = 1
            current_start = sorted_days[i]

    if current_streak > best_streak:
        best_streak = current_streak
        best_start = current_start

    best_end = best_start + timedelta(days=best_streak - 1)
    print(f"Longest commit streak: {best_streak} days ({best_start} to {best_end})")
    print(f"Total days with commits: {len(commit_days)}")
