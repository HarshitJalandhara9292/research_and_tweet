import tweepy

auth = tweepy.OAuthHandler("TWITTER_CONSUMER_KEY", "TWITTER_CONSUMER_SECRET")
auth.set_access_token("TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET")
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("✅ Twitter Authentication Successful!")
except tweepy.TweepyException as e:
    print(f"🚨 Authentication Error: {e}")
