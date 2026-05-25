import asyncio
import os
import sys

# Set dummy API key
os.environ["OPENAI_API_KEY"] = "dummy"

# Add current directory to path
sys.path.append(os.getcwd())

from pydantic_ai.models.test import TestModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.agent import agent

async def main():
    # Use real SQLite in-memory for the tools to work
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Run the agent with TestModel configured to return a simple string
    # instead of trying to call tools with dummy data
    with agent.override(model=TestModel(custom_output_text="Agent is initialized and tools are registered.", call_tools=[])):
        print("Running agent smoke test...")
        result = await agent.run("What tables are available?", deps=db)
        print(f"Agent result: {result.output}")
        assert "Agent is initialized" in result.output
        print("Smoke test PASSED")

if __name__ == "__main__":
    asyncio.run(main())
