from repo_utils import load_repo  # Importing the load_repo function
from stats.commits import commits_per_month, commits_per_day
from stats.authors import commits_by_author_per_month, commits_by_author_per_day
from stats.messages import messages_per_author, most_frequent_words
from stats.branches import commits_in_branch
from stats.merges import merges_into_branch
from stats.times import commit_times_by_hour
from stats.commits_times import commits_over_time
from stats.lovebirds import coauthored_commits
from stats.lines import lines_by_author
from stats.changes import most_changed_files

def main():
    repo_path = "../itk_website"  # Replace with your Git repository path
    repo = load_repo(repo_path)

    # Commit stats
    print("\nCommits by author per month:")
    commits_by_author_per_month(repo)

    print("\nCommits by author per day in July 2024:")
    commits_by_author_per_day(repo, "2024-07")

    # Message stats
    print("\nMessages per author (2024):")
    # messages_per_author(repo, "2024")

    print("\nMost frequently used words in commit messages:")
    most_frequent_words(repo)

    # Branch stats
    # print("\nCommits in main branch:")
    # commits_in_branch(repo, "reception-express-staging")
    
    # Merge stats
    # print("\nMerges into reception-express:")
    # merges_into_branch(repo, "reception-express-staging")
     
    # Commit times by hour
    print("\nCommit times")
    commit_times_by_hour(repo)

    # Changes to a file
    print("\nCommits per file")
    most_changed_files(repo)

    # Most line changes
    print("\nLines per author")
    lines_by_author(repo)

    # Lovebirds
    print("\nLovebirds")
    coauthored_commits(repo)

    # Commits per month
    print("\nPer month")
    commits_per_month(repo)

if __name__ == "__main__":
    main()
