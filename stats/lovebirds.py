def coauthored_commits(repo):
    coauthored_count = 0

    for commit in repo.iter_commits():
        if "Co-authored-by" in commit.message:
            coauthored_count += 1

    print(f"Co-authored commits: {coauthored_count}")

