import os
import streamlit as st

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from file_utils import split_files
from state_store import State, set_state

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


class Embedder:
    def __init__(self, repo_path, db_path):
        self.repo_path = repo_path
        self.db_path = db_path
        self.db = None
        self.retriever = None

    def load_db(self):
        embedding_function = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        if not os.path.exists(self.db_path):
            extension_freqs, document_chunks = split_files(self.repo_path)
            set_state(State.EXTENSION_FREQS, extension_freqs)
            self.db = Chroma.from_documents(
                documents=document_chunks,
                embedding=embedding_function,
                persist_directory=self.db_path,
            )
        else:
            print(f"loading db from directory: {self.db_path}")
            self.db = Chroma(
                persist_directory=self.db_path, embedding_function=embedding_function
            )

        self.retriever = self.db.as_retriever()
        self.retriever.search_kwargs["distance_metric"] = "cos"
        self.retriever.search_kwargs["fetch_k"] = 100
        self.retriever.search_kwargs["maximal_marginal_relevance"] = True
        self.retriever.search_kwargs["k"] = 10
