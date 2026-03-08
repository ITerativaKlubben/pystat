from collections import Counter, defaultdict
from datetime import datetime

from gh_stats.client import in_date_range


def pull_request_stats(gh_repo, since=None, until=None):
    """Gather PR statistics: counts, merge times, top authors/reviewers, PRs per month."""
    total = 0
    merged = 0
    open_count = 0
    closed_count = 0
    merge_times = []
    authors = Counter()
    reviewers = Counter()
    per_month = defaultdict(int)

    for pr in gh_repo.get_pulls(state="all", sort="created", direction="desc"):
        created = pr.created_at
        if not in_date_range(created, since, until):
            # Since sorted desc, if we're before the since date, stop
            if since and created.date() < datetime.strptime(since, "%Y-%m-%d").date():
                break
            continue

        total += 1
        authors[pr.user.login] += 1
        month_key = created.strftime("%Y-%m")
        per_month[month_key] += 1

        if pr.state == "open":
            open_count += 1
        elif pr.merged_at:
            merged += 1
            delta = (pr.merged_at - created).total_seconds() / 3600
            merge_times.append(delta)
            # Fetch reviewers only for merged PRs in range
            for review in pr.get_reviews():
                if review.user and review.user.login != pr.user.login:
                    reviewers[review.user.login] += 1
        else:
            closed_count += 1

    avg_merge_hours = sum(merge_times) / len(merge_times) if merge_times else 0
    merge_times_sorted = sorted(merge_times)
    median_merge_hours = (
        merge_times_sorted[len(merge_times_sorted) // 2] if merge_times_sorted else 0
    )

    return {
        "total": total,
        "merged": merged,
        "open": open_count,
        "closed": closed_count,
        "avg_merge_hours": avg_merge_hours,
        "median_merge_hours": median_merge_hours,
        "top_authors": authors.most_common(10),
        "top_reviewers": reviewers.most_common(10),
        "per_month": dict(sorted(per_month.items())),
    }
