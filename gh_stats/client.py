import os
import re
from datetime import datetime

from github import Github, Auth


def is_available():
    """Check if GITHUB_TOKEN is set in the environment."""
    return bool(os.environ.get("GITHUB_TOKEN"))


def get_github_client():
    """Return an authenticated Github instance."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    return Github(auth=Auth.Token(token))


def get_github_repo(client, slug):
    """Return a github.Repository object for the given owner/repo slug."""
    return client.get_repo(slug)


def check_rate_limit(client):
    """Check rate limit. Warn if low, return False if < 10 remaining."""
    rate_limit = client.get_rate_limit()
    rate = rate_limit.rate
    remaining = rate.remaining
    if remaining < 10:
        print(f"⚠ GitHub API rate limit critically low: {remaining} remaining. Skipping GitHub stats.")
        return False
    if remaining < 100:
        print(f"⚠ GitHub API rate limit low: {remaining}/{rate.limit} remaining.")
    return True


def in_date_range(dt, since=None, until=None):
    """Check if a datetime falls within the given date range (inclusive)."""
    if dt is None:
        return False
    # Handle timezone-aware datetimes by comparing date strings
    if hasattr(dt, 'date'):
        dt_date = dt.date()
    else:
        dt_date = dt

    if since:
        since_date = datetime.strptime(since, "%Y-%m-%d").date()
        if dt_date < since_date:
            return False
    if until:
        until_date = datetime.strptime(until, "%Y-%m-%d").date()
        if dt_date > until_date:
            return False
    return True


def detect_github_repo(repo):
    """Auto-detect owner/repo slug from git remote URL.

    Handles both SSH (git@github.com:owner/repo.git) and
    HTTPS (https://github.com/owner/repo.git) formats.
    Returns 'owner/repo' or None.
    """
    try:
        url = repo.remotes.origin.url
    except (AttributeError, IndexError):
        return None

    # SSH format: git@github.com:owner/repo.git
    m = re.match(r"git@github\.com:(.+/.+?)(?:\.git)?$", url)
    if m:
        return m.group(1)

    # HTTPS format: https://github.com/owner/repo.git
    m = re.match(r"https?://github\.com/(.+/.+?)(?:\.git)?$", url)
    if m:
        return m.group(1)

    return None
