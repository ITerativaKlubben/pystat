from collections import Counter
from datetime import datetime, timedelta, timezone
from stats.visualization import plot_commit_times_by_hour

def commit_times_by_hour(repo):
    """Analyze the most and least common commit times by hour for the past year."""
    # Get the current time (timezone-aware) and calculate the time one year ago
    now = datetime.now(timezone.utc)
    one_year_ago = now - timedelta(days=365)

    # Collect commit hours for the past year
    commit_hours = []
    for commit in repo.iter_commits():
        commit_time = commit.committed_datetime
        if commit_time >= one_year_ago:  # Filter for the past year
            commit_hours.append(commit_time.hour)

    # Count occurrences of each hour
    hour_counts = Counter(commit_hours)
    
    plot_commit_times_by_hour(hour_counts)
    # Sort by hour
    sorted_hours = sorted(hour_counts.items())

    # Display results
    print("Commit activity by hour (past year):")
    for hour, count in sorted_hours:
        print(f"{hour:02d}:00 - {count} commits")

    # Find the most and least common commit times
    most_common = hour_counts.most_common(1)[0]
    least_common = min(hour_counts.items(), key=lambda x: x[1])

    print("\nMost common commit time:")
    print(f"{most_common[0]:02d}:00 - {most_common[1]} commits")

    print("\nLeast common commit time:")
    print(f"{least_common[0]:02d}:00 - {least_common[1]} commits")

