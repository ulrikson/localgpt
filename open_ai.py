from openai import OpenAI
import os
from dotenv import load_dotenv
from helper import PromptHelper


class OpenAIClient:
    def __init__(self, api_key, base_url, model_name="gpt-4"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    def get_token_cost(self, response):
        tokens = response.usage
        input = tokens.prompt_tokens
        output = tokens.completion_tokens

        model_costs = {
            "gpt-4": (10, 30),
            "gpt-3.5": (0.50, 1.50),
            "sonar": (0.20, 0.20),
            "mistral": (0.20, 0.20),
            "codellama": (1, 1),
            "mixtral": (1, 1),
        }

        input_cost, output_cost = model_costs[self.model_name]
        usd_to_sek = 10.0
        cost = usd_to_sek * (input_cost * input + output_cost * output) / 1000000
        return f"{cost:.3f} SEK ({input} input tokens, {output} output tokens)"

    def completion(self, instruction, user_message, task, language):
        prompt = PromptHelper.get_prompt(task, language)
        model = PromptHelper.get_model(self.model_name)

        # Define the chat conversation
        conversation = [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": f"{prompt['user']} {instruction}"},
            {"role": "assistant", "content": f"{prompt['assistant']} {user_message}"},
            {"role": "user", "content": prompt["user_auto"]},
        ]

        # Call the OpenAI API for chat completion
        completion = self.client.chat.completions.create(
            model=model, messages=conversation
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
