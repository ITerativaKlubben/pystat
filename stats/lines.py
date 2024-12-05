from collections import defaultdict

def lines_by_author(repo):
    """Print the number of lines added and removed by each author."""
    lines_stats = defaultdict(lambda: {"added": 0, "removed": 0})

    for commit in repo.iter_commits():
        author = commit.author.name
        stats = commit.stats

        # Sum lines added and removed
        for file_stat in stats.files.values():
            lines_stats[author]["added"] += file_stat["insertions"]
            lines_stats[author]["removed"] += file_stat["deletions"]

    print("Lines added and removed per author:")
    for author, stats in lines_stats.items():
        print(f"{author}: {stats['added']} lines added, {stats['removed']} lines removed")

