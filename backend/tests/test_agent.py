import pytest
from pydantic_ai.models.test import TestModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Set dummy API key before importing agent
import os
os.environ["OPENAI_API_KEY"] = "dummy"

from app.services.agent import agent, list_tables, get_table_metadata

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
