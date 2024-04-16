from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_prompt(task):
    with open("/Users/eriklp/code/localgpt/prompts.json") as file:
        prompt = json.load(file)

    return prompt[task]


def get_model(model_name):
    if model_name == "gpt-4":
        return "gpt-4-turbo-preview"
    else:
        return None


def chatgpt_completion(
    instruction, user_message, model_name="gpt-4", task="message_assistant"
):
    prompt = get_prompt(task)

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
        model=get_model(model_name), messages=conversation, temperature=0.5
    )

    # Extract and return the generated reply
    reply = completion.choices[0].message.content
    return reply


if __name__ == "__main__":
    instruction = "Min kollega har rapporterat en bugg i Slack som jag behöver mer info om. jag ska svara i en tråd. hjälp mig skriva om mitt utkast"
    user_message = "du skriver att det är en bugg vilket får mig att tro att nåt inte funkar, samtidigt verkar det på bilden som att det snarare är att popupen syns men inte där du tänkt. hur är det"
    reply = chatgpt_completion(instruction, user_message)
    print(reply)
