from .agent_schema import SQLResult

# Ensure project root is in the path (3 levels up from this file)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
print("🔍 sys.path = ", sys.path)

async def get_sql_response(prompt: str) -> SQLResult:
    from .sql_agent import sql_agent, SQLDeps
    from simteam.server.db.session import Session

    db = Session()
    engine = db.get_bind()
    deps = SQLDeps(engine=engine) # type: ignore

    result = await sql_agent.run(prompt, deps=deps)
    return result.output