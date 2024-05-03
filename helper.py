import json

MODEL_DICT = {
    "llama3-8b": {
        "model": "llama-3-8b-instruct",
        "input_cost": 0.20,
        "output_cost": 0.20,
    },
    "haiku": {
        "model": "claude-3-haiku-20240307",
        "input_cost": 0.25,
        "output_cost": 1.25,
    },
    "gpt-4": {
        "model": "gpt-4-turbo-preview",
        "input_cost": 10,
        "output_cost": 30,
    },
    "sonnet": {
        "model": "claude-3-sonnet-20240229",
        "input_cost": 3,
        "output_cost": 15,
    },
    "opus": {
        "model": "claude-3-opus-20240229",
        "input_cost": 15,
        "output_cost": 75,
    },
    "llama3-70b": {
        "model": "llama-3-70b-instruct",
        "input_cost": 1,
        "output_cost": 1,
    },
    "gpt-3.5": {
        "model": "gpt-3.5-turbo",
        "input_cost": 0.50,
        "output_cost": 1.50,
    },
    "sonar": {
        "model": "sonar-small-chat",
        "input_cost": 0.20,
        "output_cost": 0.20,
    },
    "mixtral": {
        "model": "mixtral-8x22b-instruct",
        "input_cost": 1,
        "output_cost": 1,
    },
}


class PromptHelper:
    @staticmethod
    def get_prompt(task, language):
        with open("/Users/eriklp/code/localgpt/prompts.json") as file:
            prompt = json.load(file)

        return prompt[language][task]

    @staticmethod
    def get_model(model_name):
        return MODEL_DICT[model_name]["model"]

    @staticmethod
    def get_token_cost(input_tokens, output_tokens, model_name):
        input_cost = MODEL_DICT[model_name]["input_cost"]
        output_cost = MODEL_DICT[model_name]["output_cost"]

        usd_to_sek = 10.0
        cost = (
            usd_to_sek
            * (input_cost * input_tokens + output_cost * output_tokens)
            / 1000000
        )
        return f"{cost:.3f} SEK ({input_tokens} input tokens, {output_tokens} output tokens)"
