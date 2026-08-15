import os
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL")

class StateManager:
    """Handles transactional reads/writes for multi-agent synchronization in CockroachDB."""
    
    @staticmethod
    def fetch_audit_trail(remediation_id: str) -> list[dict]:
        query = """
            SELECT audit_id, agent_role, action_taken, ccloud_command_executed, executed_at 
            FROM execution_audit_log 
            WHERE remediation_id = %s 
            ORDER BY executed_at ASC;
        """
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (remediation_id,))
                return cur.fetchall()
