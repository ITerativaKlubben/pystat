from collections import Counter

def lines_by_author(repo):
    """Print the number of lines added/removed by each author."""
    lines = Counter()

    for commit in repo.iter_commits():
        author = commit.author.name
        stats = commit.stats
        lines[author] += stats.total["lines"]

    print("Lines added/removed per author:")
    for author, count in lines.most_common():
        print(f"{author}: {count} lines")

