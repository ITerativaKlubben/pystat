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

def most_frequent_words(repo):
    """Print the most frequently used words in commit messages."""
    word_counter = Counter()

    for commit in repo.iter_commits():
        words = re.findall(r'\b\w+\b', commit.message.lower())
        word_counter.update(words)

    print("Most frequently used words in commit messages:")
    for word, count in word_counter.most_common(10):
        print(f"{word}: {count}")

