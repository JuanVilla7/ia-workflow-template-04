import logging
import re
from typing import Any, Dict, List

from pydantic_ai import Agent, ModelRetry, RunContext
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.core.config import settings

logger = logging.getLogger("api.services.agent")

# Use model from settings
agent = Agent(
    settings.agent_model,
    deps_type=Session,
    instructions=(
        "You are a database analyst assistant. "
        "You have access to a database and can use tools to inspect its schema. "
        "Before answering questions about the data, you should understand the tables and their columns."
    ),
)


@agent.tool
def list_tables(ctx: RunContext[Session]) -> List[str]:
    """
    List all table names available in the database schema.
    """
    logger.debug("Tool call: list_tables")
    inspector = inspect(ctx.deps.get_bind())
    return inspector.get_table_names()


@agent.tool
def get_table_metadata(ctx: RunContext[Session], table_name: str) -> List[Dict[str, Any]]:
    """
    Get the column definitions and metadata for a specific table.

    Args:
        table_name: The name of the table to inspect.
    """
    logger.debug("Tool call: get_table_metadata for table=%s", table_name)
    inspector = inspect(ctx.deps.get_bind())
    columns = inspector.get_columns(table_name)
    
    # Convert SQLAlchemy types to strings for JSON serialization
    for col in columns:
        if "type" in col:
            col["type"] = str(col["type"])
            
    return columns


@agent.tool(retries=2)
def execute_query(ctx: RunContext[Session], query: str) -> List[Dict[str, Any]]:
    """
    Execute a SQL SELECT query and return the results as a list of dictionaries.
    Only SELECT statements are allowed for security reasons.
    Queries are limited to 100 rows by default.

    Args:
        query: The SQL SELECT query to execute.
    """
    logger.debug("Tool call: execute_query query=%s", query)

    # Security check: Only allow SELECT queries
    if not re.match(r"^\s*SELECT", query, re.IGNORECASE):
        raise ModelRetry("Only SELECT queries are allowed for security reasons.")

    try:
        # Execute the query
        result = ctx.deps.execute(text(query))
        # Fetch up to 100 rows and convert to list of dicts
        rows = result.mappings().fetchmany(100)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error("Error executing query: %s", str(e))
        raise ModelRetry(f"Database error: {str(e)}. Please correct your SQL and try again.")
