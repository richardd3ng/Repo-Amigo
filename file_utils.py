import git
import os
import shutil

from langchain.document_loaders import TextLoader, NotebookLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def clone_repo(github_url, repo_path):
    git.Repo.clone_from(github_url, repo_path)

def delete_repo(repo_path):
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

def split_documents(repo_path):
    document_chunks = []
    for dir_path, _, file_names in os.walk(repo_path):
        for file in file_names:
            file_path = os.path.join(dir_path, file)
            ext = os.path.splitext(file)[1]
            loader = None
            try:
                if ext == '.ipynb':
                    loader = NotebookLoader(file_path, include_outputs=True, max_output_length=20, remove_newline=True)
                else:
                    loader = TextLoader(file_path, encoding='utf-8')
                    document_chunks.extend(loader.load_and_split(
                        text_splitter=RecursiveCharacterTextSplitter(chunk_size=250)
                    ))
            except Exception:
                pass
    return document_chunks
