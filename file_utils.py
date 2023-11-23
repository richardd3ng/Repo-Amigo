import git
import os
import re
import shutil


def clone_repo(github_url, repo_path, access_token):
    if os.path.exists(repo_path):
        return
    if "github.com" not in github_url:
        raise Exception("Invalid GitHub URL")
    try:
        parts = re.split(r"(github\.com)", github_url)
        url_with_token = f"{parts[0]}{access_token}@{parts[1]}{parts[2]}"
        print(f"url with token: {url_with_token}")
    except:
        raise Exception("Invalid GitHub URL")
    git.Repo.clone_from(url_with_token, repo_path)


def delete_repo(repo_path):
    if not os.path.exists(repo_path):
        return
    shutil.rmtree(repo_path)
