import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from state_store import State, get_state


class QuestionContext:
    def __init__(self, repo_name, github_url, chat_history, extension_freqs):
        self.repo_name = repo_name
        self.github_url = github_url
        self.chat_history = chat_history
        self.extension_freqs = extension_freqs


def form_prompt_template():
    template = """
        Repo: {repo_name} ({github_url}) | Conv: {chat_history} | Q: {question} | FileCount: {extension_freqs} | Docs: {relevant_documents}

        Instr:
        1. Answer based on context/docs.
        2. Focus on repo/code.
        3. Consider:
            a. Purpose/features - describe.
            b. Functions/code - give details/samples.
            c. Setup/usage - give instructions.
        4. Unsure? Say "I'm not sure."

        Answer:
    """
    prompt_template = PromptTemplate(
        template=template,
        input_variables=[
            "repo_name",
            "github_url",
            "chat_history",
            "question",
            "extension_freqs",
            "relevant_documents",
        ],
    )
    return prompt_template


def get_answer(question, context: QuestionContext, retriever):
    chat_history = get_state(State.CHAT_HISTORY)
    print(f"chat_history: {chat_history}")
    print(f"extension_freqs: {context.extension_freqs}")

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)
    llm_chain = LLMChain(prompt=form_prompt_template(), llm=llm)

    relevant_documents = retriever.invoke(question)
    print(f"relevant_docs: {relevant_documents}")
    phrased_context = f"This question is about the GitHub repository '{context.repo_name}' available at {context.github_url}. The most relevant documents are:\n\n{relevant_documents}"

    answer = llm_chain.run(
        question=question,
        context=phrased_context,
        repo_name=context.repo_name,
        github_url=context.github_url,
        chat_history=context.chat_history,
        extension_freqs=context.extension_freqs,
        relevant_documents=relevant_documents,
    )
    return answer
