from collections import Counter
from stats.visualization import plot_most_changed_files


def most_changed_files(repo):
    """Analyze and plot most frequently changed files."""
    file_changes = Counter()

    for commit in repo.iter_commits():
        for file in commit.stats.files.keys():
            file_changes[file] += 1

    plot_most_changed_files(file_changes)

