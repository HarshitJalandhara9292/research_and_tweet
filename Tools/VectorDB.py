import typer
from typing import List,Optional
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import pgvector2

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

Knowledge_base=PDFUrlKnowledgeBase(
    urls=[""],
    vector_db=pgvector2(collection="ai",db_url=db_url)
)

Knowledge_base.load()

storage=PgAssistantStorage(table_name="pdf_assistant",db_url=db_url)
