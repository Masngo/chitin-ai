import uuid
import click
import logging
from src.database.cockroach import init_db
from src.agents.executor_agent import ExecutorAgent if 'ExecutorAgent' in globals() else None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@click.group()
def cli():
    """Chitin.ai - Indestructible Agentic Memory CLI"""
    pass

@cli.command()
def setup():
    """Initialize DB schemas and vector indexes."""
    init_db()

if __name__ == '__main__':
    cli()
