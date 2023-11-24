class QuestionContext:
    def __init__(self, repo_name, github_url, chat_history, extension_freqs):
        self.repo_name = repo_name
        self.github_url = github_url
        self.chat_history = chat_history
        self.extension_freqs = extension_freqs


def ask_question(question, context: QuestionContext, llm_chain, retriever):
    relevant_documents = retriever.invoke(question)
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
