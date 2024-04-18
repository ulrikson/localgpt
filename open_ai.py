from openai import OpenAI
import os
from dotenv import load_dotenv
from helper import PromptHelper


class OpenAIClient:
    def __init__(self, api_key, base_url, model_name="gpt-4"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    def get_model(self):
        if self.model_name == "gpt-4":
            return "gpt-4-turbo-preview"
        elif self.model_name == "gpt-3.5":
            return "gpt-3.5-turbo"
        elif self.model_name == "sonar":
            return "sonar-small-chat"
        elif self.model_name == "mistral":
            return "mistral-7b-instruct"
        elif self.model_name == "codellama":
            return "codellama-70b-instruct"
        elif self.model_name == "mixtral":
            return "mixtral-8x22b-instruct"
        else:
            return None

    def get_token_cost(self, response):
        tokens = response.usage
        input = tokens.prompt_tokens
        output = tokens.completion_tokens

        if self.model_name == "gpt-4":
            cost = 10 * (10 * input + 30 * output) / 1000000  # SEK
        elif self.model_name == "gpt-3.5":
            cost = 10 * (0.50 * input + 1.50 * output) / 1000000  # SEK
        elif self.model_name == "sonar" or self.model_name == "mistral":
            cost = 10 * 0.20 * (input + output) / 1000000  # SEK
        elif self.model_name == "codellama" or self.model_name == "mixtral":
            cost = 10 * 1 * (input + output) / 1000000
        else:
            return None

        return f"{cost:.3f} SEK ({input} input tokens, {output} output tokens)"

    def completion(
        self, instruction, user_message, task="message_assistant", language="swedish"
    ):
        prompt = PromptHelper.get_prompt(task, language)

        # Define the chat conversation
        conversation = [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": f"{prompt['user']} {instruction}"},
            {"role": "assistant", "content": f"{prompt['assistant']} {user_message}"},
            {"role": "user", "content": prompt["user_auto"]},
        ]

        # Call the OpenAI API for chat completion
        completion = self.client.chat.completions.create(
            model=self.get_model(), messages=conversation, temperature=0.5
        )

        tokens = self.get_token_cost(completion)
        reply = completion.choices[0].message.content
        return f"\n{reply}\n\n---\n\n{tokens}"


def ask(instruction, user_message, model_name, task, language):
    load_dotenv()
    if model_name == "gpt-4" or model_name == "gpt-3.5":
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = "https://api.openai.com/v1"
    else:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        base_url = "https://api.perplexity.ai"

    client = OpenAIClient(api_key, base_url, model_name)
    reply = client.completion(instruction, user_message, task, language)

    return reply


if __name__ == "__main__":
    instruction = "I need help with my computer"
    user_message = "My computer is not working"
    task = "message_assistant"
    language = "swedish"
    model_name = "gpt-3.5"
    print(ask(instruction, user_message, model_name, task, language))
