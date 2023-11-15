import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

class Embedder:
    def __init__(self, document_chunks):
        self.document_chunks = document_chunks
        self.embeddings = OpenAIEmbeddings(disallowed_special=())
        self.db = Chroma.from_documents(documents=self.document_chunks, embedding=self.embeddings)
        
        self.retriever = self.db.as_retriever()
        self.retriever.search_kwargs['distance_metric'] = 'cos'
        self.retriever.search_kwargs['fetch_k'] = 100
        self.retriever.search_kwargs['maximal_marginal_relevance'] = True
        self.retriever.search_kwargs['k'] = 10
        
        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=self.retriever)
        self.chat_history = []

    def get_answer(self, question):
        result = self.qa({'question': question, 'chat_history': self.chat_history})
        answer = result['answer']
        self.chat_history.append((question, answer))
        return answer    