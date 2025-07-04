import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflows.research_workflow import research_workflow
from workflows.post_from_db_workflow import post_from_db_workflow


def main():
    print("🚀 Starting Multi-Agent System...")

    search_query = input("🔍 Enter your search query: ")

    research_workflow(search_query)

    time.sleep(2)

    post_from_db_workflow(search_query)

    print("✅ End-to-end workflow completed!")


if __name__ == "__main__":
    main()








'''
import time
from Agents.research_agent import ResearchAgent
from Agents.twitter_agent import TwitterAgent
# from config.settings import SEARCH_QUERY

def main():
    print("🚀 Starting Multi-Agent System...")

    # Step 1: Research Agent fetches news and stores it
    research_agent = ResearchAgent()
    search_query = input("🔍 Enter your search query: ")
    
    print(f"📰 Researching: {search_query}")
    research_agent.search_and_store(search_query)

    print("✅ Research completed! Articles stored in database.\n")
    
    # Small delay before fetching the news
    time.sleep(2)

    # Step 2: Twitter Agent fetches stored news and posts it
    twitter_agent = TwitterAgent()
    print("🐦 Fetching news from the database and posting on Twitter...")
    twitter_agent.post_from_pinecone(search_query)

    print("✅ Workflow completed!")

if __name__ == "__main__":
    main()
'''





















# # The main.py script orchestrates the entire process of searching for news articles based on a user query, storing them in a database, and posting them to Twitter. It interacts with the ResearchWorkflow and PostFromDBWorkflow classes to handle the search and post operations. The main function collects user input, runs the research workflow, displays the search results, and then posts the articles to Twitter. This script serves as the entry point for the news search engine application.

# from workflows.research_workflow import ResearchWorkflow
# from workflows.post_from_db_workflow import post_from_db_workflow

# def main():
#     print("🚀 News Search Engine")
    
#     # Step 1: Get user input for the topic
#     query = input("Enter a topic to search: ")  # User input
    
#     # Step 2: Run the research workflow to find and store articles
#     workflow = ResearchWorkflow()
#     results = workflow.run(query)

#     print("\n📌 Found Articles:")
#     for article in results:
#         title = article[0]  # Title is the first element (index 0)
#         url = article[2]    # URL is the third element (index 2)
#         print(f"- {title} ({url})")
    
#     # Step 3: After research, post articles from the database
#     print("\n📤 Posting articles from the database...")
#     post_from_db_workflow(query)

# if __name__ == "__main__":
#     main()


