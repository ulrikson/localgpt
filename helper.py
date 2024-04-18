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
