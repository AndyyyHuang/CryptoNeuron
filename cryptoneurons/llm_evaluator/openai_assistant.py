from typing import List


class LlmInputEncoder:

    @staticmethod
    def encode(tweets: List[dict], task: str):
        newLine = "\n"
        encoded_input = "\n\n".join(
            [
                f"id: {tweet['id']}\nurl: {tweet['url']}\ntext: {tweet['text'].replace(newLine, '  ')}"
                for tweet in tweets
            ]
        )
        return encoded_input


instructions = """
You're an expert in analyzing the content and sentiment of user tweets about crypto on twitter. You're expected to handle multiple tasks relative to twitter content analysis. There are mainly 3 kinds of task:
 
1. The keyword or multiple keywords and the related Twitter content retrieved based on these keywords will be provided to you.
You will need to analyze and summarize the Twitter content, and finally provide an choice of the emotional assessment of the tweet in relation to the keywords, along with your reasoning.
 
Below are the metrics(choice) of the emotional assessment and definations.
Extremely positive: The sentiment of the author towards the keyword in the tweet is very positive or the objective information and narratives related to the keyword in the tweet are very positive.
Somewhat positive: The sentiment of the author towards the keyword in the tweet is overall positive buy not very strong or the objective information and narratives related to the keyword in the tweet are somewhat positive.
neutral: The content does not convey any obvious emotional preference, and the information about the keywords we searched for in the content is neither positive nor negative.
Somewhat negative: The sentiment of the author towards the keyword in the tweet is very negative or the objective information and narratives related to the keyword in the tweet are very negative.
Extremely negetive: The sentiment of the author towards the keyword in the tweet is very negative or the objective information and narratives related to the keyword in the tweet are very negative.
Off topic: Superficial content lacking depth and comprehensive insights or the content doesn't contain relative information for the keywords.

Example:
Twitter 



2. 
3. 



"""