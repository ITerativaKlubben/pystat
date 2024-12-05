from collections import defaultdict

def commits_by_author_per_month(repo):
    """Print commit counts grouped by author and month."""
    commits_by_author_per_month = defaultdict(lambda: defaultdict(int))

    for commit in repo.iter_commits():
        month = commit.committed_datetime.strftime("%Y-%m")
        author = commit.author.name
        commits_by_author_per_month[month][author] += 1

    for month, authors in sorted(commits_by_author_per_month.items()):
        print(f"{month}:")
        for author, count in authors.items():
            print(f"  {author}: {count}")

def commits_by_author_per_day(repo, month):
    """Print commit counts grouped by author and day for a specific month."""
    commits_by_author_per_day = defaultdict(lambda: defaultdict(int))

    for commit in repo.iter_commits():
        day = commit.committed_datetime.strftime("%Y-%m-%d")
        if day.startswith(month):
            author = commit.author.name
            commits_by_author_per_day[day][author] += 1

    for day, authors in sorted(commits_by_author_per_day.items()):
        print(f"{day}:")
        for author, count in authors.items():
            print(f"  {author}: {count}")

