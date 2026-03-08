from collections import Counter, defaultdict
from datetime import datetime

from gh_stats.client import in_date_range


def actions_stats(gh_repo, since=None, until=None):
    """Gather GitHub Actions statistics: run counts, success rate, durations, per-workflow."""
    total = 0
    success = 0
    failure = 0
    other = 0
    durations = []
    per_workflow = defaultdict(lambda: {"total": 0, "success": 0, "failure": 0})
    per_month = defaultdict(int)

    for run in gh_repo.get_workflow_runs():
        created = run.created_at
        if not in_date_range(created, since, until):
            if since and created.date() < datetime.strptime(since, "%Y-%m-%d").date():
                break
            continue

        total += 1
        month_key = created.strftime("%Y-%m")
        per_month[month_key] += 1
        wf_name = run.name or "unknown"
        per_workflow[wf_name]["total"] += 1

        if run.conclusion == "success":
            success += 1
            per_workflow[wf_name]["success"] += 1
        elif run.conclusion == "failure":
            failure += 1
            per_workflow[wf_name]["failure"] += 1
        else:
            other += 1

        if run.updated_at and run.created_at:
            dur = (run.updated_at - run.created_at).total_seconds()
            if dur > 0:
                durations.append(dur)

    total_duration_sec = sum(durations)
    avg_duration_sec = total_duration_sec / len(durations) if durations else 0
    success_rate = (success / total * 100) if total > 0 else 0

    return {
        "total": total,
        "success": success,
        "failure": failure,
        "other": other,
        "success_rate": round(success_rate, 1),
        "avg_duration_sec": avg_duration_sec,
        "total_duration_sec": total_duration_sec,
        "per_workflow": dict(per_workflow),
        "per_month": dict(sorted(per_month.items())),
    }
