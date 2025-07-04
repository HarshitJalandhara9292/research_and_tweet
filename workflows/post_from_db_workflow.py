import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# print(sys.path)

from Agents.twitter_agent import TwitterAgent


def post_from_db_workflow(query):
    """Workflow to fetch relevant content from DB and post it to Twitter."""
    print("🚀 Starting Twitter Posting Workflow...")
    
    if not query:
        print("❌ No query provided. Exiting.")
        return
    
    print(f"🔍 Searching for articles related to: {query}")

    
    twitter_agent = TwitterAgent()
    twitter_agent.post_from_pinecone(query)

    print("✅ Workflow completed!")
