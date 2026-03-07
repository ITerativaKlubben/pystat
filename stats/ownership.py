from collections import defaultdict, Counter
from datetime import datetime

def file_ownership(repo, since="2024-01-01", until=None, top_n=15):
    """Print who has touched each file the most."""
    since_date = datetime.strptime(since, "%Y-%m-%d")
    until_date = datetime.strptime(until, "%Y-%m-%d") if until else None
    file_authors = defaultdict(Counter)

    for commit in repo.iter_commits(since=since_date, until=until_date):
        author = commit.author.name
        for file in commit.stats.files.keys():
            file_authors[file][author] += 1

    if not file_authors:
        print("No commits found in the given date range.")
        return

    # Sort files by total touches, show top N
    sorted_files = sorted(file_authors.items(), key=lambda x: sum(x[1].values()), reverse=True)

    print(f"File ownership (top {top_n} most touched files):")
    for file, authors in sorted_files[:top_n]:
        top_author = authors.most_common(1)[0]
        total = sum(authors.values())
        print(f"  {file} ({total} changes) - top contributor: {top_author[0]} ({top_author[1]})")
