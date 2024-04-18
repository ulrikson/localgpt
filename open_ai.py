from openai import OpenAI
import os
from dotenv import load_dotenv
from helper import PromptHelper

load_dotenv()


def get_api_key(model_name):
    if model_name == "gpt-4" or model_name == "gpt-3.5":
        return os.getenv("OPENAI_API_KEY")
    return os.getenv("PERPLEXITY_API_KEY")


def get_base_url(model_name):
    if model_name == "gpt-4" or model_name == "gpt-3.5":
        return "https://api.openai.com/v1"
    return "https://api.perplexity.ai"


def open_ai_completion(instruction, user_message, model_name, task, language):
    client = OpenAI(api_key=get_api_key(model_name), base_url=get_base_url(model_name))
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
    task = "message_assistant"
    language = "swedish"
    model_name = "gpt-3.5"
    print(open_ai_completion(instruction, user_message, model_name, task, language))
