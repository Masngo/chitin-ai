import json
import logging
import random
from config.settings import settings

logger = logging.getLogger(__name__)

class BedrockEmbeddingService:
    def __init__(self):
        try:
            import boto3
            self.client = boto3.client(
                service_name="bedrock-runtime",
                region_name=settings.AWS_REGION
            )
            self.model_id = settings.AWS_BEDROCK_MODEL_ID
            self.has_aws = True
        except Exception:
            self.has_aws = False

    def generate_embedding(self, text_content: str) -> list[float]:
        if self.has_aws:
            try:
                import boto3
                body = json.dumps({
                    "inputText": text_content,
                    "dimensions": 1536,
                    "normalize": True
                })
                response = self.client.invoke_model(
                    body=body,
                    modelId=self.model_id,
                    accept="application/json",
                    contentType="application/json"
                )
                response_body = json.loads(response.get("body").read())
                return response_body.get("embedding")
            except Exception as e:
                logger.warning(f"AWS Bedrock call failed ({e}). Falling back to mock vector embedding.")

        # Fallback deterministic pseudo-embedding vector of dimension 1536 for offline/local test runs
        random.seed(hash(text_content) % 1000000)
        return [round(random.uniform(-1.0, 1.0), 6) for _ in range(1536)]
