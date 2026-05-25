import pytest
from pydantic_ai.models.test import TestModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Set dummy API key before importing agent
import os
os.environ["OPENAI_API_KEY"] = "dummy"

from app.services.agent import agent, list_tables, get_table_metadata, execute_query
from pydantic_ai import ModelRetry

class Base(DeclarativeBase):
    pass

class DbTestTable(Base):
    __tablename__ = "db_test_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_list_tables_tool(db_session: Session):
    from pydantic_ai import RunContext
    # We use None for model/usage/prompt as they are not needed by the tool
    ctx = RunContext(deps=db_session, model=TestModel(), usage=None, prompt="test")
    
    tables = list_tables(ctx)
    assert "db_test_table" in tables

def test_get_table_metadata_tool(db_session: Session):
    from pydantic_ai import RunContext
    ctx = RunContext(deps=db_session, model=TestModel(), usage=None, prompt="test")
    
    columns = get_table_metadata(ctx, "db_test_table")
    assert any(c["name"] == "id" for c in columns)
    assert any(c["name"] == "name" for c in columns)

@pytest.mark.asyncio
async def test_agent_initialization():
    # Verify agent is initialized with correct types
    assert agent.deps_type == Session
    assert agent is not None

def test_execute_query_success(db_session: Session):
    from pydantic_ai import RunContext
    # Insert dummy data
    db_session.add(DbTestTable(id=1, name="Test Item"))
    db_session.commit()
    
    ctx = RunContext(deps=db_session, model=TestModel(), usage=None, prompt="test")
    
    results = execute_query(ctx, "SELECT * FROM db_test_table")
    assert len(results) == 1
    assert results[0]["name"] == "Test Item"

def test_execute_query_invalid_statement(db_session: Session):
    from pydantic_ai import RunContext
    ctx = RunContext(deps=db_session, model=TestModel(), usage=None, prompt="test")
    
    with pytest.raises(ModelRetry) as exc_info:
        execute_query(ctx, "DROP TABLE db_test_table")
    assert "Only SELECT queries are allowed" in str(exc_info.value)

def test_execute_query_db_error(db_session: Session):
    from pydantic_ai import RunContext
    ctx = RunContext(deps=db_session, model=TestModel(), usage=None, prompt="test")
    
    with pytest.raises(ModelRetry) as exc_info:
        # Querying a non-existent table
        execute_query(ctx, "SELECT * FROM non_existent_table")
    assert "Database error" in str(exc_info.value)
