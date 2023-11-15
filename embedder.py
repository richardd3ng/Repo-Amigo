import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, NotebookLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

class Embedder:
    def __init__(self, repo_path, db_path):
        self.repo_path = repo_path
        self.db_path = db_path
        self.chat_history = []

    def load_db(self):
        embeddings = OpenAIEmbeddings(disallowed_special=())
        if not os.path.exists(self.db_path):
            document_chunks = self._split_documents()
            self.db = Chroma.from_documents(documents=document_chunks, embedding=embeddings, persist_directory=self.db_path)  
        else:
            self.db = Chroma(persist_directory=self.db_path, embedding_function=embeddings)
        
        self.retriever = self.db.as_retriever()
        self.retriever.search_kwargs['distance_metric'] = 'cos'
        self.retriever.search_kwargs['fetch_k'] = 100
        self.retriever.search_kwargs['maximal_marginal_relevance'] = True
        self.retriever.search_kwargs['k'] = 10

    def get_answer(self, question):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=self.retriever)
        result = qa({'question': question, 'chat_history': self.chat_history})
        answer = result['answer']
        self.chat_history.append((question, answer))
        return answer    
    
    def _split_documents(self):
        document_chunks = []
        for dir_path, _, file_names in os.walk(self.repo_path):
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
                except Exception as e:
                    pass # TODO: figure out if possible/helpful to load images and other file types
        return document_chunks