from collections import defaultdict, Counter
import re

def messages_per_author(repo, year):
    """Print commit messages grouped by author for a specific year."""
    messages_per_author = defaultdict(list)

    for commit in repo.iter_commits():
        if commit.committed_datetime.strftime("%Y") == year:
            author = commit.author.name
            messages_per_author[author].append(commit.message.strip())

    for author, messages in messages_per_author.items():
        print(f"{author}:")
        for message in messages:
            print(f"  - {message}")

def most_and_least_frequent_words(repo):
    """Print the most and least frequently used words in commit messages."""
    word_counter = Counter()
    most_common_count=10
    least_common_count=10

    for commit in repo.iter_commits():
        words = re.findall(r'\b\w+\b', commit.message.lower())  # Extract words
        word_counter.update(words)

    print(f"Most frequently used words in commit messages (Top {most_common_count}):")
    for word, count in word_counter.most_common(most_common_count):
        print(f"{word}: {count}")

    # Get the least common words by reversing the sorted list of items
    filtered_least_common_words = [
        (word, count) for word, count in sorted(word_counter.items(), key=lambda x: x[1])
        if not word.isdigit()
    ][:least_common_count]

    print(f"\nLeast frequently used words in commit messages (Top {least_common_count}, excluding numbers):")
    for word, count in filtered_least_common_words:
        print(f"{word}: {count}")
