from datetime import datetime


def contributor_stats(gh_repo, since=None, until=None):
    """Gather GitHub contributor profiles for authors active in the date range."""
    since_dt = datetime.strptime(since, "%Y-%m-%d") if since else None
    until_dt = datetime.strptime(until, "%Y-%m-%d") if until else None

    # Find logins active in the date range
    kwargs = {}
    if since_dt:
        kwargs["since"] = since_dt
    if until_dt:
        kwargs["until"] = until_dt

    active_logins = set()
    for commit in gh_repo.get_commits(**kwargs):
        if commit.author:
            active_logins.add(commit.author.login)

    # Get full profile data, filtered to active contributors
    contributors = []
    for c in gh_repo.get_contributors():
        if c.login in active_logins:
            contributors.append({
                "login": c.login,
                "avatar_url": c.avatar_url,
                "name": c.name or c.login,
                "contributions": c.contributions,
                "profile_url": c.html_url,
            })

    return {
        "total": len(contributors),
        "contributors": contributors,
    }
