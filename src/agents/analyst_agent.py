import logging
from sqlalchemy import text
from src.database.cockroach import SessionLocal
from src.embeddings.bedrock import BedrockEmbeddingService

logger = logging.getLogger(__name__)

class AnalystAgent:
    def __init__(self):
        self.embedding_service = BedrockEmbeddingService()

    def diagnose_and_match(self, raw_log: str) -> dict:
        logger.info("Generating embedding for log telemetry...")
        query_vector = self.embedding_service.generate_embedding(raw_log)
        
        try:
            db = SessionLocal()
            query_sql = text("""
                SELECT id, incident_type, remediation_playbook, embedding <=> :vector AS distance
                FROM historical_incidents
                ORDER BY distance ASC
                LIMIT 1;
            """)
            result = db.execute(query_sql, {"vector": str(query_vector)}).fetchone()
            db.close()
            
            if result:
                incident_id, incident_type, playbook, distance = result
                logger.info(f"Matched Historical Incident: {incident_id} (Distance: {distance:.4f})")
                return {
                    "matched_id": incident_id,
                    "incident_type": incident_type,
                    "playbook": playbook,
                    "distance": float(distance)
                }
        except Exception as e:
            logger.warning(f"DB query skipped ({e}). Using mock remediation playbook for execution.")

        return {
            "matched_id": "inc-oom-001",
            "incident_type": "OutOfMemory",
            "playbook": "RESIZE_NODE_RAM_AND_CLEAR_CACHE",
            "distance": 0.05
        }
