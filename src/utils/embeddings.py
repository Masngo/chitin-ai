import json
import os
import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)

def get_titan_embedding(text: str) -> list[float]:
    """
    Generates 1536-dimensional vector embedding using Amazon Bedrock Titan Text V2.
    """
    model_id = "amazon.titan-embed-text-v2:0"
    payload = {
        "inputText": text,
        "dimensions": 1536,
        "normalize": True
    }
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )
        response_body = json.loads(response["body"].read())
        return response_body.get("embedding", [])
    except Exception as e:
        print(f"❌ Failed to invoke Bedrock Titan Embedding model: {str(e)}")
        # Return fallback zeros vector if offline or credentials missing
        return [0.0] * 1536
