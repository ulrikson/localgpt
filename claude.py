import anthropic
import os
from dotenv import load_dotenv
from helper import PromptHelper

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)


def get_token_cost(response, model_name):
    tokens = response.usage
    input = tokens.input_tokens
    output = tokens.output_tokens

    if model_name == "haiku":
        cost = 10 * (0.25 * input + 1.25 * output) / 1000000  # SEK
    elif model_name == "sonnet":
        cost = 10 * (3 * input + 15 * output) / 1000000  # SEK
    elif model_name == "opus":
        cost = 10 * (15 * input + 75 * output) / 1000000

    return f"{cost:.3f} SEK ({input} input tokens, {output} output tokens)"


def claude_completion(
    instruction, user_message, model_name, task="message_assistant", language="swedish"
):
    prompt = PromptHelper.get_prompt(task, language)
    model = PromptHelper.get_model(model_name)

    completion = client.messages.create(
        model=model,
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

    tokens = get_token_cost(completion, model_name)
    reply = completion.content[0].text
    return f"\n{reply}\n\n---\n\n{tokens}"


if __name__ == "__main__":
    instruction = "Help me write a Jira ticket for a bug."
    user_message = "One user, David, is really slow to load the page."
    reply = claude_completion(
        instruction, user_message, "haiku", "pm_assistant", "english"
    )
    print(reply)
