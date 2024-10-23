from cryptoneurons.crawlers.twitter.apify_deprecated import ApifyTwitterCrawler
from cryptoneurons.config import APIFY_CONFIG

if __name__ == "__main__":
    twitter_crawler = ApifyTwitterCrawler(api_key=APIFY_CONFIG["api_key"])
    results = twitter_crawler.get_tweet_by_keywords(search_terms=["$BVM"], start="2024-01-01", end="2024-06-01", sort="Latest")
    tweets = twitter_crawler.process_list(results)
    print(tweets)