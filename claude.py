import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)


def get_prompt(task):
    with open("/Users/eriklp/code/localgpt/prompts.json") as file:
        prompt = json.load(file)

    return prompt[task]


def get_model(model_name):
    if model_name == "haiku":
        return "claude-3-haiku-20240307"
    else:
        return None


def claude_completion(instruction, user_message, model_name, task="message_assistant"):
    prompt = get_prompt(task)

    completion = client.messages.create(
        model=get_model(model_name),
        max_tokens=2000,
        temperature=0,
        system=prompt["system"],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt['user']} {instruction}",
                    }
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt['assistant']} {user_message}",
                    }
                ],
            },
            {"role": "user", "content": prompt["user_auto"]},
        ],
    )

    return completion.content[0].text


if __name__ == "__main__":
    instruction = "Help me write a Jira ticket for a bug."
    user_message = "One user, David, is really slow to load the page."
    reply = claude_completion(instruction, user_message)
    print(reply)
