from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    COCKROACH_DATABASE_URL: str = "postgresql://root@localhost:26257/chitin_db?sslmode=disable"
    COCKROACH_MCP_SERVER_URL: str = "https://cockroachlabs.cloud/mcp"
    AWS_REGION: str = "us-east-1"
    AWS_BEDROCK_MODEL_ID: str = "amazon.titan-embed-text-v2:0"

    class Config:
        env_file = ".env"

settings = Settings()
