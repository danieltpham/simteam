from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

def get_summary_chain(llm) -> Runnable:
    prompt = PromptTemplate.from_template("""
    Based on the following SQL result, answer the user question:
    Question: {question}
    SQL Result: {result}
    """)
    return prompt | llm
