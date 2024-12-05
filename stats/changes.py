from collections import Counter
from stats.visualization import plot_most_changed_files


def most_changed_files(repo):
    """Analyze and plot most frequently changed files."""
    file_changes = Counter()

    for commit in repo.iter_commits():
        for file in commit.stats.files.keys():
            file_changes[file] += 1
    
    print("Most frequently changed files:")
    for file, count in file_changes.most_common(10):
        print(f"{file}: {count} changes") 
    

