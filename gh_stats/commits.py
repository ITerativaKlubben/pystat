"""Fetch commits from GitHub API and compute all commit-based stats in one pass.

Replaces the local git stats modules when GitHub is available.
Returns a dict matching the same keys/types as the local stats.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta


def fetch_commit_stats(gh_repo, since=None, until=None):
    """Fetch all commits from GitHub and compute stats matching local git output.

    Makes one paginated call for the commit list, plus one API call per
    in-range commit to get file-level details (lines, changes, ownership).
    Also iterates commits before `since` to detect first-time contributors.
    """
    since_date = datetime.strptime(since, "%Y-%m-%d").date() if since else None
    until_date = datetime.strptime(until, "%Y-%m-%d").date() if until else None

    since_dt = datetime.strptime(since, "%Y-%m-%d") if since else None
    until_dt = datetime.strptime(until, "%Y-%m-%d") if until else None

    # Accumulators for in-range commits
    commits_per_month = defaultdict(int)
    author_monthly = defaultdict(lambda: defaultdict(int))
    author_totals = defaultdict(int)
    hour_counts = Counter()
    weekday_counts = Counter()
    word_counter = Counter()
    lines_stats = defaultdict(lambda: {"added": 0, "removed": 0})
    file_changes = Counter()
    file_authors = defaultdict(Counter)
    coauthored_count = 0
    commit_days = set()

    # Track first commit per author across ALL commits (for new contributor detection)
    first_commit_ever = {}

    # Fetch ALL commits (no date filter) to find true first commits
    # The API returns newest-first, so we process everything
    for commit in gh_repo.get_commits():
        gc = commit.commit
        author_name = gc.author.name if gc.author else "Unknown"
        date = gc.author.date if gc.author else None
        if date is None:
            continue

        d = date.date()

        # Track first-ever commit per author
        date_str = str(d)
        if author_name not in first_commit_ever or date_str < first_commit_ever[author_name]:
            first_commit_ever[author_name] = date_str

        # Skip if outside the date range for stats aggregation
        if since_date and d < since_date:
            continue
        if until_date and d > until_date:
            continue

        # --- In-range stats ---
        month_key = date.strftime("%Y-%m")
        commits_per_month[month_key] += 1
        author_monthly[month_key][author_name] += 1
        author_totals[author_name] += 1
        hour_counts[date.hour] += 1
        weekday_counts[date.weekday()] += 1
        commit_days.add(d)

        message = gc.message or ""

        # Co-authored
        if "Co-authored-by" in message:
            coauthored_count += 1

        # Word frequency (same regex as local: all \w+ tokens)
        words = re.findall(r'\b\w+\b', message.lower())
        word_counter.update(words)

        # File-level stats (triggers individual commit API call)
        try:
            if commit.stats:
                lines_stats[author_name]["added"] += commit.stats.additions
                lines_stats[author_name]["removed"] += commit.stats.deletions
            for f in commit.files:
                file_changes[f.filename] += 1
                file_authors[f.filename][author_name] += 1
        except Exception:
            pass

    # Compute streaks
    streak_data = _compute_streaks(commit_days)

    # New contributors: first-ever commit falls within the date range
    new_contributors = {}
    for author, first_date_str in first_commit_ever.items():
        first_d = datetime.strptime(first_date_str, "%Y-%m-%d").date()
        if since_date and first_d < since_date:
            continue
        if until_date and first_d > until_date:
            continue
        new_contributors[author] = first_date_str

    return {
        "commits_per_month": dict(sorted(commits_per_month.items())),
        "author_monthly": {k: dict(v) for k, v in sorted(author_monthly.items())},
        "author_totals": dict(author_totals),
        "words": word_counter,
        "hour_counts": hour_counts if hour_counts else None,
        "file_changes": file_changes,
        "lines": dict(lines_stats),
        "coauthored": coauthored_count,
        "weekday_counts": weekday_counts if weekday_counts else None,
        "streaks": streak_data,
        "new_contributors": new_contributors,
        "ownership": dict(file_authors),
    }


def _compute_streaks(commit_days):
    """Compute longest consecutive-day streak from a set of dates."""
    if not commit_days:
        return None

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
    return {
        "best_streak": best_streak,
        "best_start": str(best_start),
        "best_end": str(best_end),
        "total_days_with_commits": len(commit_days),
    }
