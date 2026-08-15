import os
import json
import psycopg
from psycopg.rows import dict_row
from src.utils.ccloud_wrapper import execute_ccloud_command

DATABASE_URL = os.getenv("DATABASE_URL")

def get_active_remediation(remediation_id: str):
    """Retrieves current remediation state from CockroachDB."""
    query = "SELECT * FROM active_remediations WHERE remediation_id = %s;"
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (remediation_id,))
            return cur.fetchone()

def update_remediation_status(remediation_id: str, status: str, current_step: int):
    """Updates status in CockroachDB active_remediations table."""
    query = """
        UPDATE active_remediations
        SET status = %s, current_step = %s, updated_at = now()
        WHERE remediation_id = %s;
    """
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (status, current_step, remediation_id))
            conn.commit()

def log_execution_audit(remediation_id: str, action: str, cmd: str, output: dict):
    """Appends an audit entry into CockroachDB execution_audit_log table."""
    query = """
        INSERT INTO execution_audit_log (remediation_id, agent_role, action_taken, ccloud_command_executed, output_summary)
        VALUES (%s, 'EXECUTOR_AGENT', %s, %s, %s);
    """
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (remediation_id, action, cmd, json.dumps(output)))
            conn.commit()

def execute_remediation_plan(remediation_id: str) -> dict:
    """Executes the action plan selected by the Analyst agent."""
    state = get_active_remediation(remediation_id)
    if not state:
        return {"error": "Remediation ID not found"}

    update_remediation_status(remediation_id, "EXECUTING", 2)
    
    # Example action step execution using ccloud wrapper
    cmd = "ccloud cluster list"
    cmd_result = execute_ccloud_command(cmd)
    
    log_execution_audit(
        remediation_id=remediation_id,
        action="INSPECT_CCLOUD_CLUSTERS",
        cmd=cmd,
        output=cmd_result
    )
    
    update_remediation_status(remediation_id, "COMPLETED", 3)
    
    return {
        "remediation_id": remediation_id,
        "final_status": "COMPLETED",
        "command_executed": cmd,
        "execution_output": cmd_result
    }
