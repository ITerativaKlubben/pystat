import argparse
import os
from datetime import datetime

from repo_utils import load_repo
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
from report import generate_report, write_report

def main():
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
    args = parser.parse_args()

    since = args.since
    until = args.until
    repo = load_repo(args.repo)
    repo_name = os.path.basename(os.path.abspath(args.repo))

    author_monthly, author_totals = commits_by_author_per_month(repo, since=since, until=until)

    data = {
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

    html = generate_report(data, repo_name, since, until, repo_path=os.path.abspath(args.repo))
    write_report(html, args.output)
    print(f"Report written to {args.output}")

if __name__ == "__main__":
    main()
