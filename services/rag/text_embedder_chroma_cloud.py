import chromadb
from team_lens_v1.config import CHROMA_TENANT_ID, CHROMA_API_KEY

client = chromadb.CloudClient(
  api_key=CHROMA_API_KEY,
  tenant=CHROMA_TENANT_ID,
  database='team_lens_db_1_development'
)