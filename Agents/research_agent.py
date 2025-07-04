import os
import logging
from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.googlesearch import GoogleSearch
from dotenv import load_dotenv
from Tools.vector_database import PineconeDB  # Using Pinecone now
from sentence_transformers import SentenceTransformer
from phi.model.google import Gemini
import sys
# print(sys.path)

load_dotenv()

class ResearchAgent:   
    def __init__(self):
        """Initialize the Research Agent with tools and Pinecone connection."""
        self.agent = Agent(
            model=Gemini(id="gemini-1.5-flash"),
            tools=[DuckDuckGo(), GoogleSearch()],
            description="A research agent that finds and extracts trending news articles.",
            instructions=[
                "Search for the latest AI trends.",
                "Search for AI news and return results as JSON.",
                "Summarize the first 3 paragraphs of each article and highlight key facts.",
                "Extract the names of people mentioned in the articles.",
                "Analyze the tone of each article to understand its target audience and key message.",
                "Generate a 140-character tweet summarizing the most important point from each article.",
                "Check for credibility of each article, ensuring they are sourced from trusted platforms.",
                "Categorize articles into themes such as 'Artificial Intelligence', 'Technology Trends', 'Healthcare', etc.",
                "Store and organize the summarized content in a structured format for easy retrieval.",
                "Based on the content, suggest 3 potential blog post ideas on the latest trends in AI."
            ],
            markdown=True,
            show_tool_calls=True,

        )
        
        self.db_tool = PineconeDB()
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  
        print("✅ Pinecone vector database initialized.")

    def search_and_store(self, query):
        """Search trending news and store relevant articles in Pinecone vector database."""
        print(f"🔍 Searching for: {query}")

        search_tool = DuckDuckGo()
        extract_tool = GoogleSearch()

        search_results = eval(search_tool.duckduckgo_search(query, max_results=5))

        if not search_results:
            print("❌ No search results found.")
            return

        for result in search_results:
            url = result.get("href", "").strip()
            title = result.get("title", "").strip()

            if not url or not title:
                print(f"⚠️ Skipping invalid article (missing title or URL): {result}")
                continue

            print(f"📄 Processing article: {title} ({url})")

            if self.db_tool.article_exists(url):
                print(f"⚠️ Duplicate article skipped: {title}")
                continue

            try:
                content = extract_tool.google_search(url).strip()
            except Exception as e:
                print(f"❌ Error extracting content from {url}: {e}")
                continue

            if not content:
                print(f"⚠️ Skipping empty content for: {title}")
                continue

            embedding = self.embedding_model.encode(content, convert_to_numpy=True)

            try:
                self.db_tool.insert_article(query, title, content, url, embedding)
                print(f"✅ Stored article in Pinecone: {title} ({url})")
            except Exception as e:
                print(f"❌ Error inserting article {title}: {e}")

        print("✅ Data storage completed!")

