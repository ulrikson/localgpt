import anthropic
import os
from dotenv import load_dotenv
from helper import PromptHelper

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)


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

    tokens = PromptHelper.get_token_cost(
        completion.usage.input_tokens, completion.usage.output_tokens, model_name
    )
    reply = completion.content[0].text
    return f"\n{reply}\n\n---\n\n{tokens}"


if __name__ == "__main__":
    instruction = "Help me write a Jira ticket for a bug."
    user_message = "One user, David, is really slow to load the page."
    reply = claude_completion(
        instruction, user_message, "haiku", "pm_assistant", "english"
    )
    print(reply)
