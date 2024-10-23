from datetime import datetime
from apify_client import ApifyClient
from typing import List


class ApifyParamsConstructor:

    @classmethod
    def construct_params(cls, start_urls=[], search_terms=[], twitter_handles=[], conversation_ids=[],
                         max_tweets_per_query=None, tweet_language=None, max_items=None, sort="Latest",
                         only_verified_users=False, only_twitter_blue=False, only_image=False,
                         only_video=False, only_quote=False, author=None, in_reply_to=None,
                         mentioning=None, geotagged_near=None, within_radius=None, geocode=None,
                         place_object_id=None, minimum_retweets=None, minimum_favorites=None,
                         minimum_replies=None, start=None, end=None, include_search_terms=False,
                         custom_map_function="(object) => { return {...object} }"):
        """
        Constructs the params dictionary for the tweet scraper API.

        Args:
            start_urls (list): List of Twitter (X) URLs.
            search_terms (list): List of search terms to search on Twitter (X).
            twitter_handles (list): List of Twitter handles to search on Twitter (X).
            conversation_ids (list): List of conversation IDs to search on Twitter (X).
            max_tweets_per_query (int): Maximum number of tweets to return per query.
            tweet_language (str): Restricts tweets to the given language, given by an ISO 639-1 code.
            max_items (int): Maximum number of items to receive as output.
            sort (str): Sorts search results by the given option. Only works with search terms and search URLs. ["Latest", "Top", "Media"]
            only_verified_users (bool): If True, only returns tweets by verified users.
            only_twitter_blue (bool): If True, only returns tweets by Twitter Blue subscribers.
            only_image (bool): If True, only returns tweets that contain images.
            only_video (bool): If True, only returns tweets that contain videos.
            only_quote (bool): If True, only returns tweets that are quotes.
            author (str): Returns tweets sent by the given user.
            in_reply_to (str): Returns tweets that are replies to the given user.
            mentioning (str): Returns tweets mentioning the given user.
            geotagged_near (str): Returns tweets sent near the given location.
            within_radius (str): Returns tweets sent within the given radius of the given location.
            geocode (str): Returns tweets sent by users located within a given radius of the given latitude/longitude.
            place_object_id (str): Returns tweets tagged with the given place.
            minimum_retweets (int): Returns tweets with at least the given number of retweets.
            minimum_favorites (int): Returns tweets with at least the given number of favorites.
            minimum_replies (int): Returns tweets with at least the given number of replies.
            start (str): Returns tweets sent after the given date.
            end (str): Returns tweets sent before the given date.
            include_search_terms (bool): If True, adds a field to each tweet about the search term used to find it.
            custom_map_function (str): Function that takes each object as argument and returns data mapped by the function.

        Returns:
            dict: The params dictionary for the API request.
        """
        params = {
            'startUrls': start_urls,
            'searchTerms': search_terms,
            'twitterHandles': twitter_handles,
            'conversationIds': conversation_ids,
            'sort': sort,
            'maxTweetsPerQuery': max_tweets_per_query,
            'tweetLanguage': tweet_language,
            'maxItems': max_items,
            'onlyVerifiedUsers': only_verified_users,
            'onlyTwitterBlue': only_twitter_blue,
            'onlyImage': only_image,
            'onlyVideo': only_video,
            'onlyQuote': only_quote,
            'author': author,
            'inReplyTo': in_reply_to,
            'mentioning': mentioning,
            'geotaggedNear': geotagged_near,
            'withinRadius': within_radius,
            'geocode': geocode,
            'placeObjectId': place_object_id,
            'minimumRetweets': minimum_retweets,
            'minimumFavorites': minimum_favorites,
            'minimumReplies': minimum_replies,
            'start': start,
            'end': end,
            'includeSearchTerms': include_search_terms,
            'customMapFunction': custom_map_function
        }

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        return params


