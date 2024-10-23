import traceback
from datetime import datetime
from openai import OpenAI
import pathlib
from cryptoneurons.utils.utils import LlmInputEncoder, auto_json_decode

with open(f"{pathlib.Path(__file__).parent.resolve()}/instructions.txt") as f:
    instructions = f.read()



class Evaluator:

    def __init__(self, api_key, organization) -> None:

        self.llm_client = OpenAI(api_key=api_key, organization=organization)



    def tweets_summary(self, docs, retries=3):
        """
        This function evaluates the documents using the LLM.
        """
        try:

            encoded_input = LlmInputEncoder.encode_tweets(docs)

            messages = [
                {
                    "role": "system",
                    "content": instructions
                },
                {
                    "role": "system",
                    "content": f"Current Time: {datetime.now().isoformat().split('T')[0]}",
                },
                {
                    "role": "user",
                    "content": f"You will be given a list of documents and you have to perform the summary task.",
                },
                {
                    "role": "user",
                    "content": "Must answer in JSON format like: {results: [{'keyword': A keyword summarized from the given documents, e.g. '$Tao', 'sentiment_assessment': The overall sentiment assessment of the tweets related to the keyword, e.g. 'somewhat positive', 'Popularity': The number of relevant tweets mentioning the keyword, e.g. 3, 'Viewpoints': Important viewpoints or insights related to the keyword, e.g. 'A lot of smart money are flowing into $Tao'}, {'keyword': .....}]}"
                },
                {
                    "role": "user", "content": f"The documents are as follows:\n {encoded_input}"
                }
            ]

            output = self.llm_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={"type": "json_object"},
                messages=messages,
                temperature=0,
            )

        except:
            print(traceback.format_exc())
            return None

        try:
            result = auto_json_decode(output.choices[0].message.content)
            return result
        except:

            if retries > 0:
                return self.tweets_summary(docs, retries - 1)
            else:
                raise Exception(
                    f"Failed to parse LLM result after retrying. Returning 0."
                )

    def responses_summary(self, responses, retries=3):
        """
        This function re-summary the responses from llm
        """
        try:
            encoded_input = LlmInputEncoder.encode_responses(responses=responses)

            messages = [
                {
                    "role": "system",
                    "content": instructions
                },
                {
                    "role": "system",
                    "content": f"Current Time: {datetime.now().isoformat().split('T')[0]}",
                },
                {
                    "role": "user",
                    "content": f"You will be given a list of responses from llm client that each response is the summary for a list of documents. And you need to merge these summaries and summarize them further.",
                },
                {
                    "role": "user",
                    "content": "Must answer in JSON format like: {results: [{'keyword': A keyword summarized from the given documents, e.g. '$Tao', 'sentiment_assessment': The overall sentiment assessment of the tweets related to the keyword, e.g. 'somewhat positive', 'Popularity': The number of relevant tweets mentioning the keyword, e.g. 3, 'Viewpoints': Important viewpoints or insights related to the keyword, e.g. 'A lot of smart money are flowing into $Tao'}, {'keyword': .....}]}"
                },
                {
                    "role": "user", "content": f"The summaries are as follows:\n {encoded_input}"
                }
            ]

            output = self.llm_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={"type": "json_object"},
                messages=messages,
                temperature=0,
            )

        except:
            print(traceback.format_exc())
            return None

        try:
            result = auto_json_decode(output.choices[0].message.content)
            return result
        except:

            if retries > 0:
                return self.responses_summary(responses, retries - 1)
            else:
                raise Exception(
                    f"Failed to parse LLM result after retrying. Returning 0."
                )