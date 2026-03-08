import argparse
import os
import sys
from datetime import datetime

from dotenv import load_dotenv

from report import generate_report, write_report


def _fetch_gh_stat(name, fn, *args, **kwargs):
    """Call a GitHub stat function, returning None on failure."""
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        print(f"⚠ GitHub {name} stats failed: {e}")
        return None


def _build_local_data(repo, since, until):
    """Compute all stats from local git history."""
    from stats.commits import commits_per_month
    from stats.authors import commits_by_author_per_month
    from stats.messages import most_and_least_frequent_words
    from stats.times import commit_times_by_hour
    from stats.lovebirds import coauthored_commits
    from stats.lines import lines_by_author
    from stats.changes import most_changed_files
    from stats.weekdays import busiest_weekday
    from stats.streaks import longest_streak
    from stats.first_commits import first_time_contributors
    from stats.ownership import file_ownership

    author_monthly, author_totals = commits_by_author_per_month(repo, since=since, until=until)
    return {
        "commits_per_month": commits_per_month(repo, since=since, until=until),
        "author_monthly": author_monthly,
        "author_totals": author_totals,
        "words": most_and_least_frequent_words(repo, since=since, until=until),
        "hour_counts": commit_times_by_hour(repo, since=since, until=until),
        "file_changes": most_changed_files(repo, since=since, until=until),
        "lines": lines_by_author(repo, since=since, until=until),
        "coauthored": coauthored_commits(repo, since=since, until=until),
        "weekday_counts": busiest_weekday(repo, since=since, until=until),
        "streaks": longest_streak(repo, since=since, until=until),
        "new_contributors": first_time_contributors(repo, since=since, until=until),
        "ownership": file_ownership(repo, since=since, until=until),
    }


def _build_github_data(gh_repo, since, until):
    """Fetch everything from GitHub API."""
    from gh_stats.commits import fetch_commit_stats
    from gh_stats.pull_requests import pull_request_stats
    from gh_stats.issues import issue_stats
    from gh_stats.actions import actions_stats
    from gh_stats.contributors import contributor_stats

    data = fetch_commit_stats(gh_repo, since, until)
    data["gh_pull_requests"] = _fetch_gh_stat("PR", pull_request_stats, gh_repo, since, until)
    data["gh_issues"] = _fetch_gh_stat("issues", issue_stats, gh_repo, since, until)
    data["gh_actions"] = _fetch_gh_stat("actions", actions_stats, gh_repo, since, until)
    data["gh_contributors"] = _fetch_gh_stat("contributors", contributor_stats, gh_repo, since, until)
    return data


def main():
    load_dotenv()

    current_year = str(datetime.now().year)

    parser = argparse.ArgumentParser(description="Git repository statistics")
    parser.add_argument("--since", default=f"{current_year}-01-01",
                        help="Start date in YYYY-MM-DD format (default: Jan 1 of current year)")
    parser.add_argument("--until", default=None,
                        help="End date in YYYY-MM-DD format (default: now)")
    parser.add_argument("--repo", default="../itk_website",
                        help="Path to the git repository (default: ../itk_website)")
    parser.add_argument("--output", default="pystat_report.html",
                        help="Output HTML file path (default: pystat_report.html)")
    parser.add_argument("--github-repo", default=None,
                        help="GitHub repo slug (owner/repo). Auto-detected from remote if omitted.")
    parser.add_argument("--local", action="store_true",
                        help="Force local git history instead of GitHub API.")
    args = parser.parse_args()

    since = args.since
    until = args.until

    # Resolve repo name (from local path or GitHub slug)
    repo = None
    repo_path = None
    if os.path.isdir(args.repo):
        from repo_utils import load_repo
        repo = load_repo(args.repo)
        repo_path = os.path.abspath(args.repo)
    repo_name = args.github_repo or (os.path.basename(repo_path) if repo_path else "unknown")

    data = {}

    if not args.local:
        from gh_stats.client import is_available, get_github_client, get_github_repo, check_rate_limit, detect_github_repo

        if is_available():
            slug = args.github_repo or (detect_github_repo(repo) if repo else None)
            if slug:
                client = get_github_client()
                if client and check_rate_limit(client):
                    print(f"Fetching GitHub stats for {slug}...")
                    try:
                        gh_repo = get_github_repo(client, slug)
                        data = _build_github_data(gh_repo, since, until)
                        repo_name = slug.split("/")[-1]
                    except Exception as e:
                        print(f"⚠ GitHub failed: {e}")
            else:
                print("GitHub token found but could not detect repo slug. Use --github-repo owner/repo.")

    # Fallback to local git
    if not data:
        if repo is None:
            print("Error: no GitHub data and no local repo. Provide --repo or set GITHUB_TOKEN.")
            sys.exit(1)
        print("Using local git history." if args.local else "Falling back to local git history.")
        data = _build_local_data(repo, since, until)
        data.update({"gh_pull_requests": None, "gh_issues": None, "gh_actions": None, "gh_contributors": None})

    html = generate_report(data, repo_name, since, until, repo_path=repo_path)
    write_report(html, args.output)
    print(f"Report written to {args.output}")

if __name__ == "__main__":
    main()