class ApifyTwitterCrawler:
    def __init__(self, api_key):
        self.client = ApifyClient(api_key)

        # users may use any other actor id that can crawl twitter data
        self.actor_id = "apidojo/tweet-scraper"

    def get_tweet_by_url(self, start_urls, start=None, end=None, tweet_language=None, max_items=None,
                         only_verified_users=False, only_twitter_blue=False, minimum_retweets=None,
                         minimum_favorites=None,
                         minimum_replies=None):
        """

        Get tweets by url.
        The url can be a specific post or reply. It can also be a customed advanced search supported by twitter.
        Example: https://twitter.com/search?f=live&q=(from%3ACryptoApprenti1)%20until%3A2024-03-22%20since%3A2024-03-20%20-filter%3Areplies&src=typed_query

        """

        params = ApifyParamsConstructor.construct_params(start_urls=start_urls, start=start, end=end,
                                                         tweet_language=tweet_language, max_items=max_items,
                                                         only_verified_users=only_verified_users,
                                                         only_twitter_blue=only_twitter_blue,
                                                         minimum_retweets=minimum_retweets,
                                                         minimum_favorites=minimum_favorites,
                                                         minimum_replies=minimum_replies)

        run = self.client.actor(self.actor_id).call(
            run_input=params
        )

        results = [
            item
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items()
        ]
        return results

    def get_tweet_by_keywords(self, search_terms, start=None, end=None, sort=None, tweet_language=None, max_items=None,
                              only_verified_users=False, only_twitter_blue=False, minimum_retweets=None,
                              minimum_favorites=None,
                              minimum_replies=None):
        """

        Searches for the given query on the crawled data.

        """

        params = ApifyParamsConstructor.construct_params(search_terms=search_terms, start=start, end=end, sort=sort,
                                                         tweet_language=tweet_language, max_items=max_items,
                                                         only_verified_users=only_verified_users,
                                                         only_twitter_blue=only_twitter_blue,
                                                         minimum_retweets=minimum_retweets,
                                                         minimum_favorites=minimum_favorites,
                                                         minimum_replies=minimum_replies)

        run = self.client.actor(self.actor_id).call(
            run_input=params
        )

        results = [
            item
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items()
        ]
        return results

    def get_tweet_by_accounts(self, twitter_handles, start=None, end=None, sort=None, tweet_language=None,
                              max_items=None,
                              minimum_retweets=None, minimum_favorites=None, minimum_replies=None):
        """
        Searches for the given account handle on the crawled data.

        """
        search_terms = [f"from:{twitter_handle} since:{start} until:{end}" for twitter_handle in twitter_handles]
        params = ApifyParamsConstructor.construct_params(search_terms=search_terms, sort=sort,
                                                         tweet_language=tweet_language,
                                                         max_items=max_items, minimum_retweets=minimum_retweets,
                                                         minimum_favorites=minimum_favorites,
                                                         minimum_replies=minimum_replies)

        run = self.client.actor(self.actor_id).call(
            run_input=params
        )

        results = [
            item
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items()
        ]
        return results

    def process_item(self, item):
        """
        Process the item.
        You can see the details of each data fields in https://apify.com/apidojo/tweet-scraper
        Args:
            item (dict): The item to process.

        Returns:
            dict: The processed item.
        """
        time_format = "%a %b %d %H:%M:%S %z %Y"
        return {
            "id": item.get("id"),
            "url": item.get("url"),
            "type": item.get("type"),
            "author_name": item["author"]["userName"],
            "author_description": item["author"]["description"],
            "author_created_at": datetime.strptime(
                item["author"]["createdAt"], time_format
            ).isoformat(),
            "author_followers": item["author"]["followers"],
            "author_media_count": item["author"]["mediaCount"],
            "author_statuses_count": item["author"]["statusesCount"],
            "author_is_veried": item["author"]["isVerified"],
            # "author_account_type": item["author"]["advertiserAccountType"],
            "text": item.get("text"),
            "createdAt": datetime.strptime(
                item.get("createdAt"), time_format
            ).isoformat(),
            "retweetCount": item.get("retweetCount"),
            "replyCount": item.get("replyCount"),
            "likeCount": item.get("likeCount"),
            "quoteCount": item.get("quoteCount"),
            "isReply": item.get("isReply"),
            "isRetweet": item.get("isRetweet"),
            "isQuote": item.get("isQuote"),
            ## Todo: Add quote information(The twitter that has been quoted by this author could be informative and should be regarded as an independent tweet)
            "language": item.get("lang")
        }

    def process_list(self, results):
        """
        Process the results from the search.

        Args:
            results (list): The list of results to process.

        Returns:
            list: The list of processed results.
        """
        return [self.process_item(result) for result in results]

