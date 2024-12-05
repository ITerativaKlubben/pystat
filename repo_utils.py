from git import Repo

def load_repo(repo_path):
    """Load a Git repository."""
    try:
        repo = Repo(repo_path)
        if repo.bare:
            raise Exception("Repository is bare")
        return repo
    except Exception as e:
        print(f"Error loading repo: {e}")
        exit(1)

