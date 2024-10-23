from cryptoneurons.crawlers.twitter.apify import ApifyTwitterCrawler
from cryptoneurons.llm_evaluator.evaluator import Evaluator
from cryptoneurons.config import TWITTER_CRAWLER_CONFIG, APIFY_CONFIG, OPENAI_CONFIG, ALPHASCAN_KOL_ACCOUNTS
from cryptoneurons.utils.utils import truncate_tweets_by_token_limit, send_message_to_channel
from datetime import datetime, timedelta
import os
import time
from tqdm import tqdm

os.environ['TZ'] = 'UTC'
time.tzset()


# kol_accounts = TWITTER_CRAWLER_CONFIG["kol_accounts"]
kol_accounts = ALPHASCAN_KOL_ACCOUNTS
# print(kol_accounts)

if __name__ == "__main__":


    # -----Scrape Tweets-----

    # Crawl the tweets of kols for past 24 hours
    st = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d")
    et = datetime.now().strftime("%Y-%m-%d")

    twitter_crawler = ApifyTwitterCrawler(api_key=APIFY_CONFIG["api_key"])
    results = twitter_crawler.get_tweet_by_accounts(twitter_handles=kol_accounts,
                                                    start=st,
                                                    end=et,
                                                    minimum_retweets=None,
                                                    minimum_favorites=20,
                                                    minimum_replies=5,
                                                    sort="Latest"
                                                    )
    tweets = twitter_crawler.process_list(results)


    # -----Evaluation and Summary-----

    evaluator = Evaluator(api_key=OPENAI_CONFIG['api_key'], organization=OPENAI_CONFIG['organization'])

    # Truncate tweets due to the token length limiation of LLM
    tweet_epoches = truncate_tweets_by_token_limit(tweets=tweets, token_limit=10000)
    summaries_container = []
    for tweet_epoch in tqdm(tweet_epoches):
        summary_res = evaluator.tweets_summary(tweet_epoch)
        summaries_container.extend(summary_res['results'])


    for item in summaries_container:
        message = f"🔹 Keyword: {item['keyword']}\n" \
                  f"🟢 Sentiment Assessment: {item['sentiment_assessment']}\n" \
                  f"🔥 Popularity: {item['Popularity']}\n" \
                  f"🌟 Viewpoints: {item['Viewpoints']}\n\n"

        send_message_to_channel(message)
        time.sleep(3)

    """
    # No need to re-summarize
    if len(tweet_epoches) == 1:
        for item in summaries_container:
            message = f"🔹 Keyword: {item['keyword']}\n" \
                      f"🟢 Sentiment Assessment: {item['sentiment_assessment']}\n" \
                      f"🔥 Popularity: {item['Popularity']}\n" \
                      f"🌟 Viewpoints: {item['Viewpoints']}\n\n"

            send_message_to_channel(message)
            time.sleep(3)
    else:
        # Re-summarize
        final_summary = evaluator.responses_summary(responses=summaries_container)

        for item in final_summary['results']:
            message = f"🔹 Keyword: {item['keyword']}\n" \
                    f"🟢 Sentiment Assessment: {item['sentiment_assessment']}\n" \
                    f"🔥 Popularity: {item['Popularity']}\n" \
                    f"🌟 Viewpoints: {item['Viewpoints']}\n\n"

            send_message_to_channel(message)
            time.sleep(3)
    """