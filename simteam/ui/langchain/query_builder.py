from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from sqlalchemy.engine import Engine
from langchain_core.prompts import PromptTemplate

import os, dotenv
dotenv.load_dotenv()


def get_custom_sql_prompt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, 'prompt.txt')
    with open(prompt_path, 'r') as f:
        prompt = f.read()
    return PromptTemplate.from_template(prompt)

def get_sql_chain(engine: Engine) -> tuple[SQLDatabaseChain, SQLDatabase, ChatOpenAI]:
    db = SQLDatabase(engine)
    
    llm = ChatOpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        model="gpt-4.1-nano",
        temperature=0,
        max_tokens=1500, # type: ignore
        stop=[";"] # type: ignore
    )
    
    prompt = get_custom_sql_prompt()
    chain = SQLDatabaseChain.from_llm(
        llm=llm,
        db=db,
        prompt=prompt,
        return_intermediate_steps=True,
        verbose=True,
    )

    return chain, db, llm
