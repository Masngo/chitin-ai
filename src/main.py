import uuid
import click
import logging
from src.database.cockroach import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@click.group()
def cli():
    """Chitin.ai - Indestructible Agentic Memory CLI"""
    pass

@cli.command()
def setup():
    """Initialize DB schemas and vector indexes."""
    init_db()

@cli.command()
@click.option('--log', prompt='Raw CloudWatch Log', help='Event log from CloudWatch')
@click.option('--cluster', prompt='Cluster ID', help='Target Cluster ID')
@click.option('--remediation-id', default=None, help='Existing remediation ID')
def run(log: str, cluster: str, remediation_id: str):
    """Run infrastructure incident remediation workflow."""
    from src.agents.analyst_agent import AnalystAgent
    from src.agents.executor_agent import ExecutorAgent

    rem_id = remediation_id or f"rem-{uuid.uuid4().hex[:8]}"
    analyst = AnalystAgent()
    executor = ExecutorAgent()

    click.echo(f"\n--- Initiating Chitin.ai Workflow [{rem_id}] ---")
    
    match = analyst.diagnose_and_match(log)
    if "error" in match:
        click.echo("Failed to match incident.")
        return

    executor.execute_remediation_plan(
        remediation_id=rem_id,
        cluster_id=cluster,
        playbook=match["playbook"]
    )

if __name__ == '__main__':
    cli()
