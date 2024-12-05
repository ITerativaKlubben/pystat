def commits_in_branch(repo, branch_name):
    """Print commits in a specific branch."""
    branch_commits = list(repo.iter_commits(branch_name))

    print(f"Commits in branch {branch_name}:")
    for commit in branch_commits:
        print(f"{commit.hexsha} - {commit.author.name}: {commit.message.strip()}")

def compare_branch_activity(repo, branches):
    """Compare commit activity across branches."""
    branch_activity = {}

    for branch in branches:
        branch_activity[branch] = len(list(repo.iter_commits(branch)))

    print("Branch activity comparison:")
    for branch, count in sorted(branch_activity.items(), key=lambda x: x[1], reverse=True):
        print(f"{branch}: {count} commits")

