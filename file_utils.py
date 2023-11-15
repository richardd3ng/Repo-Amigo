import git
import os
import shutil

def clone_repo(github_url, repo_path):
    if os.path.exists(repo_path):
        return
    git.Repo.clone_from(github_url, repo_path)

def delete_repo(repo_path):
    if not os.path.exists(repo_path):
        return
    shutil.rmtree(repo_path)

