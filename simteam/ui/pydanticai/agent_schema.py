from pydantic import BaseModel, Field

class SQLQuery(BaseModel):
    question: str = Field(description="Natural language question about the data")

class SQLResult(BaseModel):
    sql: str = Field(description="The SQL generated to answer the question")
    result: str = Field(description="Stringified SQL result to be summarised")
