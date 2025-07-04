import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# print(sys.path)

from Agents.research_agent import ResearchAgent

def research_workflow(query):
    """Run the research workflow to search for news and store it in Pinecone."""
    print(f"🚀 Starting research workflow for query: {query}")

    research_agent = ResearchAgent()
    research_agent.search_and_store(query)

    print("✅ Research workflow completed!")

if __name__ == "__main__":
    # Example usage
    user_query = input("🔍 Enter your search query: ")
    research_workflow(user_query)



