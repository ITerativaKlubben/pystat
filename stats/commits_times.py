def commits_over_time(repo):
    from collections import defaultdict

    commit_trends = defaultdict(int)
    for commit in repo.iter_commits():
        week = commit.committed_datetime.strftime("%Y-%W")
        commit_trends[week] += 1

    print("Commits over time (by week):")
    for week, count in sorted(commit_trends.items()):
        print(f"Week {week}: {count} commits")

