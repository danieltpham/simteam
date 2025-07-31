from dataclasses import dataclass
from sqlalchemy.engine import Engine
from sqlalchemy import text
from openai import OpenAI
from pydantic_ai import Agent, RunContext
from pydantic_ai.settings import ModelSettings
from .agent_schema import SQLQuery, SQLResult

import os
import dotenv
dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Load custom prompt from prompt.txt ----
def load_prompt_from_file() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, "prompt.txt")
    with open(prompt_path, "r") as f:
        return f.read()

prompt_text = load_prompt_from_file()

# ---- Dependency Injection ----
@dataclass
class SQLDeps:
    engine: Engine

# ---- Agent Setup ----
sql_agent = Agent(
    model="openai:gpt-4.1-nano", #"openai:gpt-4o",
    deps_type=SQLDeps,
    output_type=SQLResult,
    system_prompt=prompt_text,
    model_settings=ModelSettings(
        temperature= 0,
        max_tokens= 1500,
        # stop_sequences=[";"]
    )
)

# ---- Tool to execute SQL ----
@sql_agent.tool
async def execute_sql(ctx: RunContext[SQLDeps], sql: str) -> str:
    """Execute the SQL query and return the result as a string."""
    try:
        with ctx.deps.engine.begin() as conn:
            result = conn.execute(text(sql)).fetchall()
        return str(result)
    except Exception as e:
        return f"SQL execution error: {e}"

# # ---- Optional dynamic table injection ----
# @sql_agent.system_prompt
# async def inject_schema_hint(ctx: RunContext[SQLDeps]) -> str:
#     with ctx.deps.engine.connect() as conn:
#         tables = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
#         table_list = [row[0] for row in tables]
#     return f"The database contains the following tables: {', '.join(table_list)}"
