import os
import pinecone
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class PineconeDB:
    def __init__(self):
        """Initialize Pinecone vector database."""
        self.pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        index_name = "news-articles"
        if index_name not in self.pc.list_indexes().names():
            print(f"🚀 Creating new Pinecone index: {index_name}...")
            self.pc.create_index(
        name="news-articles",
        dimension=384,  
        metric="cosine",
        spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
        )
        print("✅ Pinecone index created!")
        self.index = self.pc.Index(index_name)

    def insert_article(self, query, title, content, url, embedding):
        """Store article content and embedding in Pinecone."""
        vector_id = url  
        metadata = {"title": title, "query": query, "url": url}
        self.index.upsert([(vector_id, embedding.tolist(), metadata)])

    def article_exists(self, url):
        """Check if article already exists in Pinecone."""
        result = self.index.fetch([url])
        return bool(result.get("vectors"))

    def search_similar_articles(self, query, embedding, top_k=5):
        """Find similar articles based on intent."""
        results = self.index.query(vector=embedding.tolist(), top_k=top_k, include_metadata=True)
        return results["matches"]





