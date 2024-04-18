import json


class PromptHelper:
    @staticmethod
    def get_prompt(task, language):
        with open("/Users/eriklp/code/localgpt/prompts.json") as file:
            prompt = json.load(file)

        return prompt[language][task]

    @staticmethod
    def get_model(model_name):
        model_mapping = {
            "gpt-4": "gpt-4-turbo-preview",
            "gpt-3.5": "gpt-3.5-turbo",
            "sonar": "sonar-small-chat",
            "mistral": "mistral-7b-instruct",
            "codellama": "codellama-70b-instruct",
            "mixtral": "mixtral-8x22b-instruct",
            "haiku": "claude-3-haiku-20240307",
            "sonnet": "claude-3-sonnet-20240229",
            "opus": "claude-3-opus-20240229",
        }

        return model_mapping.get(model_name, None)

    @staticmethod
    def get_token_cost(input_tokens, output_tokens, model_name):
        model_costs = {
            "gpt-4": (10, 30),
            "gpt-3.5": (0.50, 1.50),
            "sonar": (0.20, 0.20),
            "mistral": (0.20, 0.20),
            "codellama": (1, 1),
            "mixtral": (1, 1),
            "haiku": (0.25, 1.25),
            "sonnet": (3, 15),
            "opus": (15, 75),
        }

        input_cost, output_cost = model_costs[model_name]
        usd_to_sek = 10.0
        cost = (
            usd_to_sek
            * (input_cost * input_tokens + output_cost * output_tokens)
            / 1000000
        )
        return f"{cost:.3f} SEK ({input_tokens} input tokens, {output_tokens} output tokens)"
