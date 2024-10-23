from typing import List
from telegram import Bot
import asyncio
from cryptoneurons.config import TELEGRAM_CONFIG
import json

class LlmInputEncoder:

    @staticmethod
    def encode_tweets(tweets: List[dict]):
        newLine = "\n"
        encoded_input = "\n\n".join(
            [
                f"itemId: {i}\nid: {tweet['id']}\nurl: {tweet['url']}\ntext: {tweet['text'].replace(newLine, '  ')}"
                for i, tweet in enumerate(tweets)
            ]
        )
        return encoded_input

    @staticmethod
    def encode_responses(responses: List[dict]):

        encoded_input = "\n\n".join(
            [
                dict_to_str(response)
                for i, response in enumerate(responses)
            ]
        )
        return encoded_input

def dict_to_str(dic):
    # Create a list to store formatted key-value pairs
    formatted_pairs = []

    # Iterate over key-value pairs in the dictionary
    for key, value in dic.items():
        formatted_pairs.append(f"{key}: {value}")

    # Join the formatted pairs with a comma and space
    result_str = '\n'.join(formatted_pairs)

    return result_str


def truncate_tweets_by_token_limit(tweets, token_limit=10000):

    truncated_lis = []
    token_count = 0
    i = 0
    truncated_num = 0
    truncated_lis.append([])
    
    newLine = "\n"
    encoded_tweets = [
            f"itemId: {i}\nid: {tweet['id']}\nurl: {tweet['url']}\ntext: {tweet['text'].replace(newLine, '  ')}"
            for i, tweet in enumerate(tweets)
        ]
    
    for i, tweet_text in enumerate(encoded_tweets):

        token_count += len(tweet_text.split())
        truncated_lis[truncated_num].append(tweets[i])
        i += 1
        
        if token_count >= token_limit:
            truncated_num += 1
            truncated_lis.append([])
            token_count = 0
            
    return truncated_lis


def auto_json_decode(text):
    try:
        data = json.loads(text)
        # print("JSON loaded successfully:", data)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", str(e), "\n start auto fill")

        text = text.strip()
        if text.endswith("}"):
            completed_json_string = text + '''] }'''

        elif text.endswith("]"):
            completed_json_string = text + ''' }'''

        else:
            completed_json_string = text + '''."}] }'''

        data = json.loads(completed_json_string)
    return data


async def _send_message_to_channel(text):
    bot_token = TELEGRAM_CONFIG["bot_token"]
    channel_id = TELEGRAM_CONFIG["channel_id"]
    bot = Bot(bot_token)
    await bot.send_message(chat_id=channel_id, text=text)

def send_message_to_channel(text):
    asyncio.run(_send_message_to_channel(text))