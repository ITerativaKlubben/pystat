from datetime import datetime

from gh_stats.client import in_date_range


def issue_stats(gh_repo, since=None, until=None):
    """Gather issue statistics (excluding PRs): opened/closed in range, currently open."""
    opened_in_range = 0
    closed_in_range = 0
    resolution_times = []

    since_dt = datetime.strptime(since, "%Y-%m-%d") if since else None

    for issue in gh_repo.get_issues(state="all", since=since_dt, sort="created", direction="desc"):
        if issue.pull_request is not None:
            continue

        created = issue.created_at
        if not in_date_range(created, since, until):
            if since and created.date() < datetime.strptime(since, "%Y-%m-%d").date():
                break
            continue

        opened_in_range += 1

        if issue.state == "closed":
            closed_in_range += 1
            if issue.closed_at:
                delta = (issue.closed_at - created).total_seconds() / 3600
                resolution_times.append(delta)

    # Current open count (all time, excluding PRs)
    current_open = sum(1 for i in gh_repo.get_issues(state="open") if i.pull_request is None)

    avg_resolution_hours = (
        sum(resolution_times) / len(resolution_times) if resolution_times else 0
    )

    return {
        "current_open": current_open,
        "opened": opened_in_range,
        "closed": closed_in_range,
        "avg_resolution_hours": avg_resolution_hours,
    }
