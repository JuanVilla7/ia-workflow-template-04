import logging
from typing import Any, Dict, List

from pydantic_ai import Agent, RunContext
from sqlalchemy import inspect
from sqlalchemy.orm import Session

logger = logging.getLogger("api.services.agent")

# We'll use a placeholder model. In a real scenario, this would come from settings.
# Pydantic AI expects 'provider:model-name'
agent = Agent(
    "openai:gpt-4o",
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
    return inspector.get_columns(table_name)
