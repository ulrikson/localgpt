from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Load the API key from the environment variable
api_key = os.getenv("PERPLEXITY_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.perplexity.ai",
)


def get_prompt(task, language):
    with open("/Users/eriklp/code/localgpt/prompts.json") as file:
        prompt = json.load(file)

    return prompt[language][task]


def get_model(model_name):
    # Models: https://docs.perplexity.ai/docs/model-cards
    if model_name == "sonar":
        return "sonar-small-chat"
    elif model_name == "mistral":
        return "mistral-7b-instruct"
    elif model_name == "codellama":
        return "codellama-70b-instruct"
    elif model_name == "mixtral":
        return "mixtral-8x7b-instruct"


def perplexity_completion(instruction, user_message, model_name="sonar", task="message_assistant", language="swedish"):
    prompt = get_prompt(task, language)

    # Define the chat conversation
    conversation = [
        {
            "role": "system",
            "content": prompt["system"],
        },
        {"role": "user", "content": f"{prompt['user']} {instruction}"},
        {
            "role": "assistant",
            "content": f"{prompt['assistant']} {user_message}",
        },
        {"role": "user", "content": prompt["user_auto"]},
    ]

    # Call the OpenAI API for chat completion
    completion = client.chat.completions.create(
        model=get_model(model_name), messages=conversation
    )

    # Extract and return the generated reply
    reply = completion.choices[0].message.content
    return reply


if __name__ == "__main__":
    instruction = "What's the best way to write a Python class?"
    user_message = "I'm trying to learn object-oriented programming."
    reply = perplexity_completion(instruction, user_message, "sonar")
    print(reply)
