import matplotlib.pyplot as plt

def plot_commit_times_by_hour(hour_counts):
    """Plot commit activity by hour."""
    hours, counts = zip(*sorted(hour_counts.items()))
    plt.bar(hours, counts)
    plt.title("Commit Activity by Hour (Past Year)")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Commits")
    plt.xticks(range(0, 24))
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_lines_by_author(lines):
    """Plot lines changed by author."""
    authors, line_counts = zip(*lines.items())
    plt.barh(authors, line_counts)
    plt.title("Lines Added/Removed per Author")
    plt.xlabel("Number of Lines")
    plt.ylabel("Author")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_most_changed_files(file_changes):
    """Plot most frequently changed files."""
    files, counts = zip(*file_changes.most_common(10))
    plt.barh(files, counts)
    plt.title("Most Frequently Changed Files")
    plt.xlabel("Number of Changes")
    plt.ylabel("File")
    plt.tight_layout()
    plt.show()

def plot_commit_trends(commit_trends):
    """Plot commit trends over time."""
    dates, counts = zip(*sorted(commit_trends.items()))
    plt.plot(dates, counts, marker="o")
    plt.title("Commit Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

