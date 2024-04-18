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
        return "mixtral-8x22b-instruct"


def get_token_cost(response, model_name):
    tokens = response.usage
    input = tokens.prompt_tokens
    output = tokens.completion_tokens

    if model_name == "sonar" or model_name == "mistral":
        cost = 10 * 0.20 * (input + output) / 1000000  # SEK
    elif model_name == "codellama" or model_name == "mixtral":
        cost = 10 * 1 * (input + output) / 1000000

    return f"{cost:.3f} SEK ({input} input tokens, {output} output tokens)"


def perplexity_completion(
    instruction,
    user_message,
    model_name="sonar",
    task="message_assistant",
    language="swedish",
):
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

    tokens = get_token_cost(completion, model_name)
    reply = completion.choices[0].message.content
    return f"\n{reply}\n\n---\n\n{tokens}"


if __name__ == "__main__":
    instruction = "Min kollega har rapporterat en bugg i Slack som jag behöver mer info om. jag ska svara i en tråd. hjälp mig skriva om mitt utkast"
    user_message = "du skriver att det är en bugg vilket får mig att tro att nåt inte funkar, samtidigt verkar det på bilden som att det snarare är att popupen syns men inte där du tänkt. hur är det"
    reply = perplexity_completion(instruction, user_message, "sonar", "message_assistant", "swedish")
    print(reply)
