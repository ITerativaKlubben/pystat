from repo_utils import load_repo  # Importing the load_repo function
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
    repo_path = "../itk_website"  # Replace with your Git repository path
    repo = load_repo(repo_path)

    # Commit stats
    print("\nCommits by author per month:")
    commits_by_author_per_month(repo, since="2024-01-01")

    print("\nCommits by author per day in July 2024:")
    commits_by_author_per_day(repo, "2024-07", since="2024-01-01")

    print("\nCommits by author per day in August 2024:")
    commits_by_author_per_day(repo, "2024-08", since="2024-01-01")

    # Commit Message stats (a lot of text)
    # print("\nMessages per author (2024):")
    # messages_per_author(repo, "2024")

    # Most frequantly used words in commit messages 
    print("\n")
    most_and_least_frequent_words(repo)

    # Commit times by hour
    print("\n")
    commit_times_by_hour(repo)

    # Changes to a file   
    print("\n")
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
    
    # Commits lengths
    # print("\nCommit length info")
    # analyze_commit_message_lengths(repo)

if __name__ == "__main__":
    main()
