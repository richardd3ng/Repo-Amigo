# Repo Amigo

This web app is a tool for asking questions about GitHub repositories leveraging LangChain and OpenAI's GPT-3.5-turbo language model!

<img width="635" alt="image" src="https://github.com/richardd3ng/Repo-Amigo/assets/73263775/3e9e0a3a-1166-46ed-abc7-3e42b206f751">


## Try it out!

https://repo-amigo.streamlit.app/

## Key Features
- Login via GitHub OAuth2.0 to clone public GitHub repositories
- Indexes files and stores embeddings in a ChromaDB vector database.
- Supports a variety of file formats, including text, code, and Jupyter Notebooks.
- Produces in-depth responses to user inquiries derived from repository files.
- Leverages OpenAI's language model to craft replies.
- Provides key documents most pertinent to each query.
