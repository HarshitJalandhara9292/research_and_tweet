import os
import pinecone
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.twitter import TwitterTools
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import tweepy

load_dotenv()

class TwitterAgent:
    def __init__(self):
        """Initialize Twitter agent with API credentials and Pinecone vector search."""

        required_keys = [
            "TWITTER_CONSUMER_KEY", "TWITTER_CONSUMER_SECRET",
            "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET",
            "PINECONE_API_KEY", "PINECONE_INDEX_NAME"
        ]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        if missing_keys:
            raise ValueError(f"🚨 Missing API keys in .env file: {', '.join(missing_keys)}")

        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_CONSUMER_KEY"),
            os.getenv("TWITTER_CONSUMER_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        self.api = tweepy.API(auth)
        try:
            user = self.api.verify_credentials()
            print(f"✅ Authorized to tweet as: @{user.screen_name}")
        except Exception as e:
            print(f"🚨 Error verifying Twitter credentials: {e}")
            raise

        self.twitter_tools = TwitterTools()

        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index_name = os.getenv("PINECONE_INDEX_NAME")
        if index_name not in self.pc.list_indexes().names():
            raise ValueError(f"🚨 Pinecone index '{index_name}' not found.")
        self.index = self.pc.Index(index_name)
        print(f"✅ Connected to Pinecone index: {index_name}")

        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.agent = Agent(
            model=Gemini(id="gemini-1.5-flash"),
            tools=[self.twitter_tools],
            description="Posts relevant news articles on Twitter using vector search.",
            instructions=[
                "Post the most important news articles on Twitter.",
                "Ensure tweets are engaging and within 280 characters.",
                "Include relevant hashtags like #AI, #Tech, etc.",
                "If the article is technical, simplify it for a wider audience.",
                "Include a call-to-action (CTA) like 'Read more here'."
            ],
            markdown=True,
            show_tool_calls=True,
        )

    def search_relevant_news(self, query):
        """Fetch the most relevant news article from Pinecone using vector search."""
        print(f"🔍 Searching Pinecone for: {query}")
        query_vector = self.embedding_model.encode(query).tolist()
        results = self.index.query(vector=query_vector, top_k=1, include_metadata=True)

        if not results.get("matches"):
            print("❌ No relevant articles found.")
            return None

        article = results["matches"][0]["metadata"]
        print(f"✅ Found: {article.get('title', 'No Title')} - {article.get('url', '')}")
        return article

    def post_from_pinecone(self, query):
        """Search and post news article on Twitter."""
        article = self.search_relevant_news(query)
        if not article:
            print("🚨 Nothing to post.")
            return

        tweet = f"{article.get('title', 'No Title')}\n\n{article.get('content', '')[:200]}... Read more: {article.get('url', '')}"

        try:
            response = self.twitter_tools.create_tweet(tweet)
            print(f"✅ Tweet posted: {response}")
        except Exception as e:
            print(f"🚨 Error posting tweet: {e}")

if __name__ == "__main__":
    agent = TwitterAgent()
    topic = input("🔍 Enter a topic to post about: ")
    agent.post_from_pinecone(topic)


