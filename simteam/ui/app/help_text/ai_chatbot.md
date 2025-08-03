### AI Assistant

Ask questions about your organisation in natural language — no need to write SQL.

1. Converts your question into SQL using a custom [prompt-engineered](https://github.com/danieltpham/simteam/blob/main/simteam/ui/pydanticai/prompt.txt) LLM
2. Executes the query against the **live organisational database**
3. Returns a plain-language answer and, optionally, the raw SQL for transparency

### Important Notes

* The assistant is **stateless**: it does *not* remember previous questions or context.
* It has been **prompt-engineered** for safe, read-only SQL only:
  * No `DELETE`, `DROP`, `INSERT`, `UPDATE`, or multi-statement queries
  * Attempts to trick or override the bot (e.g. “ignore instructions…”) are blocked
* You’re welcome to test its **robustness** using edge cases or misleading prompts — the system is designed to fail safely and log potentially malicious requests.
* Use the expander below each response to view the generated SQL.
