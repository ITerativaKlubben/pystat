def merges_into_branch(repo, branch_name):
    """List merge commits into a specific branch."""
    try:
        branch_commits = list(repo.iter_commits(branch_name))
        print(f"Merge commits in branch '{branch_name}':")

        for commit in branch_commits:
            if len(commit.parents) > 1:  # Merge commits have more than one parent
                # Split message into title and description
                message_lines = commit.message.strip().split("\n", 1)
                title = message_lines[0]  # First line is the title
                description = message_lines[1].strip() if len(message_lines) > 1 else "No description"
                print(f"- {title}\n  Description: {description}\n")

    except Exception as e:
        print(f"Error: Unable to retrieve merges for branch '{branch_name}'. {e}")

