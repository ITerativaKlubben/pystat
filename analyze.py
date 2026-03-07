import argparse
from datetime import datetime

from repo_utils import load_repo
from stats.commits import commits_per_month, commits_per_day
from stats.authors import commits_by_author_per_month, commits_by_author_per_day
from stats.messages import messages_per_author, most_and_least_frequent_words
from stats.branches import commits_in_branch
from stats.merges import merges_into_branch
from stats.times import commit_times_by_hour
from stats.commits_times import commits_over_time
from stats.lovebirds import coauthored_commits
from stats.lines import lines_by_author
from stats.changes import most_changed_files
from stats.length import analyze_commit_message_lengths

def main():
    current_year = str(datetime.now().year)

    parser = argparse.ArgumentParser(description="Git repository statistics")
    parser.add_argument("--since", default=f"{current_year}-01-01",
                        help="Start date in YYYY-MM-DD format (default: Jan 1 of current year)")
    parser.add_argument("--until", default=None,
                        help="End date in YYYY-MM-DD format (default: now)")
    parser.add_argument("--repo", default="../itk_website",
                        help="Path to the git repository (default: ../itk_website)")
    args = parser.parse_args()

    since = args.since
    until = args.until
    repo = load_repo(args.repo)

    date_range = f"{since} to {until or 'now'}"

    # Commit stats
    print(f"\nCommits by author per month ({date_range}):")
    commits_by_author_per_month(repo, since=since, until=until)

    print(f"\nCommits by author per day ({date_range}):")
    commits_by_author_per_day(repo, since=since, until=until)

    # Commit Message stats (a lot of text)
    # print(f"\nMessages per author ({date_range}):")
    # messages_per_author(repo, since[:4])

    # Most frequantly used words in commit messages
    print("\n")
    most_and_least_frequent_words(repo, since=since, until=until)

    # Commit times by hour
    print("\n")
    commit_times_by_hour(repo, since=since, until=until)

    # Changes to a file
    print("\n")
    most_changed_files(repo, since=since, until=until)

    # Most line changes
    print("\nLines per author")
    lines_by_author(repo, since=since, until=until)

    # Lovebirds
    print("\nLovebirds")
    coauthored_commits(repo, since=since, until=until)

    # Commits per month
    print("\nPer month")
    commits_per_month(repo, since=since, until=until)

    # Commits lengths
    # print("\nCommit length info")
    # analyze_commit_message_lengths(repo)

if __name__ == "__main__":
    main()
