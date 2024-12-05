def analyze_commit_message_lengths(repo):
    """Analyze the longest, shortest, and average commit message lengths, excluding merges and squash commits."""
    commit_lengths = []
    commit_messages = []

    for commit in repo.iter_commits():
        # Exclude merge commits based on the number of parents
        if len(commit.parents) > 1:
            continue

        # Combine the commit message head and body
        full_message = f"{commit.summary} {commit.message}".strip()

        # Skip squash commits based on keywords
        if "squash" in full_message.lower() or "merge" in full_message.lower():
            continue

        commit_lengths.append(len(full_message))
        commit_messages.append(full_message)

    if not commit_lengths:
        print("No commits found (or all were merges/squash commits).")
        return

    # Calculate longest, shortest, and average lengths
    longest = max(commit_lengths)
    shortest = min(commit_lengths)
    average = sum(commit_lengths) / len(commit_lengths)

    print(f"Longest commit message length: {longest}")
    print(f"Shortest commit message length: {shortest}")
    print(f"Average commit message length: {average:.2f}")

    # Find the actual longest and shortest messages
    longest_message = commit_messages[commit_lengths.index(longest)]
    shortest_message = commit_messages[commit_lengths.index(shortest)]

    print("\nLongest Commit Message:")
    print(f"Length: {longest}\nMessage:\n{longest_message}")

    print("\nShortest Commit Message:")
    print(f"Length: {shortest}\nMessage:\n{shortest_message}")
