from openai import OpenAI
import os
from dotenv import load_dotenv
from helper import PromptHelper

load_dotenv()


def get_api(model_name):
    if "gpt" in model_name:
        return os.getenv("OPENAI_API_KEY"), "https://api.openai.com/v1"

    return os.getenv("PERPLEXITY_API_KEY"), "https://api.perplexity.ai"


def open_ai_completion(instruction, user_message, model_name, task, language):
    api_key, base_url = get_api(model_name)
    client = OpenAI(api_key=api_key, base_url=base_url)
    prompt = PromptHelper.get_prompt(task, language)
    model = PromptHelper.get_model(model_name)

    conversation = [
        {"role": "system", "content": prompt["system"]},
        {"role": "user", "content": f"{prompt['user']} {instruction}"},
        {"role": "assistant", "content": f"{prompt['assistant']} {user_message}"},
        {"role": "user", "content": prompt["user_auto"]},
    ]

    completion = client.chat.completions.create(model=model, messages=conversation)

    tokens = PromptHelper.get_token_cost(
        completion.usage.prompt_tokens,
        completion.usage.completion_tokens,
        model_name,
    )
    reply = completion.choices[0].message.content
    return f"\n{reply}\n\n---\n\n{tokens}"


if __name__ == "__main__":
    instruction = "I need help with my computer"
    user_message = "My computer is not working"
    print(
        open_ai_completion(
            instruction, user_message, "gpt-3.5", "message_assistant", "swedish"
        )
    )
